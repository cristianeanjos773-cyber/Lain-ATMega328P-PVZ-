from dataclasses import dataclass, field

@dataclass
class USART_PROPERTIES:
    SERIAL_PORT: str 
    BAUDRATE: int
    TIMEOUT: int  
    USART_HANDLERS: dict[bytes, function] = field(default_factory=dict) # type: ignore

@dataclass
class BotAttributes: 
    ChannelSendId: int

@dataclass
class JSONType:
    success: bool
    message: str
    origin: str
    payload: dict | None = None