from __future__ import annotations

from typing import Any, Callable, Generic, ParamSpec, Type, TypeVar

from aiohttp import ClientSession
from yarl import URL

from . import models

__all__ = "Client", "Endpoint", "ep"

BASE = "https://api.lunardev.group/"

T = TypeVar("T", bound=models.BaseModel)
P = ParamSpec("P")


class Endpoint(Generic[T, P]):
    def __init__(self, route: str, *, model: Type[T], fn: Callable[P, Any]):
        self.url = URL(BASE + route)
        self.model = model
        self.fn = fn

    async def request(
        self,
        session: ClientSession,
        headers: dict[str, str],
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> T:
        url = self.url.with_query(**kwargs) if kwargs else self.url
        resp = await session.get(url, headers=headers)
        return self.model(resp)


def ep(route: str, model: Type[T]):
    def inner(fn: Callable[P, Any]) -> Endpoint[T, P]:
        return Endpoint(route, model=model, fn=fn)

    return inner


class Client:
    def __init__(self, *, session: ClientSession, token: str):
        self._session = session
        self.__headers = {"Authorization": f"Bearer {token}"}

    async def request(
        self, endpoint: Endpoint[T, P], *args: P.args, **kwargs: P.kwargs
    ):
        res = await endpoint.request(self._session, self.__headers, *args, **kwargs)
        return res
