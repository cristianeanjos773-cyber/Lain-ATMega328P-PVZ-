import discord

async def ButtonCommandHandler(BUTTON_BYTE: bytes, Channel: int) -> None:

    BUTTON_CHARACTER: str = BUTTON_BYTE.decode('utf-8').strip() 

    if isinstance(Channel, discord.TextChannel):
        await Channel.send(f"```[LAIN SERIAL PORT, BLUE BUTTON]: byte RECEIVED: '{BUTTON_CHARACTER}' FROM BLUE```")   