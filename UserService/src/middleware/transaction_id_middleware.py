import uuid
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from UserService.src.middleware.transaction_context import set_transaction_id

class TransactionIdMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        transaction_id = request.headers.get("X-Correlation-ID") or str(uuid.uuid4())
        
        # Save in context var
        set_transaction_id(transaction_id)
        
        # Make it available to response too
        response = await call_next(request)
        response.headers["X-Transaction-ID"] = transaction_id
        return response
    
# By adding the ID to response headers, we allow clients and downstream systems to trace requests end-to-end.