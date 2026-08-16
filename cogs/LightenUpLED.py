from typing import TYPE_CHECKING
from discord.ext import commands 

if TYPE_CHECKING:
    class USART_BOT(commands.Cog):
        async def USART_SEND(self, data: bytes) -> None: ... # this is just here to satisfy python strivt 
else:
    USART_BOT = commands.Cog

LED_COMMAND: bytes = b'K'

class LightenUPLEDClass(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot: commands.Bot = bot 

    @commands.command(name="LightenUPLED")
    async def LightenUpLED(self, ctx: commands.Context[commands.Bot]):
        USART_COG = self.bot.get_cog("USART_BOT")

        if USART_COG:
            COG_SERIAL: USART_BOT = USART_COG # type: ignore 
            await COG_SERIAL.USART_SEND(LED_COMMAND)

async def setup(bot: commands.Bot):
    await bot.add_cog(LightenUPLEDClass(bot))