from __future__ import annotations
import uuid
from dataclasses import dataclass, field
from typing import Any, Callable, Protocol
SENSITIVE_TOOL = "escalate_ticket"
class Model(Protocol):
    def invoke(self, messages: list[dict[str, Any]]) -> dict[str, Any]: ...
class StateStore(Protocol):
    def load(self, thread_id: str) -> dict[str, Any] | None: ...
    def save(self, thread_id: str, state: dict[str, Any]) -> None: ...
@dataclass
class InMemoryStateStore:
    states: dict[str, dict[str, Any]] = field(default_factory=dict)
    def load(self, thread_id: str) -> dict[str, Any] | None:
        state = self.states.get(thread_id)
        return None if state is None else dict(state)
    def save(self, thread_id: str, state: dict[str, Any]) -> None: self.states[thread_id] = dict(state)
def query_service_health(service: str) -> dict[str, str]: return {"service": service, "status": "degraded" if service == "auth" else "healthy"}
def search_runbooks(query: str, service: str | None = None) -> list[dict[str, Any]]: return [{"content": f"Runbook match for {query}", "metadata": {"service": service or "general"}}]
def escalate_ticket(ticket_title: str, severity: str) -> dict[str, str]:
    if not ticket_title.strip() or not severity.strip(): raise ValueError("ticket_title and severity are required")
    return {"ticket_id": f"INC-{uuid.uuid4().hex[:8].upper()}", "title": ticket_title, "severity": severity}
SAFE_TOOLS: dict[str, Callable[..., Any]] = {"query_service_health": query_service_health, "search_runbooks": search_runbooks}
SENSITIVE_TOOLS: dict[str, Callable[..., Any]] = {SENSITIVE_TOOL: escalate_ticket}
def sensitive_calls(tool_calls: list[dict[str, Any]]) -> list[dict[str, Any]]: return [call for call in tool_calls if call.get("name") in SENSITIVE_TOOLS]
def route_tools(tool_calls: list[dict[str, Any]]) -> str: return "sensitive_tools" if sensitive_calls(tool_calls) else "safe_tools"
def _tool_message(call: dict[str, Any], content: Any) -> dict[str, Any]: return {"role": "tool", "tool_call_id": call.get("id", ""), "name": call.get("name", ""), "content": str(content)}
class TriageAgent:
    def __init__(self, model: Model | None = None, store: StateStore | None = None) -> None: self.model, self.store = model, store or InMemoryStateStore()
    def _model_call(self, messages: list[dict[str, Any]]) -> dict[str, Any]:
        if self.model is not None: return self.model.invoke(messages)
        text = messages[-1]["content"].lower(); calls = [{"id": "health-1", "name": "query_service_health", "args": {"service": "auth"}}]
        if "escalat" in text or "immediately" in text: calls.append({"id": "escalate-1", "name": SENSITIVE_TOOL, "args": {"ticket_title": "Incident escalation", "severity": "high"}})
        return {"role": "assistant", "content": "I investigated the incident.", "tool_calls": calls}
    def run(self, thread_id: str, message: str) -> dict[str, Any]:
        state = self.store.load(thread_id) or {"messages": []}; response = self._model_call(state["messages"] + [{"role": "user", "content": message}]); calls = response.get("tool_calls", [])
        if sensitive_calls(calls):
            state.update({"messages": state["messages"] + [{"role": "user", "content": message}, response], "pending_calls": calls, "status": "AWAITING_APPROVAL"}); self.store.save(thread_id, state); return {"status": "AWAITING_APPROVAL", "pending_action": sensitive_calls(calls), "messages": state["messages"]}
        result = self._execute_calls(calls); state.update({"messages": state["messages"] + [{"role": "user", "content": message}, response, *result], "status": "COMPLETED"}); self.store.save(thread_id, state); return {"status": "COMPLETED", "messages": state["messages"]}
    def approve(self, thread_id: str) -> dict[str, Any]:
        state = self.store.load(thread_id)
        if not state or state.get("status") != "AWAITING_APPROVAL": raise LookupError("no pending approval for thread")
        result = self._execute_calls(state["pending_calls"]); state.update({"messages": state["messages"] + result, "pending_calls": [], "status": "RESOLVED"}); self.store.save(thread_id, state); return {"status": "RESOLVED", "messages": state["messages"]}
    def reject(self, thread_id: str, reason: str) -> dict[str, Any]:
        state = self.store.load(thread_id)
        if not state or state.get("status") != "AWAITING_APPROVAL": raise LookupError("no pending approval for thread")
        result = [_tool_message(call, f"Rejected by engineer: {reason}") for call in state["pending_calls"]]; state.update({"messages": state["messages"] + result, "pending_calls": [], "status": "REJECTED"}); self.store.save(thread_id, state); return {"status": "REJECTED", "messages": state["messages"]}
    def _execute_calls(self, calls: list[dict[str, Any]]) -> list[dict[str, Any]]:
        messages = []
        for call in calls:
            fn = {**SAFE_TOOLS, **SENSITIVE_TOOLS}.get(call.get("name")); messages.append(_tool_message(call, fn(**call.get("args", {})) if fn else f"Unknown tool: {call.get('name')}"))
        return messages
def build_agent() -> TriageAgent: return TriageAgent()
