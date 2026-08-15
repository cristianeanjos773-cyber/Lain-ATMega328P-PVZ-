"""
This is a helper function to generate a string between "TOTALLY dark" and "FULLY BRIGHT"
it helps USART_READ take care only of reading the serial port and not concerning about formatting statuses. 
"""

def LightNumberStatus(LIGHT_VALUE: int) -> str:

    if LIGHT_VALUE == 0:
        return "TOTALLY DARK"
    elif LIGHT_VALUE >= 1 and LIGHT_VALUE <= 199:
        return "DARK ROOM"
    elif LIGHT_VALUE >= 200 and LIGHT_VALUE <= 599: 
        return "MID ILUMINOSITY"
    elif LIGHT_VALUE >= 600 and LIGHT_VALUE <= 899:
        return "BRIGHT ROOM" 
    elif LIGHT_VALUE >= 900 and LIGHT_VALUE <= 1022:
        return "VERY BRIGHT ROOM"
    elif LIGHT_VALUE == 1023:
        return "TOTALLY BRIGHT ROOM"
    else:
        return "TOTALLY BRIGHT ROOM"