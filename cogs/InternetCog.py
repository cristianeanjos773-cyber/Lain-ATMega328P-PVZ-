"""
Purpose: This code will be responsible for the stuff the discord Bot will do with the internet, for example send data, read data
in the flask server I created in RunBot.py 
"""
import requests 
import discord
import time

from discord.ext import commands  
from Engine import Bot

URL_FLASK = "http://localhost:5000/Receive"

class InternetCog(commands.Cog):

    def __init__(self, bot: Bot) -> None: 
        self.bot = bot  

    async def SendDataToInternet(self, Message: str):
        self.Channel = await self.bot.fetch_channel(self.bot.Config.ChannelSendId)

        self.DataToSend = {
            "Message": Message, 
            "Origin": "LainATMega328P"
        }

        MaxAttempts: int = 3 

        for attempts in range(MaxAttempts):

            try:
                Port =  requests.post(URL_FLASK, json=self.DataToSend, timeout=5)
            
                if Port.status_code == 200:
                    if isinstance(self.Channel, discord.TextChannel):
                        await self.Channel.send(f"```json\n[LAIN WIRED CONNECTION]: SENT PACKAGE TO THE WIRED! PACKAGE SENT: '{self.DataToSend}' ```") ## GG 
                    break 
                else:
                    if isinstance(self.Channel, discord.TextChannel):
                        await self.Channel.send(f"```[LAIN WIRED CONNECTION]: FAILED TO SEND PACKAGE TO THE WIRED: PORT_CODE_ERROR: '{Port.status_code}' DATA FAILED TO SEND: '{self.DataToSend}' ```")
                                                 
        
            except requests.exceptions.RequestException as error:
                if isinstance(self.Channel, discord.TextChannel):
                    await self.Channel.send(f"```[LAIN WIRED CONNECTION STATUS]: TRIED TO SEND DATA TO THE WIRED, FAILED! REASON: '{error}' ```") # if this happens pretend lain was distracted looking at nothing and couldnt connect

            if attempts < MaxAttempts:
                time.sleep(2)
            else:
                if isinstance(self.Channel, discord.TextChannel):
                    await self.Channel.send(f"```[LAIN WIRED CONNECTION STATUS]: FATAL ERROR! COULD NOT SEND PACKAGE AFTER: '{MaxAttempts}' (its so over :skull:)  ```") # i pray for ts not to happen honestly, pls internet Lain Wired God, dont do thnis ever.

    @commands.command(name="SendDataToInternetCommand")
    async def SendDataToInternetCommand(self, ctx: commands.Context[Bot]):
        MessageToSend: str = "Lain Command 1" # this is for tests, not the finished version 

        await ctx.send(f"```[LAIN WIRED CONNECTION STATUS]: REQUESTED TO SEND: '{MessageToSend}' ```")
        await self.SendDataToInternet(Message=MessageToSend)
                      
                

async def setup(bot: Bot):
    await bot.add_cog(InternetCog(bot))