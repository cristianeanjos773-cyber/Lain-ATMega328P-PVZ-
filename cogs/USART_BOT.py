import serial 
import discord
from GLOBAL.GlobalTypes import USART_PROPERTIES 

from utils.LightNumberStatus import LightNumberStatus 
from discord.ext import commands, tasks

COMMUNICATION_SUCCESS: bytes = b'S'
COMMUNICATION_ERROR: bytes = b'E'
COMMUNICATION_NULL: bytes = b'N'

class USART_BOT(commands.Cog): 
    def __init__(self, bot: commands.Bot, USART_STATUS: USART_PROPERTIES) -> None:
        self.bot: commands.Bot = bot
        self.ConnectedPort: serial.Serial | None = None       
        self.USART_STATUS: USART_PROPERTIES = USART_STATUS

    async def SETUP_USART(self):
        UsartStatus = self.USART_STATUS 
        SERIAL_PORT = UsartStatus.SERIAL_PORT
        BAUDRATE = UsartStatus.BAUDRATE
        TIMEOUT = UsartStatus.TIMEOUT 

        self.Channel = await self.bot.fetch_channel(self.USART_STATUS.CHANNEL_SEND_ID)

        try:

            self.ConnectedPort = serial.Serial(port=SERIAL_PORT, baudrate=BAUDRATE, timeout=TIMEOUT)
            print(self.Channel, self.ConnectedPort)
            if not self.READ_LOOP.is_running():
               self.READ_LOOP.start()  
                
            if isinstance(self.Channel, discord.TextChannel):
                await self.Channel.send(f"```[LAIN SERIAL STATUS]: SUCCESS. Lain was able to connect to COM3 Serial PORT.```")

        except Exception as e:

            if isinstance(self.Channel, discord.TextChannel):
               await self.Channel.send(f"```[LAIN SERIAL STATUS]: FAILED! Was not able to connect\nREASON: {e}```")

    async def cog_load(self):
        await self.SETUP_USART()

    async def cog_unload(self):
        self.READ_LOOP.cancel()

        if self.ConnectedPort and self.ConnectedPort.is_open:
            self.ConnectedPort.close()

    
    async def USART_READ(self):

        ConnectedPort = self.ConnectedPort    

        if not ConnectedPort or ConnectedPort.in_waiting == 0:
            return

        FIRST_BYTE: bytes = ConnectedPort.read(1); """
            THIS will be the first byte coming to the discord bot, it is not an int or anything else, but a character. this character will determine
            if the next bytes are light status, temperature status, whatever. 
            this is needed to organize the python bot, so it can get ready to read an int or a value. 
        """

        print(FIRST_BYTE)

        if not FIRST_BYTE:
            await self.USART_SEND(COMMUNICATION_ERROR)
            return 

        #print(ConnectedPort.writable())
        #print(COMMUNICATION_SUCCESS)
        
        ConnectedPort.write(COMMUNICATION_SUCCESS) 

        if FIRST_BYTE == b'L':  
            LIGHT_BYTES: bytes = ConnectedPort.read(2)
            LIGHT_VALUE = int.from_bytes(LIGHT_BYTES, byteorder="big")
            LIGHT_STATUS: str = LightNumberStatus(LIGHT_VALUE) 

            if isinstance(self.Channel, discord.TextChannel):
                await self.Channel.send(f"```[LAIN SERIAL PORT]: CRIS'S ROOM NUMBER LIGHT STATUS Number:'{LIGHT_VALUE}', \n LIGHT STATUS: '{LIGHT_STATUS}'```")

        elif FIRST_BYTE == b'B':
            BUTTON_CHARACTER: str = FIRST_BYTE.decode('utf-8').strip() 


            if isinstance(self.Channel, discord.TextChannel):
                await self.Channel.send(f"```[LAIN SERIAL PORT]: byte RECEIVED: '{BUTTON_CHARACTER}' ```")    


    async def USART_SEND(self, MESSAGE: bytes):
            ConnectedPort = self.ConnectedPort 
    
            if not ConnectedPort or not ConnectedPort.writable():
                return 
    
            ConnectedPort.write(MESSAGE)            

            if isinstance(self.Channel, discord.TextChannel):
                await self.Channel.send(f"```[LAIN SERIAL PORT]: Lain sent BYTE: {MESSAGE} to ATMega328P!```")     


    @tasks.loop(seconds=0.5)
    async def READ_LOOP(self):
        await self.USART_READ()

    @READ_LOOP.before_loop
    async def BEFORE_READ_LOOP(self):
        await self.bot.wait_until_ready()

    
        

async def setup(bot: commands.Bot) -> None:
    USART_STATUS: USART_PROPERTIES = USART_PROPERTIES(
        SERIAL_PORT='COM3',
        BAUDRATE=9600, 
        CHANNEL_SEND_ID=1412280982253342781,  
        TIMEOUT=1,
    )

    await bot.add_cog(USART_BOT(bot, USART_STATUS)) 