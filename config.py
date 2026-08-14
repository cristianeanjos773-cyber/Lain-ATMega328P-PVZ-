import os 
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_BOT_TOKEN")
PREFIX = "!"

if not TOKEN:
    raise RuntimeError("DISCORD_BOT_TOKEN is not set in environment variables.")