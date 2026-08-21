import discord
import serial 

async def ButtonCommandHandler(BUTTON_BYTE: bytes, Channel: int, ConnectedPort: serial.Serial) -> None:

    BUTTON_CHARACTER: str = BUTTON_BYTE.decode('utf-8').strip() 

    if isinstance(Channel, discord.TextChannel):
        await Channel.send(f"```[LAIN SERIAL PORT, BLUE BUTTON]: byte RECEIVED: '{BUTTON_CHARACTER}' FROM WHITE BUTTON!```")   