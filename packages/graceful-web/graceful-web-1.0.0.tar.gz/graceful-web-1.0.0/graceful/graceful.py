import json
import socket
import asyncio
import mimetypes
from typing import Any, Callable, Coroutine, Dict, List, Optional, Tuple, Type

from graceful.request import HttpRequest
from graceful.response import HttpResponse, HttpException
from graceful.template import Template


class Graceful:
    websocket: Callable[[socket.socket, Tuple[str, int]], None]
    middleware: Callable[[HttpRequest, Callable[[HttpRequest], Coroutine]], Coroutine]

    ver = "1.0.0"
    default_host: str = "localhost"
    default_port: int = 8080
    bufsize: int = 1024
    timeout: float = 180

    active: bool = True

    host: str
    port: int
    applications: Dict[str, List[Dict]]
    exceptions: Dict[int, Callable]

    def __init__(
        self,
        host: str = default_host,
        port: int = default_port,
        websocket: Optional[Callable] = None,
        middleware: Optional[Callable] = None,
    ) -> None:
        self.websocket = websocket or self.serve_response
        self.middleware = middleware or self.middleware

        self.host = host
        self.port = port
        self.applications = {}
        self.exceptions = {}

    async def middleware(self, request: HttpRequest, fetch: Coroutine) -> None:
        return await fetch(request)

    async def handle_request(
        self, request: HttpRequest, response: HttpResponse, action: Callable
    ) -> Any:
        kwargs = {
            key: item
            for key, item in Template.cast(
                {"request": request, "body": request.body, "response": response}
                | request.urlkeys
                | request.queries
                | request.headers
                | request.cookies,
                action.__annotations__,
            ).items()
            if key in action.__code__.co_varnames[: action.__code__.co_argcount]
        }

        return (
            await action(**kwargs)
            if asyncio.iscoroutinefunction(action)
            else action(**kwargs)
        )

    async def handle_response(self, response: HttpResponse, result: Any) -> bytes:
        if result is None:
            return response.encode()

        elif isinstance(result, HttpResponse):
            return result.encode()

        if isinstance(result, (set, tuple, list, dict)):
            response.headers.setdefault("Content-Type", "application/json")
            result = json.dumps(self.body)

        elif "text/x-file" == response.headers.get("Content-Type", "").lower():
            try:
                with open(result, "rb") as file:
                    mimetype, charset = mimetypes.guess_type(result)
                    response.headers["Content-Type"] = f"{mimetype}; {charset}"
                    result = asyncio.get_event_loop().run_in_executor(None, file.read)

            except FileNotFoundError as e:
                raise HttpException(status=404) from e

        if hasattr(result, "__str__"):
            result = str(result).encode()

        elif hasattr(result, "encode"):
            result = result.encode()

        if isinstance(result, bytes):
            response.body = result

        return response.encode()

    async def fetch_request(self, conn: socket.socket) -> HttpRequest:
        loop = asyncio.get_event_loop()
        data = b""

        try:
            while True:
                data += await asyncio.wait_for(
                    loop.sock_recv(conn, self.bufsize), self.timeout
                )

                if b"\r\n\r\n" in data:
                    break

            request = HttpRequest.from_bytes(data)
            length = int(request.headers.get("Content-Length", 0))

            while length > 0:
                chunk = await asyncio.wait_for(
                    loop.sock_recv(conn, min(self.bufsize, length)), self.timeout
                )

                if chunk:
                    request.body += chunk
                    length -= len(chunk)

                else:
                    raise HttpException(status=400)

            return request

        except TimeoutError as e:
            raise HttpException(status=408) from e

    async def fetch_response(
        self, request: HttpRequest
    ) -> Tuple[HttpResponse, Callable]:
        req_dirs = request.url.strip("/").split("/")

        for app in self.applications.get(request.method, tuple()):
            app_dirs = app["url"].split("/")

            if len(req_dirs) < len(app_dirs):
                continue

            for i, (req_dir, app_dir) in enumerate(zip(req_dirs, app_dirs)):
                if app_dir.startswith("{") and app_dir.endswith("}"):
                    key, *exts = app_dir.strip("{}").split(":")

                    if len(req_dirs[i:]) < len(exts):
                        break

                    if key:
                        request.urlkeys[key] = req_dir

                    for s, ext in enumerate(exts, i):
                        request.urlkeys[ext] = "/".join(req_dirs[s:])

                elif app_dir != req_dir:
                    break

            else:
                return app["response"](*app["args"], **app["kwargs"]), app["action"]

            request.urlkeys.clear()

        raise HttpException(status=404)

    async def fetch_exception(self, e: Exception) -> Tuple[HttpException, Callable]:
        if not isinstance(e, HttpException):
            e = HttpException(status=500)

        return e, self.exceptions.get(e.status, lambda: None)

    async def serve_request(self) -> None:
        loop = asyncio.get_event_loop()

        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setblocking(False)
        server.bind((self.host, self.port))
        server.listen()

        while self.active:
            await loop.create_task(self.websocket(*await loop.sock_accept(server)))

        server.close()
        loop.close()

    async def serve_response(self, conn: socket.socket, addr: Tuple[str, int]) -> None:
        with conn:
            try:
                request = await self.fetch_request(conn)
                response, action = await self.middleware(request, self.fetch_response)
                result = await self.handle_request(request, response, action)
                data = await self.handle_response(response, result)

            except Exception as e:
                response, action = await self.fetch_exception(e)
                result = await self.handle_request(request, response, action)
                data = await self.handle_response(response, result)

            print(
                f"[graceful {self.ver}] [{addr[0]}] '{request.method} {request.url} {request.ver}' {response.status} {addr[1]}"
            )

            await asyncio.get_event_loop().sock_sendall(conn, data)

    def run(self) -> None:
        print(
            f"[graceful {self.ver}] Hello from the graceful community! http://{self.host}:{self.port}/"
        )

        asyncio.run(self.serve_request())

    def route(
        self,
        method: str,
        url: str,
        response: Optional[Type[HttpResponse]] = None,
        *args: Any,
        **kwargs: Any,
    ) -> Callable:
        if method not in self.applications:
            self.applications[method] = []

        def routing(action: Callable):
            self.applications[method].append(
                {
                    "url": url.strip("/"),
                    "action": action,
                    "response": response or HttpResponse,
                    "args": args,
                    "kwargs": kwargs,
                }
            )

        return routing

    def get(
        self,
        url: str,
        response: Optional[Type[HttpResponse]] = None,
        *args: Any,
        **kwargs: Any,
    ):
        return self.route("GET", url, response, *args, **kwargs)

    def post(
        self,
        url: str,
        response: Optional[Type[HttpResponse]] = None,
        *args: Any,
        **kwargs: Any,
    ):
        return self.route("POST", url, response, *args, **kwargs)

    def put(
        self,
        url: str,
        response: Optional[Type[HttpResponse]] = None,
        *args: Any,
        **kwargs: Any,
    ):
        return self.route("PUT", url, response, *args, **kwargs)

    def delete(
        self,
        url: str,
        response: Optional[Type[HttpResponse]] = None,
        *args: Any,
        **kwargs: Any,
    ):
        return self.route("DELETE", url, response, *args, **kwargs)

    def head(
        self,
        url: str,
        response: Optional[Type[HttpResponse]] = None,
        *args: Any,
        **kwargs: Any,
    ):
        return self.route("HEAD", url, response, *args, **kwargs)

    def connect(
        self,
        url: str,
        response: Optional[Type[HttpResponse]] = None,
        *args: Any,
        **kwargs: Any,
    ):
        return self.route("CONNECT", url, response, *args, **kwargs)

    def options(
        self,
        url: str,
        response: Optional[Type[HttpResponse]] = None,
        *args: Any,
        **kwargs: Any,
    ):
        return self.route("OPTIONS", url, response, *args, **kwargs)

    def trace(
        self,
        url: str,
        response: Optional[Type[HttpResponse]] = None,
        *args: Any,
        **kwargs: Any,
    ):
        return self.route("TRACE", url, response, *args, **kwargs)

    def patch(
        self,
        url: str,
        response: Optional[Type[HttpResponse]] = None,
        *args: Any,
        **kwargs: Any,
    ):
        return self.route("PATCH", url, response, *args, **kwargs)

    def exception(self, status: int) -> Callable:
        def routing(action: Callable):
            self.exceptions[status] = action

        return routing
