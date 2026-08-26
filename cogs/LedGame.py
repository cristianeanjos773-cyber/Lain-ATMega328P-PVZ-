import discord
import random 
import asyncio 
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


    async def ReturnMessageInput(self, ctx: commands.Context[Bot]) -> discord.Message | None:

        try:
            AnswerMessage: discord.Message = await self.bot.wait_for(
                "message", 
                check=lambda m: (m.channel == ctx.channel and m.author != self.bot.user), 
                timeout=30
            )

            if AnswerMessage:
                return AnswerMessage 

        except asyncio.timeout:
            await ctx.send(f"[LAIN MINIGAMES: LEDGAME]: TIMEOUT! If you want to start again, use the init command!")

         
    @commands.command(name="LedGameInit")
    async def LedGameInit(self, ctx: commands.Context[Bot]):

        USART_COG: USART_BOT = self.bot.get_cog("USART_BOT") #type: ignore

        if not USART_COG :
            print(f"[LedGame]: was not able to find usart cog")
            return  

        RandomChosenLed: bytes = await RandomLed()
         
        await USART_COG.USART_SEND(LED_COMMANDS["LED_GAME_START_COMMAND"])
        await USART_COG.USART_SEND(RandomChosenLed)
        await ctx.send(f"```[LAIN MINIGAMES: LEDGAME]: Try to guess the red LED! (RED LED:7, GREEN LIGHT:4, SECOND RED LED: 3) YOU HAVE 30 SECONDS```")

        UserMessageAnswer: discord.Message | None = await self.ReturnMessageInput(ctx=ctx) 

        if UserMessageAnswer is None:
            return
        
        UserMessageContentByte: bytes = UserMessageAnswer.content.encode(encoding="ascii")

        if int.from_bytes(UserMessageContentByte) < 0 or int.from_bytes(UserMessageContentByte) > 255:
            await ctx.send(f"[LAIN MINIGAMES: LEDGAME]: YOU LOST! you tried to guess a number that is bigger or smaller than an unsigned 1 byte integer (uint8_t in C)")

        if UserMessageContentByte == RandomChosenLed:
            await ctx.send(f"[LAIN MINIGAMES: LEDGAME]: YOU WON! You guessed the right activated LED!")
        else: 
            await ctx.send(f"[LAIN MINIGAMES: LEDGAME]: YOU LOST! You either guessed the wrong activated LED or passed something invalid")



async def setup(bot: Bot): 
    await bot.add_cog(LedGame(bot))