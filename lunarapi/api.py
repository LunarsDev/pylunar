from __future__ import annotations
from typing import TYPE_CHECKING, Any, Callable, Dict, Generic, Literal, Type, TypeVar

from yarl import URL

if TYPE_CHECKING:
    from typing_extensions import ParamSpec
    from aiohttp import ClientSession
    from .models import BaseModel

if TYPE_CHECKING:
    P = ParamSpec('P')
else:
    P = TypeVar('P')

__all__ = "Client", "Endpoint", "ep"

BASE = "https://api.lunardev.group/"

ModalT = TypeVar("ModalT", bound="BaseModel")

class Endpoint(Generic[ModalT, P]):
    def __init__(self, route: str, *, model: Type[ModalT], fn: Callable[P, Any]) -> None:
        self.url: URL = URL(BASE + route)
        self.model: Type[ModalT] = model
        self.fn: Callable[P, Any] = fn

    async def request(
        self,
        session: ClientSession,
        headers: dict[str, str],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> ModalT:
        url = self.url.with_query(**kwargs) if kwargs else self.url
        resp = await session.get(url, headers=headers)
        return self.model(resp)

def ep(route: str, model: Type[ModalT]) -> Callable[[Callable[P, Any]], Endpoint[ModalT, P]]:
    def inner(fn: Callable[P, Any]) -> Endpoint[ModalT, P]:
        return Endpoint(route, model=model, fn=fn)

    return inner


class Client:
    def __init__(self, *, session: ClientSession, token: str) -> None:
        self._session: ClientSession = session
        self.__headers: Dict[Literal["Authorization"], str] = {"Authorization": f"Bearer {token}"}

    async def request(
        self, endpoint: Endpoint[ModalT, P], *args: P.args, **kwargs: P.kwargs
    ) -> ModalT:
        res = await endpoint.request(self._session, self.__headers, *args, **kwargs)
        return res
