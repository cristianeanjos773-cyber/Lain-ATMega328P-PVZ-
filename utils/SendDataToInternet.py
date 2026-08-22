import discord
import requests 
import asyncio 

from GLOBAL.GlobalTypes import JSONType

from dataclasses import asdict


URL_FLASK = "http://localhost:5000/Receive"

 
async def SendDataToInternet(Channel: int, JSON: JSONType):

        MaxAttempts: int = 3 

        for attempts in range(MaxAttempts):

            try:
                Port =  requests.post(URL_FLASK, json=asdict(JSON), timeout=5)
            
                if Port.status_code == 200:

                    if isinstance(Channel, discord.TextChannel):
                        await Channel.send(f"```json\n[LAIN WIRED CONNECTION]: SENT PACKAGE TO THE WIRED! PACKAGE SENT: '{JSON}' ```") ## GG, Lain did it  
                    break

                else:

                    if isinstance(Channel, discord.TextChannel):
                        await Channel.send(f"```[LAIN WIRED CONNECTION]: FAILED TO SEND PACKAGE TO THE WIRED: PORT_CODE_ERROR: '{Port.status_code}' DATA FAILED TO SEND: '{JSON}' ```")
                                                 
        
            except requests.exceptions.RequestException as error:
                if isinstance(Channel, discord.TextChannel):
                    await Channel.send(f"```[LAIN WIRED CONNECTION STATUS]: TRIED TO SEND DATA TO THE WIRED, FAILED! REASON: '{error}' ```") # if this happens pretend lain was distracted looking at nothing and couldnt connect :sob: 

            if attempts < MaxAttempts:
                await asyncio.sleep(2)
            else:
                if isinstance(Channel, discord.TextChannel):
                    await Channel.send(f"```[LAIN WIRED CONNECTION STATUS]: FATAL ERROR! COULD NOT SEND PACKAGE AFTER: '{MaxAttempts}' (its so over :skull:)  ```") # i pray for ts not to happen honestly, pls internet Lain Wired God, dont do thnis ever.
