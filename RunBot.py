from Engine import create_bot
from config import TOKEN 

def main():
    bot = create_bot()
    bot.run(str(TOKEN)) 
    
if __name__ == "__main__":
    main()