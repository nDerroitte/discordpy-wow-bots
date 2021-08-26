import os
import discord
from dotenv import load_dotenv
from roleClient import *

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN_ROLE')
GUILD = os.getenv('DISCORD_GUILD')

client = RoleClient(GUILD)
client.run(TOKEN)
