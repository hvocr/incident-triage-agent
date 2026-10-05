from agent import TriageAgent, InMemoryStateStore, route_tools, sensitive_calls

def test_route_checks_every_tool_call():
    calls = [{"id":"safe","name":"query_service_health","args":{"service":"auth"}},{"id":"sensitive","name":"escalate_ticket","args":{"ticket_title":"x","severity":"high"}}]
    assert route_tools(calls) == "sensitive_tools"; assert sensitive_calls(calls) == [calls[1]]
def test_pause_and_approve():
    agent = TriageAgent(store=InMemoryStateStore()); paused = agent.run("t1", "Auth is timing out. Escalate immediately."); assert paused["status"] == "AWAITING_APPROVAL"; resolved = agent.approve("t1"); assert resolved["status"] == "RESOLVED"; assert any("ticket_id" in m["content"] for m in resolved["messages"])
def test_rejection_answers_all_pending_calls():
    class MixedModel:
        def invoke(self, messages): return {"role":"assistant","content":"","tool_calls":[{"id":"a","name":"query_service_health","args":{"service":"auth"}},{"id":"b","name":"escalate_ticket","args":{"ticket_title":"x","severity":"high"}}]}
    agent = TriageAgent(model=MixedModel(), store=InMemoryStateStore()); agent.run("t2", "incident"); rejected = agent.reject("t2", "not authorized"); tool_messages = [m for m in rejected["messages"] if m["role"] == "tool"]; assert len(tool_messages) == 2; assert all("Rejected by engineer" in m["content"] for m in tool_messages)
