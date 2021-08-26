import os
import discord
from dotenv import load_dotenv
from strikeClient import *

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN_STRIKE')
GUILD = os.getenv('DISCORD_GUILD')

client = strikeClient(GUILD)
client.run(TOKEN)
