import os
import discord
from dotenv import load_dotenv
from auraManagementClient import *

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN_AURA_MA')
GUILD = os.getenv('DISCORD_GUILD_AURA')

client = auraManagementClient(GUILD)
client.run(TOKEN)
