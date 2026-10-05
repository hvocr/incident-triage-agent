# Idea: Autonomous Incident Triage Agent

An AI agent investigates incidents by checking backend health and searching runbooks. If manual intervention is needed, escalation pauses for engineer approval; rejection must never execute the escalation. Paused investigations should survive restarts. Engineers use a REST API and simple web UI. The intended stack is Gemini, Supabase pgvector, LangGraph, FastAPI, Gradio, and Render.
