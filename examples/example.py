from lunarapi import Client, endpoints
from aiohttp import ClientSession
import asyncio

token = "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE2NjU0MzIyMzcsIm5iZiI6MTY2NTQzMjIzNywianRpIjoiY2M3YjUwMTMtYmIwMi00YzZjLTlhZTctNzk3YzI1NzNlYmRlIiwiaWRlbnRpdHkiOiJ3aW50ZXIiLCJmcmVzaCI6ZmFsc2UsInR5cGUiOiJhY2Nlc3MifQ.ALmwRaObiu0w9EFSPSoPlZS72Ehrd1NQdFj6knXsSws"  # Replace with your Lunar API Key.

async def main():
    async with ClientSession() as session:
        client = Client(session=session, token=token)

        # image = await client.request(endpoints.generate_achievement, text="Woo! I made a request!")
        # await image.save("image.jpg")

        nsfw_jpg = await client.request(endpoints.nsfw("jpg"))
        data = await nsfw_jpg.to_dict()
        print("Image URL is", data["url"])

asyncio.run(main())
