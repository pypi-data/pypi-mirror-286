from typing import Dict, Mapping, Optional


class HttpRequest:
    method: str = "GET"
    url: str = "/"
    ver: str = "HTTP/1.1"
    urlkeys: Dict[str, str]
    queries: Dict[str, str]
    headers: Dict[str, str]
    cookies: Dict[str, str]
    body: bytes = b""

    def __init__(
        self,
        method: Optional[str] = None,
        url: Optional[str] = None,
        body: Optional[bytes] = None,
        urlkeys: Optional[Mapping[str, str]] = None,
        queries: Optional[Mapping[str, str]] = None,
        headers: Optional[Mapping[str, str]] = None,
        cookies: Optional[Mapping[str, str]] = None,
        ver: Optional[str] = None,
    ) -> None:
        self.method = method or self.method
        self.url = url or self.url
        self.ver = ver or self.ver
        self.urlkeys = urlkeys or {}
        self.queries = queries or {}
        self.headers = headers or {}
        self.cookies = cookies or {}
        self.body = body or self.body

    def encode(self) -> bytes:
        url = self.url
        queries = "&".join(f"{key}={value}" for key, value in self.queries.items())

        if queries:
            url += "?" + queries
        
        statusline = f"{self.method} {url} {self.ver}\r\n"
        headers = "".join(f"{key}: {value}\r\n" for key, value in self.headers.items())

        if self.cookies:
            headers += (
                "Cookie: "
                + "; ".join(f"{key}={value}" for key, value in self.cookies.items())
                + "\r\n"
            )

        return (statusline + headers + "\r\n").encode() + self.body

    @classmethod
    def from_bytes(cls, data: bytes) -> "HttpRequest":
        instance = cls()

        head, instance.body = data.split(b"\r\n\r\n", 1)
        request_line, *headers = head.decode().split("\r\n")

        instance.method, instance.url, instance.ver = request_line.split(" ", 2)

        if "?" in instance.url:
            instance.url, queries = instance.url.split("?", 1)

            for query in queries.split("&"):
                key, value = query.split("=", 1)
                instance.queries[key.strip()] = value.strip()

        for header in headers:
            key, value = header.split(":", 1)
            instance.headers[key.strip().title()] = value.strip()

        if "Cookie" in instance.headers:
            for cookie in instance.headers["Cookie"].split(";"):
                key, value = cookie.split("=", 1)
                instance.cookies[key.strip()] = value.strip()

            del instance.headers["Cookie"]

        return instance
