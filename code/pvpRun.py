import os
import discord
from dotenv import load_dotenv
from pvpClient import *

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN_PVP')
GUILD = os.getenv('DISCORD_GUILD')

client = pvpClient(GUILD)
client.run(TOKEN)
