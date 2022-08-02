import aiohttp


class BaseModel:
    def __init__(self, response: aiohttp.ClientResponse):
        self.response = response


class Image(BaseModel):
    async def bytes(self):
        return await self.response.read()


class JSON(BaseModel):
    async def to_dict(self):
        return await self.response.json()
