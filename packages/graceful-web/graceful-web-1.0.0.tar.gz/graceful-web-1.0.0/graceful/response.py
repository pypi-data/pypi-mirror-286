from datetime import datetime
from typing import Any, Dict, Literal, Mapping, Optional, Sequence, Union

from graceful.cookie import Cookie


class HttpResponse:
    _status: int = 200
    _reason: str = "OK"
    _reason_default: bool = True
    _cookies: Dict[str, Cookie] = {}

    ver: str = "HTTP/1.1"
    headers: Dict[str, str] = {}
    body: bytes = b""

    statuses = {
        100: "Continue",
        101: "Switching Protocols",
        102: "Processing",
        103: "Early Hints",
        200: "OK",
        201: "Created",
        202: "Accepted",
        203: "Non-Authoritative Information",
        204: "No Content",
        205: "Reset Content",
        206: "Partial Content",
        207: "Multi-Status",
        208: "Already Reported",
        226: "IM Used",
        300: "Multiple Choices",
        301: "Moved Permanently",
        302: "Found",
        303: "See Other",
        304: "Not Modified",
        305: "Use Proxy",
        307: "Temporary Redirect",
        308: "Permanent Redirect",
        400: "Bad Request",
        401: "Unauthorized",
        402: "Payment Required",
        403: "Forbidden",
        404: "Not Found",
        405: "Method Not Allowed",
        406: "Not Acceptable",
        407: "Proxy Authentication Required",
        408: "Request Timeout",
        409: "Conflict",
        410: "Gone",
        411: "Length Required",
        412: "Precondition Failed",
        413: "Payload Too Large",
        414: "URI Too Long",
        415: "Unsupported Media Type",
        416: "Range Not Satisfiable",
        417: "Expectation Failed",
        418: "I'm a Teapot",
        421: "Misdirected Request",
        422: "Unprocessable Entity",
        423: "Locked",
        424: "Failed Dependency",
        425: "Too Early",
        426: "Upgrade Required",
        428: "Precondition Required",
        429: "Too Many Requests",
        431: "Request Header Fields Too Large",
        451: "Unavailable For Legal Reasons",
        500: "Internal Server Error",
        501: "Not Implemented",
        502: "Bad Gateway",
        503: "Service Unavailable",
        504: "Gateway Timeout",
        505: "HTTP Version Not Supported",
        506: "Variant Also Negotiates",
        507: "Insufficient Storage",
        508: "Loop Detected",
        510: "Not Extended",
        511: "Network Authentication Required",
    }

    def __init__(
        self,
        body: Optional[bytes] = None,
        headers: Optional[Mapping[str, str]] = None,
        status: Optional[int] = None,
        reason: Optional[str] = None,
        ver: Optional[str] = None,
    ) -> None:
        self.ver = ver or self.ver
        self.body = body or self.body

        if headers:
            self.headers = headers

        if status:
            self.status = status

        if reason:
            self.reason = reason

    @property
    def status(self) -> int:
        return self._status

    @status.setter
    def status(self, value: int) -> None:
        self._status = value

        if self._reason_default:
            self._reason = self.statuses.get(self._status, self._reason)

    @property
    def reason(self) -> str:
        return self._reason

    @reason.setter
    def reason(self, value: str) -> None:
        self._reason = value
        self._reason_default = self._reason == self.statuses.get(self._status)

    def get_cookie(self, name: str) -> Cookie:
        return self._cookies[name]

    def set_cookie(
        self,
        name: str,
        value: Optional[str] = None,
        expires: Union[datetime, str, int, None] = None,
        max_age: Optional[int] = None,
        domain: Optional[str] = None,
        path: Optional[str] = None,
        secure: Optional[bool] = None,
        httponly: Optional[bool] = None,
        samesite: Optional[Literal["lax", "strict", "None"]] = None,
    ) -> None:
        if name in self._cookies:
            cookie = self._cookies[name]
        else:
            cookie = Cookie(name)
            self._cookies[name] = cookie

        if value:
            cookie.value = value

        if expires:
            cookie.expires = expires

        if max_age:
            cookie.max_age = max_age

        if domain:
            cookie.domain = domain

        if path:
            cookie.path = path

        if secure:
            cookie.secure = secure

        if httponly:
            cookie.httponly = httponly

        if samesite:
            cookie.samesite = samesite

    def delete_cookie(
        self,
        name: str,
        expires: bool = False,
        max_age: bool = False,
        domain: bool = False,
        path: bool = False,
        secure: bool = False,
        httponly: bool = False,
        samesite: bool = False,
    ) -> None:
        if not any([expires, max_age, domain, path, secure, httponly, samesite]):
            if name in self._cookies:
                del self._cookies[name]
            return

        if name in self._cookies:
            cookie = self._cookies[name]

            if expires:
                cookie.expires = None

            if max_age:
                cookie.max_age = None

            if domain:
                cookie.domain = None

            if path:
                cookie.path = "/"

            if secure:
                cookie.secure = False

            if httponly:
                cookie.httponly = False

            if samesite:
                cookie.samesite = None

    def encode(self) -> bytes:
        statusline = f"{self.ver} {self.status} {self.reason}\r\n"
        headers = "".join(
            f"{key.title()}: {item}\r\n" for key, item in self.headers.items()
        )
        cookies = "".join(
            f"Set-Cookie: {cookie}\r\n" for cookie in self._cookies.values()
        )

        return (statusline + headers + cookies + "\r\n").encode() + self.body

    @classmethod
    def from_bytes(cls, data: bytes) -> "HttpResponse":
        instance = cls()

        head, instance.body = data.split(b"\r\n\r\n", 1)
        response_line, *headers = head.decode().split("\r\n")

        instance.ver, status, instance.reason = response_line.split(" ", 2)
        instance.status = int(status)

        for header in headers:
            key, value = header.split(":", 1)
            key = key.strip().title()
            value = value.strip()

            if key == "Set-Cookie":
                cookie = {}

                pair, *attrs = value.split(";")
                cookie_name, cookie_value = pair.split("=", 1)
                cookie["name"] = cookie_name.strip()
                cookie["value"] = cookie_value.strip()

                for attr in attrs:
                    attr_key, *attr_value = attr.split("=", 1)
                    cookie[attr_key.strip().lower().replace("-", "_")] = (
                        attr_value[0].strip() if attr_value else True
                    )

                instance.set_cookie(**cookie)

            else:
                instance.headers[key] = value

        return instance


class HttpException(HttpResponse, Exception): ...
