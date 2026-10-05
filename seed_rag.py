from __future__ import annotations
import os
from typing import Any
RUNBOOKS = [("Auth service 504 timeouts: check upstream saturation and restart the unhealthy worker.", "auth"), ("Database high latency: inspect slow queries, locks, and connection pool saturation.", "database"), ("Payment gateway failures: verify provider status, retry policy, and idempotency keys.", "payments")]
def seed(connection: Any, embed: Any) -> int:
    inserted = 0
    from psycopg.types.json import Jsonb
    with connection.cursor() as cursor:
        for content, service in RUNBOOKS:
            vector = embed(content, task_type="RETRIEVAL_DOCUMENT", output_dimensionality=768)
            cursor.execute("insert into incident_docs(content, metadata, embedding) values (%s, %s, %s) on conflict (content_hash) do nothing", (content, Jsonb({"service": service}), vector)); inserted += cursor.rowcount
    connection.commit(); return inserted
def main() -> None:
    from dotenv import load_dotenv
    load_dotenv()
    if not os.getenv("DATABASE_URL") or not os.getenv("GEMINI_API_KEY"): raise RuntimeError("DATABASE_URL and GEMINI_API_KEY must be set before seeding")
    import psycopg
    from langchain_google_genai import GoogleGenerativeAIEmbeddings
    embeddings = GoogleGenerativeAIEmbeddings(model=os.getenv("GEMINI_EMBEDDING_MODEL", "gemini-embedding-001"), output_dimensionality=768, google_api_key=os.environ["GEMINI_API_KEY"])
    with psycopg.connect(os.environ["DATABASE_URL"], prepare_threshold=None) as connection: seed(connection, embeddings.embed_query)
if __name__ == "__main__": main()
