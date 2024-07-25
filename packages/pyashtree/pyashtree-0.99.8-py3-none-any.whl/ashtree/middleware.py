from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response
from mongey.cache.request_local import req_cache_ctx


class RequestLocalCacheMiddleware(BaseHTTPMiddleware):

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        req_cache = req_cache_ctx.set({})
        response = await call_next(request)
        req_cache_ctx.reset(req_cache)
        return response
