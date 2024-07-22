from datetime import datetime, timedelta
from typing import Literal, Optional, Union

class Cookie:
    _expires: Optional[datetime] = None

    name: str
    value: str = ""
    max_age: Optional[int]
    domain: Optional[str]
    path: Optional[str]
    secure: bool
    httponly: bool
    samesite: Optional[Literal["lax", "strict", "None"]]

    def __init__(
        self,
        name: str,
        value: Optional[str] = None,
        expires: Union[datetime, str, int, None] = None,
        max_age: Optional[int] = None,
        domain: Optional[str] = None,
        path: Optional[str] = None,
        secure: bool = False,
        httponly: bool = False,
        samesite: Optional[Literal["lax", "strict", "None"]] = None,
    ) -> None:
        self.name = name
        self.value = value or ""
        self.expires = expires
        self.max_age = max_age
        self.domain = domain
        self.path = path
        self.secure = secure
        self.httponly = httponly
        self.samesite = samesite

    def __str__(self) -> str:
        cookie_str = f"{self.name}={self.value}"

        if self._expires:
            expires = self._expires.strftime("%a, %d %b %Y %H:%M:%S GMT")
            cookie_str += f"; Expires={expires}"

        if self.max_age is not None:
            cookie_str += f"; Max-Age={self.max_age}"

        if self.domain:
            cookie_str += f"; Domain={self.domain}"

        if self.path:
            cookie_str += f"; Path={self.path}"

        if self.secure:
            cookie_str += "; Secure"

        if self.httponly:
            cookie_str += "; HttpOnly"

        if self.samesite:
            cookie_str += f"; SameSite={self.samesite.capitalize()}"

        return cookie_str

    @property
    def expires(self) -> Optional[datetime]:
        return self._expires
    
    @expires.setter
    def expires(self, value: Union[datetime, str, int, None]) -> None:
        if isinstance(value, datetime):
            self._expires = value

        elif isinstance(value, str):
            self._expires = datetime.fromisoformat(value)

        elif isinstance(value, int):
            self._expires = datetime.now() + timedelta(seconds=value)

        else:
            self._expires = None
