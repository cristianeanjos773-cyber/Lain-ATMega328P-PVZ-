import time 
import discord
import requests 

from Engine import Bot
from GLOBAL.GlobalTypes import JSONType

from dataclasses import asdict


URL_FLASK = "http://localhost:5000/Receive"


async def SendDataToInternet(bot: Bot, JSON: JSONType):
        Channel = await bot.fetch_channel(bot.Config.ChannelSendId)
        MaxAttempts: int = 3 

        for attempts in range(MaxAttempts):

            try:
                Port =  requests.post(URL_FLASK, json=asdict(JSON), timeout=5)
            
                if Port.status_code == 200:

                    if isinstance(Channel, discord.TextChannel):
                        await Channel.send(f"```json\n[LAIN WIRED CONNECTION]: SENT PACKAGE TO THE WIRED! PACKAGE SENT: '{JSON}' ```") ## GG 
                    break

                else:

                    if isinstance(Channel, discord.TextChannel):
                        await Channel.send(f"```[LAIN WIRED CONNECTION]: FAILED TO SEND PACKAGE TO THE WIRED: PORT_CODE_ERROR: '{Port.status_code}' DATA FAILED TO SEND: '{JSON}' ```")
                                                 
        
            except requests.exceptions.RequestException as error:
                if isinstance(Channel, discord.TextChannel):
                    await Channel.send(f"```[LAIN WIRED CONNECTION STATUS]: TRIED TO SEND DATA TO THE WIRED, FAILED! REASON: '{error}' ```") # if this happens pretend lain was distracted looking at nothing and couldnt connect

            if attempts < MaxAttempts:
                time.sleep(2)
            else:
                if isinstance(Channel, discord.TextChannel):
                    await Channel.send(f"```[LAIN WIRED CONNECTION STATUS]: FATAL ERROR! COULD NOT SEND PACKAGE AFTER: '{MaxAttempts}' (its so over :skull:)  ```") # i pray for ts not to happen honestly, pls internet Lain Wired God, dont do thnis ever.
