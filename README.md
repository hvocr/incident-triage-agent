# Autonomous Incident Triage Agent

A complete spec-driven incident triage workflow: runbook storage, safe triage, human approval, FastAPI/Gradio UI, routing hardening, and Render deployment metadata.

## Local setup

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
pytest -q
python app.py
```

API: `GET /healthz`, `POST /chat`, and `POST /approve`. The Gradio UI is mounted at `/`.

## Supabase and Gemini

Run `db/migrations/001_incident_docs.sql` in Supabase SQL Editor. Set `GEMINI_API_KEY` and `DATABASE_URL` as environment variables only. Run `python seed_rag.py` twice to verify idempotency.

## Render

Create a service from `render.yaml`, set root directory to the repository root, and provide the two secret environment variables.
