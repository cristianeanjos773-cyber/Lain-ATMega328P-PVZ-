import discord
import random 
import asyncio 
from discord.ext import commands
from Engine import Bot
from Command_Bytes_sent import LED_COMMANDS

from GLOBAL.GlobalTypes import USART_BOT

async def RandomLed() -> bytes:

    LedCommandList = [
       LED_COMMANDS["LED3_CHOSEN"],
       LED_COMMANDS["LED4_CHOSEN"],
       LED_COMMANDS["LED7_CHOSEN"]
    ]
    
    ChosenLedCommandList = random.choice(LedCommandList)

    return ChosenLedCommandList  

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

        except TimeoutError:
            await ctx.send(f"[LAIN MINIGAMES: LEDGAME]: TIMEOUT! If you want to start again, use the init command!")

         
    @commands.command(name="LedGameInit")
    async def LedGameInit(self, ctx: commands.Context[Bot]):

        USART_COG: USART_BOT = self.bot.get_cog("USART_BOT") #type: ignore

        if not USART_COG :
            print(f"[LedGame]: was not able to find usart cog")
            return  

        RandomChosenLed: bytes = await RandomLed()

        await USART_COG.USART_SEND(RandomChosenLed)

        await ctx.send(f"```[LAIN MINIGAMES: LEDGAME]: Try to guess the red LED! (RED LED:7, GREEN LIGHT:4, SECOND RED LED: 3) YOU HAVE 30 SECONDS \n right answer: '{RandomChosenLed}'``` \n ('Randomchosenled byte: {RandomChosenLed}'), command byte: \n {LED_COMMANDS["LED_GAME_START_COMMAND"]} ")

        UserMessageAnswer: discord.Message | None = await self.ReturnMessageInput(ctx=ctx) 

        if UserMessageAnswer is None:
            return
        
        Correct_Led_Number: int = int.from_bytes(RandomChosenLed, byteorder="little")

        try:
            UserAnswerNum = int(UserMessageAnswer.content)
        except ValueError:
            await ctx.send(f"```[LAIN MINIGAMES: LEDGAME]: YOU LOST! You must type a valid number.```")
            return


        if UserAnswerNum < 0 or UserAnswerNum > 255:
            await ctx.send(f"```[LAIN MINIGAMES: LEDGAME]: YOU LOST! you tried to guess a number that is bigger or smaller than an unsigned 1 byte integer (uint8_t in C)```")
            return
        
        if UserAnswerNum == Correct_Led_Number:
            await ctx.send(f"```[LAIN MINIGAMES: LEDGAME]: YOU WON! You guessed the right activated LED!```")
        else:
            await ctx.send(f"```[LAIN MINIGAMES: LEDGAME]: YOU LOST! You either guessed the wrong activated LED or passed something invalid, the right LED NUMBER WAS:\n '{Correct_Led_Number}' ```")
            await ctx.send(f"USERMSGANSWER BYTE: '{UserAnswerNum}' | USERMESGANSWER: '{UserMessageAnswer.content}'")

        
        

async def setup(bot: Bot): 
    await bot.add_cog(LedGame(bot))