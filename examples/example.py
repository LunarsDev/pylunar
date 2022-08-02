from pylunar import Client, endpoints
from aiohttp import ClientSession
import asyncio

token = ""  # Replace with your Lunar API Key.

async def main():
    async with ClientSession() as session:
        client = Client(session=session, token=token)
        image = await client.request(endpoints.generate_achievement, text="Woo! I made a request!")
        await image.save("image.jpg")

asyncio.run(main())