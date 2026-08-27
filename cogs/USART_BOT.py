import serial 
import discord
import asyncio 

from ATMega328PCommandHandlers.ButtonCommandHandler import ButtonCommandHandler
from ATMega328PCommandHandlers.LightCommandHandler import LightCommandHandler 

from GLOBAL.GlobalTypes import USART_PROPERTIES 
from discord.ext import commands, tasks
from typing import Any 

from Engine import Bot

COMMUNICATION_SUCCESS: bytes = b'S'
COMMUNICATION_ERROR: bytes = b'E'
COMMUNICATION_NULL: bytes = b'N'

LIGHT_COMMAND: bytes = b'L'
BUTTON_COMMAND: bytes = b'B'
RIGHT_NUMBER_MESSAGE: bytes = b'R'

#DISTANCE_SENSOR_COMMAND: bytes = b'D'  (dont wanna do it anymore, too stressful + breadboard doesnt have much space left)

class USART_BOT(commands.Cog): 

    def __init__(self, bot: Bot, USART_STATUS: USART_PROPERTIES) -> None:
        self.bot: Bot = bot
        self.ConnectedPort: serial.Serial | None = None       
        self.USART_STATUS: USART_PROPERTIES = USART_STATUS
        self.USART_HANDLERS: dict[bytes, Any] = self.USART_STATUS.USART_HANDLERS


    async def SETUP_USART(self):
        UsartStatus = self.USART_STATUS 
        SERIAL_PORT = UsartStatus.SERIAL_PORT
        BAUDRATE = UsartStatus.BAUDRATE
        TIMEOUT = UsartStatus.TIMEOUT 

        self.Channel = await self.bot.fetch_channel(self.bot.Config.ChannelSendId)

        try:

            self.ConnectedPort = serial.Serial(port=SERIAL_PORT, baudrate=BAUDRATE, timeout=TIMEOUT)
            print(self.Channel, self.ConnectedPort)

            if not self.READ_LOOP.is_running():
               self.READ_LOOP.start()  
                
            if isinstance(self.Channel, discord.TextChannel):
                await self.Channel.send(f"```[LAIN SERIAL STATUS]: SUCCESS. Lain was able to connect to COM3 Serial PORT.```")


        except Exception as error:

            if isinstance(self.Channel, discord.TextChannel):
               await self.Channel.send(f"```[LAIN SERIAL STATUS]: FAILED! Was not able to connect\nREASON: {error}```")

    async def cog_load(self):
        await self.SETUP_USART()

    async def cog_unload(self):
        self.READ_LOOP.cancel()

        if self.ConnectedPort and self.ConnectedPort.is_open:
            self.ConnectedPort.close()

    
    async def USART_READ(self) -> bytes | None:
        ConnectedPort = self.ConnectedPort    

        if not ConnectedPort or ConnectedPort.in_waiting == 0:
            return

        """
            THIS will be the first byte coming to the discord bot, it is not an int or anything else, but a character. this character will determine
            if the next bytes are light status, temperature status, whatever. 
            this is needed to organize the python bot, so it can get ready to read an int or a value. 
        """
        FIRST_BYTE: bytes = ConnectedPort.read(1); 

        #print(FIRST_BYTE)

        if not FIRST_BYTE:
            await self.USART_SEND(COMMUNICATION_ERROR)
            return 

        #print(ConnectedPort.writable())
        #print(COMMUNICATION_SUCCESS)
        
        ConnectedPort.write(COMMUNICATION_SUCCESS) 

        CommandHandler: callable = self.USART_HANDLERS.get(FIRST_BYTE) #type: ignore 

        if CommandHandler:
            await CommandHandler(FIRST_BYTE, self.Channel, self.ConnectedPort)
        #else:
            #pass
            #print("WE WERE NOT ABLKE TO FIND HANDLER", FIRST_BYTE)

        return FIRST_BYTE;

    async def NULL_RESPONSE_HANDLER(self, MESSAGE: bytes):

        # COMMENTARY WHEN I WAKE UP: change C to [SPECIFIC_LED > SPECIFIC_ FUNCTION] BECAUSE ITS OVER ENGIINEREINED

        Attempts = 0 
        MaxAttempts = 3

        while Attempts < MaxAttempts:
            ATMegaAnswer: bytes | None = await self.USART_READ() 

            if Attempts >= MaxAttempts:
                Attempts += 1
            else:
                if ATMegaAnswer == COMMUNICATION_ERROR or ATMegaAnswer == COMMUNICATION_NULL:
                    if isinstance(self.Channel, discord.TextChannel):
                        await self.Channel.send(f"```[LAIN SERIAL PORT]: FATAL ERROR! tried to send the same byte after 3 attempts and still failed. the wired is not in our hearts :( )```") #bla 
                        break 

            if ATMegaAnswer == COMMUNICATION_SUCCESS:
                if isinstance(self.Channel, discord.TextChannel):
                     await self.Channel.send(f"```[LAIN SERIAL PORT]: RETRY SUCCES! Lain sent BYTE: '{MESSAGE}', (Communication SUCCES!) to ATMega328P :) ```")
                     break

            await asyncio.sleep(2)



    async def USART_SEND(self, MESSAGE: bytes):
            ConnectedPort = self.ConnectedPort 
    
            if not ConnectedPort or not ConnectedPort.writable():
                return 

            if isinstance(self.Channel, discord.TextChannel):
                 await self.Channel.send(f"```[LAIN SERIAL PORT]: Lain tried to send BYTE: '{MESSAGE}' to ATMega328P!```")  

            ConnectedPort.reset_input_buffer()
            ConnectedPort.write(MESSAGE)            
            ATMegaAnswer: bytes | None = await self.USART_READ() 
                       
            if ATMegaAnswer is None:
                return ; 

            if ATMegaAnswer == COMMUNICATION_SUCCESS:
                if isinstance(self.Channel, discord.TextChannel):
                    await self.Channel.send(f"```[LAIN SERIAL PORT]: Lain sent BYTE: '{MESSAGE}', (Communication SUCCES!) to ATMega328P```")
                    return ; 
            
            if ATMegaAnswer == COMMUNICATION_NULL:
                if isinstance(self.Channel, discord.TextChannel):
                     await self.Channel.send(f"```[LAIN SERIAL PORT]: Lain sent BYTE: '{MESSAGE}', (Commnucation ERROR) to ATMega328P!```")  
                     await self.Channel.send(f" ```[LAIN SERIAL PORT]: Lain will retry to send the message until it gets success for a few seconds! hold on! ```")
                     await self.NULL_RESPONSE_HANDLER(MESSAGE) 

                 
                                         

    @tasks.loop(seconds=0.5)
    async def READ_LOOP(self):
        await self.USART_READ() 

    @READ_LOOP.before_loop
    async def BEFORE_READ_LOOP(self):
        await self.bot.wait_until_ready()

async def setup(bot: Bot) -> None:
    USART_STATUS: USART_PROPERTIES = USART_PROPERTIES(
        SERIAL_PORT='COM3',
        BAUDRATE=9600, 
        TIMEOUT=1,
        USART_HANDLERS = { #type: ignore 
            LIGHT_COMMAND: LightCommandHandler,
            BUTTON_COMMAND: ButtonCommandHandler, 
        }
    )

    await bot.add_cog(USART_BOT(bot, USART_STATUS)) 