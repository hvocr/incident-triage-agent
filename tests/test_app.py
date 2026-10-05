from fastapi.testclient import TestClient
import app as app_module
def test_healthz_does_not_need_external_services():
    response = TestClient(app_module.app).get("/healthz"); assert response.status_code == 200; assert response.json() == {"status":"ok"}
def test_approve_without_pending_returns_400():
    response = TestClient(app_module.app).post("/approve", json={"thread_id":"missing","approved":True}); assert response.status_code == 400
