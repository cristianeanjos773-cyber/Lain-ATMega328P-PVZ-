"""
Purpose: This code will be responsible for the commands where the bot will communicate to the internet anything
in the flask server I created in RunBot.py 
"""
#import requests 
#import discord
#import time

from discord.ext import commands  
from Engine import Bot
from utils.SendDataToInternet import SendDataToInternet 
from GLOBAL.GlobalTypes import JSONType 

#URL_FLASK = "http://localhost:5000/Receive"

class InternetCog(commands.Cog):

    def __init__(self, bot: Bot) -> None: 
        self.bot = bot  
   
    @commands.command(name="SendDataToInternetCommand")
    async def SendDataToInternetCommand(self, ctx: commands.Context[Bot]):
        Channel = self.bot.Config.ChannelSendId 

        JSONToSend: JSONType = JSONType(
            success=True,
            message="Lain Command 1",
            origin="LainATMega328P", 
        )
           
        await ctx.send(f"```[LAIN WIRED CONNECTION STATUS]: REQUESTED TO SEND: '{JSONToSend}' ```")
        await SendDataToInternet(Channel=Channel, JSON=JSONToSend)
                      
                

async def setup(bot: Bot):
    await bot.add_cog(InternetCog(bot))