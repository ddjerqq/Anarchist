import disnake
from disnake import ApplicationCommandInteraction
from disnake.ext import commands
from disnake.ext.commands import errors

from __main__ import PREFIX
from __main__ import GUILD_IDS

from database import database
from utils import *

class Jobs(commands.Cog):
    def __init__(self, client):
        self.client = client
    
def setup(client):
    client.add_cog(Jobs(client))
