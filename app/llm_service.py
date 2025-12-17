import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY not found")

genai.configure(api_key=api_key)

MODEL_NAME = "gemini-2.5-flash"

model = genai.GenerativeModel(
    model_name=MODEL_NAME,
    generation_config={
        "temperature": 0.1,
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 4096,
    }
)

def is_quota_error(e: Exception) -> bool:
    msg = str(e).lower()
    return any(k in msg for k in [
        "quota",
        "429",
        "rate limit",
        "exceeded your current quota"
    ])

class LLMService:
    @staticmethod
    def generate(task: str, content: str, query: str = "") -> dict:

        if task == "SUMMARIZE":
            prompt = (
                "Summarize the content STRICTLY in this format:\n\n"
                "### 📝 Executive Summary\n"
                "(1 sentence)\n\n"
                "### 🔑 Key Highlights\n"
                "- Bullet 1\n- Bullet 2\n- Bullet 3\n\n"
                "### 📖 Deep Dive\n"
                "(Exactly 5 sentences)\n\n"
                f"CONTENT:\n{content[:8000]}"
            )

        elif task == "SENTIMENT":
            prompt = (
                "Analyze sentiment.\n"
                "Format: Label (Confidence 0–1) – One line justification.\n\n"
                f"CONTENT:\n{content[:8000]}"
            )

        elif task == "CODE_EXPLAIN":
            prompt = (
                "Analyze the code:\n"
                "1. Explain what it does\n"
                "2. Detect bugs or risks\n"
                "3. Mention time complexity\n\n"
                f"CODE:\n{content[:8000]}"
            )

        elif task == "CHAT":
            prompt = query

        elif task == "CLARIFY":
            prompt = (
                f"The user wrote: '{query}'.\n"
                "Ask ONE short clarification question."
            )

        else:
            return {"ok": False, "output": "", "error": "UNKNOWN_TASK"}

        try:
            resp = model.generate_content(prompt)
            return {"ok": True, "output": resp.text}

        except Exception as e:
            if is_quota_error(e):
                return {"ok": False, "output": "", "error": "LLM_QUOTA_EXCEEDED"}
            return {"ok": False, "output": "", "error": "LLM_FAILURE"}
