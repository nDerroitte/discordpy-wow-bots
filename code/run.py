import os
import discord
from dotenv import load_dotenv
from mainClient import *

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

client = MainClient(GUILD)
client.run(TOKEN)
