import discord
import os
from typing import Any
from discord.ext import commands
from GLOBAL.GlobalTypes import BotAttributes 


from config import PREFIX

class Bot(commands.Bot):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.Config: BotAttributes = BotAttributes(ChannelSendId=1412280982253342781)


def create_bot() ->Bot:

    intents = discord.Intents.default()
    intents.message_content = True
    intents.presences = True
    intents.members = True 
    intents.voice_states = True
    
    bot = Bot(command_prefix=PREFIX, intents=intents)
    
    async def setup_hook ():
        
        for FileName in os.listdir('cogs'):
            if FileName.endswith('.py') and not FileName.startswith('__'):
                await bot.load_extension(f"cogs.{FileName[:-3]}")


    bot.setup_hook = setup_hook 

    @bot.event
    async def on_ready():
        ChannelID = 1412280982253342781 # IF YOU'RE A PERSON CHANGING MY BOT, CHANGE THIS TO YOUR OWN CHANNEL ID.
        channel = bot.get_channel(ChannelID)  

        await bot.tree.sync()
   
        if channel:
            #await UsartATest(channel)
            await channel.send("```[LAIN BOOT STATUS]: LAIN IS ONLINE!```") # type: ignore
        else:
            print("channel doesnt exist.")

    return bot 