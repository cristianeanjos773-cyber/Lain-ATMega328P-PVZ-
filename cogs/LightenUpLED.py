from typing import TYPE_CHECKING
from discord.ext import commands 
from Engine import Bot

if TYPE_CHECKING:
    class USART_BOT(commands.Cog):
        async def USART_SEND(self, data: bytes) -> None: ... # this is just here to satisfy python strivt 
else:
    USART_BOT = commands.Cog

TURN_ON_LED_COMMAND: bytes = b'K'
TURN_OFF_LED_COMMAND: bytes = b'J'

class LightenUPLEDClass(commands.Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot: Bot = bot 

    @commands.command(name="LightenUPLED")
    async def LightenUpLED(self, ctx: commands.Context[Bot]):
        USART_COG = self.bot.get_cog("USART_BOT")
        
        if USART_COG:
            COG_SERIAL: USART_BOT = USART_COG # type: ignore
            print(TURN_ON_LED_COMMAND) 
            await COG_SERIAL.USART_SEND(TURN_ON_LED_COMMAND)

    @commands.command(name="TurnOFFLED")
    async def TurnOFFLED(self, ctx : commands.Context[Bot]):
            USART_COG = self.bot.get_cog("USART_BOT")
                
            if USART_COG:
                COG_SERIAL: USART_BOT = USART_COG # type: ignore
                print(TURN_ON_LED_COMMAND) 
                await COG_SERIAL.USART_SEND(TURN_OFF_LED_COMMAND)

                


async def setup(bot: Bot):
    await bot.add_cog(LightenUPLEDClass(bot))