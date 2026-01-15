from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from main import app
import uuid


class AuditLogMiddleware(BaseHTTPMiddleware):
        def __init__(self, app):
            super().__init__(app)

        async def dispatch(self, request: Request, call_next):
              

            trace_id = request.headers.get("X-Trace-ID", str(uuid.uuid4()))
            request.state.trace_id = trace_id
            response = await call_next(request)

