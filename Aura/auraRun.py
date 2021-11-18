import os
import discord
from dotenv import load_dotenv
from auraMain import *

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN_AURA')
GUILD = os.getenv('DISCORD_GUILD_AURA')

client = AuraClient(GUILD)
client.run(TOKEN)
