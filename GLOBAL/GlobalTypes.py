from dataclasses import dataclass


@dataclass
class USART_PROPERTIES:
    SERIAL_PORT: str 
    BAUDRATE: int
    CHANNEL_SEND_ID: int
    TIMEOUT: int  
