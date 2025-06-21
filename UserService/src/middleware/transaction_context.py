import contextvars

# Create a context var (thread-safe, async-safe)
_transaction_id_ctx_var = contextvars.ContextVar("transaction_id", default=None)

def set_transaction_id(transaction_id: str):
    _transaction_id_ctx_var.set(transaction_id)

def get_transaction_id() -> str:
    return _transaction_id_ctx_var.get()

# Why ContextVar?
# Unlike thread-local storage, contextvars works with async/await code, making it safe for FastAPI's concurrent request handling. 
# This ensures that each request’s correlation ID is isolated, even when many requests are handled concurrently.