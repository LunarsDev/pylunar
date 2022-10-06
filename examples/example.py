from lunarapi import Client, endpoints
from aiohttp import ClientSession
import asyncio

token = "fff"  # Replace with your Lunar API Key.

async def main():
    async with ClientSession() as session:
        client = Client(session=session, token=token)

        image = await client.request(endpoints.generate_achievement, text="Woo! I made a request!")
        await image.save("image.jpg")

        nsfw_jpg = await client.request(endpoints.nsfw("jpg"))
        data = await nsfw_jpg.to_dict()
        print("Image URL is", data["url"])

asyncio.run(main())
