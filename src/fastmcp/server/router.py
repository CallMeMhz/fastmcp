from collections.abc import Awaitable, Callable

from starlette.requests import Request
from starlette.responses import Response
from starlette.routing import BaseRoute, Route, WebSocketRoute
from starlette.websockets import WebSocket


class APIRouter:
    def __init__(self, prefix: str):
        self.prefix = prefix
        self.routes = []

    def custom_route(
        self,
        path: str,
        methods: list[str],
        name: str | None = None,
        include_in_schema: bool = True,
    ):
        def decorator(
            func: Callable[[Request], Awaitable[Response]],
        ) -> Callable[[Request], Awaitable[Response]]:
            self.routes.append(
                Route(
                    self._normalize_path(path),
                    endpoint=func,
                    methods=methods,
                    name=name,
                    include_in_schema=include_in_schema,
                )
            )
            return func

        return decorator

    def custom_ws_route(
        self,
        path: str,
        name: str | None = None,
    ):
        """
        Decorator to register a custom WebSocket route on the FastMCP server.

        Args:
            path: URL path for the WebSocket route (e.g., "/ws")
            name: Optional name for the route

        Example:
            @server.custom_websocket("/ws")
            async def websocket_endpoint(websocket: WebSocket):
                await websocket.accept()
                while True:
                    data = await websocket.receive_text()
                    await websocket.send_text(f"Echo: {data}")
        """

        def decorator(
            func: Callable[[WebSocket], Awaitable[None]],
        ) -> Callable[[WebSocket], Awaitable[None]]:
            self.routes.append(
                WebSocketRoute(
                    self._normalize_path(path),
                    endpoint=func,
                    name=name,
                )
            )
            return func

        return decorator

    def get_routes(self) -> list[BaseRoute]:
        return self.routes

    def _normalize_path(self, path: str) -> str:
        if self.prefix:
            if not self.prefix.startswith("/"):
                self.prefix = "/" + self.prefix
            if self.prefix.endswith("/"):
                self.prefix = self.prefix[:-1]
            path = self.prefix + path

        if not path.startswith("/"):
            path = "/" + path

        if path != "/" and path.endswith("/"):
            path = path[:-1]

        return path
    