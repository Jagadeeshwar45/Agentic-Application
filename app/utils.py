import re
import logging
import tempfile
from faster_whisper import WhisperModel
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import (
    TranscriptsDisabled,
    NoTranscriptFound,
    VideoUnavailable
)
from youtube_transcript_api.formatters import TextFormatter

model = WhisperModel("base", device="cpu", compute_type="int8")
logger = logging.getLogger("YouTubeTool")

class Audio_Transcriber:
    @staticmethod
    def transcribe_audio(audio_bytes: bytes) -> str:
        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tmp:
            tmp_path = tmp.name
            tmp.write(audio_bytes)
            tmp.flush()
        
        try:
            segments, _ = model.transcribe(tmp_path)
            result = " ".join(seg.text.strip() for seg in segments)
            return result
        finally:
            try:
                import os
                os.unlink(tmp_path)
            except:
                pass


class YouTubeTool:
    @staticmethod
    def extract_video_id(url: str) -> str | None:
        patterns = [
            r'(?:v=|\/)([0-9A-Za-z_-]{11})', 
            r'shorts\/([0-9A-Za-z_-]{11})',
            r'^([0-9A-Za-z_-]{11})$'
        ]
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        return None

    @staticmethod
    def get_transcript(url: str) -> str:
        video_id = YouTubeTool.extract_video_id(url)
        if not video_id:
            return "❌ Invalid YouTube URL."

        try:
            try:
                transcript = YouTubeTranscriptApi.get_transcript(
                    video_id,
                    languages=['en'],
                    proxies={
                        'http': None,
                        'https': None
                    }
                )
                if not transcript:
                    return "⚠️ No transcript available for this video."
                text = ' '.join([entry['text'] for entry in transcript if entry.get('text')])
                
                if not text.strip():
                    return "⚠️ Transcript is empty or unavailable."
                    
                return text
                
            except Exception as e:
                try:
                    from pytube import YouTube
                    yt = YouTube(f"https://www.youtube.com/watch?v={video_id}")
                    caption = yt.captions.get_by_language_code('en')
                    if not caption:
                        caption = yt.captions.get_by_language_code('a.en')
                    if not caption:
                        raise Exception("No captions available")
                    return caption.generate_srt_captions()
                except Exception as fallback_error:
                    raise e from fallback_error

        except Exception as e:
            error_msg = str(e).lower()
            if 'transcripts disabled' in error_msg:
                return "⚠️ Transcripts are disabled for this video."
            elif 'no transcript' in error_msg:
                return "⚠️ No transcript available for this video."
            elif 'unavailable' in error_msg or 'private' in error_msg:
                return "❌ Video is unavailable or private."
            
            logger.error(f"Transcript Error for {video_id}: {e}")
            return f"⚠️ Could not retrieve transcript: {str(e)}"


class Fallback_Summarizer:
    @staticmethod
    def fallback_summary(text: str) -> str:
        sentences = [s.strip() for s in text.split(".") if len(s.strip()) > 20]

        if not sentences:
            return "Content extracted, but insufficient text to summarize."

        one_line = sentences[0]
        bullets = sentences[1:4] or sentences[:3]
        paragraph = ". ".join(sentences[:5])

        return (
            "### 📝 Executive Summary\n"
            f"{one_line}.\n\n"
            "### 🔑 Key Highlights\n" +
            "\n".join(f"- {b}." for b in bullets) +
            "\n\n### 📖 Deep Dive\n" +
            paragraph + "."
        )
