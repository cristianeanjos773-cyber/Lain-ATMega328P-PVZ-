#import asyncio
#import discord
#import serial


async def SendUsartMessageStatus():
        a = "h"
        print(a) 

'''
async def UsartATest(ChannelID: discord.TextChannel):


    try:
        ser = serial.Serial('COM3', 9600, timeout=1)
        if ser.is_open:
            await ChannelID.send("``` LAIN STATUS: SERIAL CONNECTION MADE. ```")
            await asyncio.sleep(2) 
    except Exception as e:
        await ChannelID.send(f"``` LAIN STATUS: SERIAL CONNECTION FAILED! ERROR: {e} ```")
        return

    while True:
        try:
            if ser.in_waiting > 0:
                letra_vinda_do_c = ser.read(1).decode('utf-8', errors='ignore')
                
                if letra_vinda_do_c == "A":
                    await ChannelID.send(f"``` LAIN STATUS: CHARACTER '{letra_vinda_do_c}' RECEIVED FROM ATMEGA328P! ```")
                    print("we tried, okay?")
                else:
                    await ChannelID.send(f"``` LAIN STATUS: RECEIVED '{letra_vinda_do_c}' FROM ATMEGA328P! ```")
            
            await asyncio.sleep(1)
            
        except Exception as e:
            await ChannelID.send(f"``` LAIN STATUS: SERIAL ERROR DURING LOOP: {e} ```")
            break

    ser.close()
'''
