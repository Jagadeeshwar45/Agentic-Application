from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from app.orchestrator import AgentOrchestrator
from app.processors import FileProcessor
from app.models import AgentResponse

app = FastAPI(title="Agentic Document Assistant")
orchestrator = AgentOrchestrator()

@app.post("/process", response_model=AgentResponse)
async def process_request(
    query: str = Form(...),
    file: UploadFile = File(None)
):
    file_bytes = None
    file_type = None

    if file:
        file_bytes = await file.read()

        if "image" in file.content_type:
            file_type = "image"
        elif "pdf" in file.content_type:
            file_type = "pdf"
        elif "audio" in file.content_type:
            file_type = "audio"

    result = orchestrator.plan_and_execute(
        query=query,
        file_bytes=file_bytes,
        file_type=file_type
    )

    return AgentResponse(
        response_text=result.get("response") or "⚠️ No response generated.",
        action_taken=result.get("action", "unknown"),
        needs_clarification=result.get("needs_clarification", False)
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)