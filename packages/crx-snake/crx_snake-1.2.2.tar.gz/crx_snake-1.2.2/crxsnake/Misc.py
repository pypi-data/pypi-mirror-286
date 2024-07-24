from datetime import datetime
from disnake import Embed, Color

red = Color.from_rgb(255, 0, 0)
green = Color.from_rgb(0, 255, 0)
blue = Color.from_rgb(0, 0, 255)
yellow = Color.from_rgb(255, 255, 0)
purple= Color.from_rgb(139,0,255)
trans = Color.from_rgb(43, 45, 49)


async def get_unix_time():
    return int(datetime.now().timestamp())

async def create_embed(title, description, color=trans):
    return Embed(title=title, description=description, color=color)
