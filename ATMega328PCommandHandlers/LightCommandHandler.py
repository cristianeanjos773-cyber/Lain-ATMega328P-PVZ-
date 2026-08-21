import discord
from utils.LightNumberStatus import LightNumberStatus 

async def LightCommandHandler(LIGHT_BYTES: bytes, Channel: int) -> None:

    LIGHT_VALUE = int.from_bytes(LIGHT_BYTES, byteorder="big")
    LIGHT_STATUS: str = LightNumberStatus(LIGHT_VALUE) 

    if isinstance(Channel, discord.TextChannel):
        await Channel.send(f"```[LAIN SERIAL PORT, LIGHT SENSOR]: CRIS'S ROOM NUMBER LIGHT STATUS Number:'{LIGHT_VALUE}',\nLIGHT STATUS: '{LIGHT_STATUS}'```")
