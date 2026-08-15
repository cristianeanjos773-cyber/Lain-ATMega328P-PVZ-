import discord
import os
from discord.ext import commands

from config import PREFIX

def create_bot():

    intents = discord.Intents.default()
    intents.message_content = True
    intents.presences = True
    intents.members = True 
    intents.voice_states = True
    
    bot = commands.Bot(command_prefix=PREFIX, intents=intents)
    
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
            await channel.send("``` LAIN STATUS: WIRED CONNECTION ESTABILISHED! ```") # type: ignore
        else:
            print("channel doesnt exist.")

    return bot 