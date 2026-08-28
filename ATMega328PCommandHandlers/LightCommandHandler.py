import discord
import serial 

from utils.LightNumberStatus import LightNumberStatus 
from GLOBAL.GlobalTypes import JSONType 
from utils.SendDataToInternet import SendDataToInternet 

async def LightCommandHandler(FIRST_BYTE: bytes, Channel: int, ConnectedPort: serial.Serial | None) -> None:

    if not isinstance(ConnectedPort, serial.Serial):
        if isinstance(Channel, discord.TextChannel):
            await Channel.send(f"```[LAIN SERIAL PORT, LIGHT SENSOR FUNCTION]: CONNECTED PORT IS NOT A VALID SERIAL.SERIAL TYPE! type: '{type(ConnectedPort)}' ```") # if this happens, its because either connected port is broken or passed wrong arg
        return 
        
    LIGHT_BYTES = ConnectedPort.read(2)

    #print("LIGHT BYTES:", LIGHT_BYTES, "FIRST BYTE:", FIRST_BYTE)
        
    LIGHT_VALUE = int.from_bytes(LIGHT_BYTES, byteorder="big")
    LIGHT_STATUS: str = LightNumberStatus(LIGHT_VALUE)

    LightJSON: JSONType = JSONType(
        success=True, 
        message=LIGHT_STATUS, 
        origin="LainATMega328P",
        command="LIGHT_COMMAND", 
    )

    await SendDataToInternet(Channel=Channel, JSON=LightJSON)

    if isinstance(Channel, discord.TextChannel):
        await Channel.send(f"```[LAIN SERIAL PORT, LIGHT SENSOR]: CRIS'S ROOM NUMBER LIGHT STATUS Number:'{LIGHT_VALUE}',\nLIGHT STATUS: '{LIGHT_STATUS}'```")
