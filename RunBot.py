from threading import Thread 
from Engine import create_bot
from flask import Flask, request 
from config import TOKEN 
from Engine import create_bot, BotAttributes  # <-- Adicione BotAttributes aqui no import

app = Flask(__name__)

@app.route("/Receive", methods=["POST"])
def ReceiveServerData():
    Data = request.json 
    print(f"Data received: '{Data}'")
    return {"status": "Success"}, 200

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
    main()