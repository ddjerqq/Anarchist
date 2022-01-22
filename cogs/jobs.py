import disnake
from disnake import ApplicationCommandInteraction
from disnake.ext import commands
from disnake.ext.commands import errors

from __main__ import PREFIX
from __main__ import GUILD_IDS
from models.buttons import YesNoButton
from database import database
from utils import *

class Jobs(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.slash_command(
        name        = "test", 
        description = "test command made for testing",
        guild_ids   = GUILD_IDS
        )
    async def _test(self, inter: ApplicationCommandInteraction):
        start = disnake.Embed(
            title = "test command",
            description = "click below to choose your fate",
            color = 0x00ff00
        )
        button = YesNoButton()
        
        await inter.send(view = button, embed = start)

        await button.wait()

        if button.choice:
            yes = disnake.Embed(
                title = "Yes",
                color = 0x00ff00
            )
            await inter.edit_original_message(embed = yes, view = None)
        else:
            no = disnake.Embed(
                title = "No",
                color = 0xff0000
            )
            await inter.edit_original_message(embed = no, view = None)


def setup(client):
    client.add_cog(Jobs(client))