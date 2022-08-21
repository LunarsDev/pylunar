from __future__ import annotations
from typing import TYPE_CHECKING, Any

from io import BytesIO
import aiohttp

if TYPE_CHECKING:
    from typing import Callable, Protocol, Union

    from aiohttp import ClientResponse

    class DiscordT(Protocol):
        File: Callable[[Union[BytesIO, Any], str], Any]
else:
    DiscordT: Any
class BaseModel:
    def __init__(self, response: ClientResponse) -> None:
        self.response: ClientResponse = response


class Image(BaseModel):
    async def bytes(self) -> bytes:
        return await self.response.read()
    
    async def file(self, module: DiscordT):  # sourcery skip: avoid-builtin-shadow
        b = await self.response.read()
        return module.File(BytesIO(b), "image.png")

    async def save(self, fp: str) -> None:
        with open(fp, "wb") as f:
            f.write(await self.bytes())

class JSON(BaseModel):
    async def to_dict(self) -> dict[Any, Any]:
        return await self.response.json()
