import serial 
import discord
from GLOBAL.GlobalTypes import USART_PROPERTIES 
from discord.ext import commands 

class USART_BOT(commands.Cog): 
    def __init__(self, bot: commands.Bot, USART_STATUS: USART_PROPERTIES) -> None:
        self.bot: commands.Bot = bot
        self.ConnectedPort: serial.Serial | None = None       
        self.USART_STATUS: USART_PROPERTIES = USART_STATUS

    async def SETUP_USART(self):
        channel = self.bot.get_channel(self.USART_STATUS.CHANNEL_SEND_ID)

        try:

            UsartStatus = self.USART_STATUS 
            SERIAL_PORT = UsartStatus.SERIAL_PORT
            BAUDRATE = UsartStatus.BAUDRATE
            TIMEOUT = UsartStatus.TIMEOUT 

            self.ConnectedPort = serial.Serial(port=SERIAL_PORT, baudrate=BAUDRATE, timeout=TIMEOUT)

            if isinstance(channel, discord.TextChannel):
                await channel.send(f"LAIN SERIAL STATUS: SUCCESS. Lain was able to connect to COM3 Serial PORT.")
                         
        except Exception as e:
            if isinstance(channel, discord.TextChannel):
               await channel.send(f"LAIN SERIAL STATUS: FAILED! Was not able to connect\n REASON: {e}")


 
async def setup(bot: commands.Bot) -> None:
    USART_STATUS: USART_PROPERTIES = USART_PROPERTIES(
        SERIAL_PORT='COM3',
        BAUDRATE=9600, 
        CHANNEL_SEND_ID=1411887431254413384,  
        TIMEOUT=5,
    )
    await bot.add_cog(USART_BOT(bot, USART_STATUS)) 