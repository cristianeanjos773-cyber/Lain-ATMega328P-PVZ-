from discord.ext import commands 
from Command_Bytes_sent import LED_COMMANDS   
from GLOBAL.GlobalTypes import USART_BOT
from Engine import Bot



class LightenUPLEDClass(commands.Cog):

    def __init__(self, bot: Bot) -> None:
        self.bot: Bot = bot 

    @commands.command(name="LightenUPLED")
    async def LightenUpLED(self, ctx: commands.Context[Bot]):
        USART_COG: USART_BOT = self.bot.get_cog("USART_BOT") #type: ignore
        
        if not USART_COG:
            return 

        await USART_COG.USART_SEND(LED_COMMANDS["TURN_ON_LED_COMMAND"])
        await ctx.send(f"```[LAIN COMMANDS]: ASKED ATMega328P to turn on the RED LED```")

    @commands.command(name="TurnOFFLED")
    async def TurnOFFLED(self, ctx: commands.Context[Bot]):
        USART_COG: USART_BOT = self.bot.get_cog("USART_BOT") #type: ignore
            
        if not USART_COG:
            return 

        await USART_COG.USART_SEND(LED_COMMANDS["TURN_OFF_LED_COMMAND"])
        await ctx.send(f"```[LAIN COMMANDS]: ASKED ATMega328P to turn off the RED LED```")

async def setup(bot: Bot):
    await bot.add_cog(LightenUPLEDClass(bot))