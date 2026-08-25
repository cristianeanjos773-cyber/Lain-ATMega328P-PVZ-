import discord
from discord.ext import commands
from Engine import Bot
from Command_Bytes_Sent import LED_COMMANDS

from GLOBAL.GlobalTypes import USART_BOT



class LedGame(commands.Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot 

    @commands.command(name="LedGameInit") 
    async def LedGameInit(self, ctx: commands.Context[Bot]):
        USART_COG: USART_BOT = self.bot.get_cog("USART_BOT") #type: ignore 

        if not USART_COG :
            print(f"[LedGame]: was not able to find usart cog")
            return

        await USART_COG.USART_SEND(LED_COMMANDS["LED_GAME_START_COMMAND"])


async def setup(bot: Bot): 
    await bot.add_cog(LedGame(bot))