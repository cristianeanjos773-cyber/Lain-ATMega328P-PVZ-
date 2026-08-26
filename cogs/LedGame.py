import discord
import random 
from discord.ext import commands
from Engine import Bot
from Command_Bytes_sent import LED_COMMANDS

from GLOBAL.GlobalTypes import USART_BOT

async def RandomLed() -> bytes:

    LedNumbers = [
        3,
        4,
        7, 
    ]
    
    RandomNumber = random.choice(LedNumbers)

    return bytes([RandomNumber])  

class LedGame(commands.Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot 

    @commands.command(name="LedGameInit") 
    async def LedGameInit(self, ctx: commands.Context[Bot]):

        USART_COG: USART_BOT = self.bot.get_cog("USART_BOT") #type: ignore

        if not USART_COG :
            print(f"[LedGame]: was not able to find usart cog")
            return  

        RandomChosenLed: bytes = await RandomLed()
         
        await USART_COG.USART_SEND(LED_COMMANDS["LED_GAME_START_COMMAND"])

        await USART_COG.USART_SEND(RandomChosenLed)


async def setup(bot: Bot): 
    await bot.add_cog(LedGame(bot))