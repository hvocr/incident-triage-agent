from seed_rag import RUNBOOKS, seed
class Cursor:
    def __init__(self): self.rowcount = 1; self.calls = []
    def execute(self, sql, params): self.calls.append((sql, params))
class Connection:
    def __init__(self): self.cursor_instance = Cursor(); self.commits = 0
    def cursor(self):
        class Context:
            def __enter__(_self): return self.cursor_instance
            def __exit__(_self, *_args): return False
        return Context()
    def commit(self): self.commits += 1
def test_seed_uses_768_embeddings_and_conflict_guard():
    connection = Connection(); vectors = []
    def embed(content, **kwargs): vectors.append((content, kwargs)); return [0.1] * 768
    assert seed(connection, embed) == 3; assert len(vectors) == len(RUNBOOKS); assert all(item[1]["output_dimensionality"] == 768 for item in vectors); assert all("on conflict" in sql.lower() for sql, _ in connection.cursor_instance.calls)
