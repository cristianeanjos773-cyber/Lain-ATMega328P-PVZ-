from dataclasses import dataclass, field
from discord.ext import commands 

@dataclass
class USART_PROPERTIES:
    SERIAL_PORT: str 
    BAUDRATE: int
    TIMEOUT: int  
    USART_HANDLERS: dict[bytes, function] = field(default_factory=dict) # type: ignore

@dataclass
class USART_BOT(commands.Cog):
    async def USART_SEND(self, data: bytes) -> None: ...  

@dataclass
class BotAttributes: 
    ChannelSendId: int

@dataclass
class JSONType:
    success: bool
    message: str
    origin: str
    payload: dict | None = None # type: ignore
    command: str | None = None