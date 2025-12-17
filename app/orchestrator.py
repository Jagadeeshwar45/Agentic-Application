from app.llm_service import LLMService
from app.utils import YouTubeTool
from app.utils import Fallback_Summarizer

class AgentOrchestrator:
    def __init__(self):
        self.llm = LLMService()

    def _detect_intent(self, query: str, has_file: bool) -> str | None:
        q = query.lower().strip()
        if any(greet in q for greet in ["hi", "hello", "hey", "good morning", "good evening"]):
            return "CHAT"

        if has_file:
            if "summarize" in q:
                return "SUMMARIZE"
            if "sentiment" in q or "tone" in q:
                return "SENTIMENT"
            if "explain" in q or "code" in q:
                return "CODE_EXPLAIN"
            if "extract" in q or "text" in q or "ocr" in q:
                return "EXTRACT"

        if not has_file and q.endswith("?"):
            return "CHAT"

        return None

    def plan_and_execute(self, query: str, file_bytes: bytes = None, file_type: str = None) -> dict:
        file_text = None

        if file_type == "audio" and file_bytes:
             from app.utils import Audio_Transcriber
             file_text = Audio_Transcriber.transcribe_audio(file_bytes)

        elif file_type == "image" and file_bytes:
             from app.processors import FileProcessor
             file_text = FileProcessor.process_image(file_bytes)

        elif file_type == "pdf" and file_bytes:
             from app.processors import FileProcessor
             file_text = FileProcessor.process_pdf(file_bytes)

        if "youtube.com" in query or "youtu.be" in query:
            fetched_transcript = YouTubeTool.get_transcript(query)
            
            if "❌" in fetched_transcript or "⚠️" in fetched_transcript:
                return {
                    "response": fetched_transcript, 
                    "action": "YOUTUBE_ERROR",
                    "needs_clarification": False
                }
            
            file_text = fetched_transcript
        
        has_file = bool(file_text)

        intent = self._detect_intent(query, has_file)

        if intent is None and "youtube" in query:
             intent = "EXTRACT"

        if intent is None and has_file:
            clarify = self.llm.generate("CLARIFY", "", query)
            return {
                "response": clarify["output"] if clarify["ok"] else "Could you clarify your request?",
                "action": "ask_clarification",
                "needs_clarification": True
            }

        if intent == "CHAT":
            llm = self.llm.generate("CHAT", "", query)
            return {
                "response": llm["output"] if llm["ok"] else "Hello! How can I help you today?",
                "action": "CHAT",
                "needs_clarification": False
            }

        if intent == "EXTRACT" and file_type in {"image", "pdf"}:
            if not has_file:
                return {"response": "No file to extract.", "action": "error"}

            return {
                "response": file_text,
                "action": "EXTRACT_TEXT"
            }

        if intent == "EXTRACT" and file_type == "audio":
            return {
                "response": (
                    "✅ **Audio Transcription Successful**\n"
                    "*Method: Speech-to-Text*\n\n"
                    + file_text
                ),
                "action": "AUDIO_TRANSCRIBE",
                "needs_clarification": False
            }

        context = file_text if has_file else query
        llm = self.llm.generate(intent, context, query)

        if llm["ok"]:
            return {"response": llm["output"], "action": intent}

        if llm["error"] == "LLM_QUOTA_EXCEEDED":
            if intent == "SUMMARIZE":
                return {
                    "response": Fallback_Summarizer.fallback_summary(context),
                    "action": "SUMMARIZE_FALLBACK"
                }

            return {
                "response": "⚠️ AI service temporarily unavailable.",
                "action": "LLM_UNAVAILABLE"
            }

        return {
            "response": "An unexpected error occurred.",
            "action": "error"
        }
