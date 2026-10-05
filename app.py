from __future__ import annotations
import os
from typing import Any
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from agent import TriageAgent, build_agent
agent: TriageAgent = build_agent()
class ChatRequest(BaseModel):
    thread_id: str = Field(min_length=1)
    message: str = Field(min_length=1)
class ApprovalRequest(BaseModel):
    thread_id: str = Field(min_length=1)
    approved: bool
    rejection_reason: str | None = None
def healthz() -> dict[str, str]: return {"status": "ok"}
def chat(request: ChatRequest) -> dict[str, Any]: return agent.run(request.thread_id, request.message)
def approve(request: ApprovalRequest) -> dict[str, Any]:
    try: return agent.approve(request.thread_id) if request.approved else agent.reject(request.thread_id, request.rejection_reason or "No reason provided")
    except LookupError as exc: raise HTTPException(status_code=400, detail=str(exc)) from exc
def create_ui() -> Any:
    import gradio as gr
    with gr.Blocks(title="Incident Triage") as ui:
        thread = gr.Textbox(label="Thread ID", value="demo-thread"); incident = gr.Textbox(label="Incident Description"); state = gr.Label(label="Workflow State"); log = gr.Markdown(label="Agent Log"); reason = gr.Textbox(label="Rejection Reason"); trigger = gr.Button("Trigger Triage"); approve_button = gr.Button("Approve Escalation"); reject_button = gr.Button("Reject Action")
        def run_ui(thread_id: str, text: str) -> tuple[dict[str, str], str]:
            result = agent.run(thread_id, text); return {result["status"]: 1}, str(result["messages"][-1:])
        trigger.click(run_ui, [thread, incident], [state, log]); approve_button.click(lambda t: agent.approve(t), [thread], [state, log]); reject_button.click(lambda t, r: agent.reject(t, r), [thread, reason], [state, log])
    return ui
def create_app() -> FastAPI:
    api = FastAPI(title="Autonomous Incident Triage Agent"); api.add_api_route("/healthz", healthz, methods=["GET"]); api.add_api_route("/chat", chat, methods=["POST"]); api.add_api_route("/approve", approve, methods=["POST"])
    try:
        import gradio as gr; return gr.mount_gradio_app(api, create_ui(), path="/")
    except ImportError: return api
app = create_app()
if __name__ == "__main__":
    import uvicorn; uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", "7860")))
