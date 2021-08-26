import os
import discord
from dotenv import load_dotenv
from timeClient import *

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN_TIME')
GUILD = os.getenv('DISCORD_GUILD')

client = timeClient(GUILD)
client.run(TOKEN)
