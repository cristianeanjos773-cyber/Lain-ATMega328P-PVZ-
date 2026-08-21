"""
Purpose: This code will be responsible for the stuff the discord Bot will do with the internet, for example send data, read data
in the flask server I created in RunBot.py 
"""
import requests 
import discord
from discord.ext import commands  
from Engine import Bot

URL_FLASK = ""

class InternetCog(commands.Cog):

    def __init__(self, bot: Bot) -> None: 
        self.bot = bot  
        self.CHANNEL_SEND_ID = 1412280982253342781

    async def SendDataToInternet(self, Message: str):
        self.Channel = await self.bot.fetch_channel(self.CHANNEL_SEND_ID)
        self.DataToSend = {
            "Message": Message, 
            "Origin": "LainATMega328P"
        }

        try:
            pass
            #Port =  requests.post(URL_FLASK, self.DataToSend)
        
        except requests.exceptions.RequestException:
            pass
             

async def setup(bot: Bot):
    await bot.add_cog(InternetCog(bot))