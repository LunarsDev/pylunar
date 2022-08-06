from io import BytesIO
import aiohttp

class BaseModel:
    def __init__(self, response: aiohttp.ClientResponse):
        self.response = response


class Image(BaseModel):
    async def bytes(self):
        return await self.response.read()
    
    async def file(self, discord):  # sourcery skip: avoid-builtin-shadow
        b = await self.response.read()
        return discord.File(BytesIO(b), "image.png")

    async def save(self, fp: str):
        with open(fp, "wb") as f:
            f.write(await self.bytes())

class JSON(BaseModel):
    async def to_dict(self):
        return await self.response.json()
