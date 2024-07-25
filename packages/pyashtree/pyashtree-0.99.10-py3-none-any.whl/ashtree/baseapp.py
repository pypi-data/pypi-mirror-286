from fastapi import FastAPI
from contextlib import asynccontextmanager
from .middleware import RequestLocalCacheMiddleware


class BaseApp(FastAPI):

    def __init__(self, **kwargs):
        kwargs["lifespan"] = BaseApp._lifespan
        super().__init__(**kwargs)
        self.setup_routes()
        self.setup_middleware()

    @asynccontextmanager
    async def _lifespan(self):
        await self.on_startup()
        yield
        await self.on_shutdown()

    async def on_startup(self) -> None:
        pass

    async def on_shutdown(self) -> None:
        pass

    def setup_routes(self) -> None:
        pass

    def setup_middleware(self) -> None:
        self.add_middleware(RequestLocalCacheMiddleware)  # type: ignore

