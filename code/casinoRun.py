import os
import discord
from dotenv import load_dotenv
from casinoClient import *

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN_CASINO')
GUILD = os.getenv('DISCORD_GUILD')

client = casinoClient(GUILD)
client.run(TOKEN)
