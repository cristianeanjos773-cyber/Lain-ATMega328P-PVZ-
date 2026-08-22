from threading import Thread 
from Engine import create_bot
from flask import Flask, request
from config import TOKEN 
from Engine import create_bot, BotAttributes  

app = Flask(__name__)

class ServerState:
    def __init__(self) -> None:
        self.LatestData = None

State = ServerState() 

@app.route("/Receive", methods=["POST"])
def ReceiveServerData():
    State.LatestData = request.get_json() 
    return {"status": "Success"}, 200

@app.route("/Data", methods=["GET"])
def GetData():
    if State.LatestData is None:
       return {"status": "Failed", "message": "NO_DATA"}, 200

    return State.LatestData, 200  


def RunServer():
    app.run(host="0.0.0.0", port=5000, debug=False)   

def main():

    ServerThread = Thread(target=RunServer)
    ServerThread.daemon = (True)

    ServerThread.start() 

    bot = create_bot() 

    bot.Config = BotAttributes( #type: ignore 
        ChannelSendId=1412280982253342781, 
    )

    bot.run(str(TOKEN))  
    
if __name__ == "__main__":
    main() # The born of Lain's Digital Mind.
    # Let's all love Lain.  