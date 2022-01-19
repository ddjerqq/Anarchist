# built-ins
import os

# 3rd party libraries
import disnake
from disnake.ext import commands

# local imports
from utils import *
from supersecrets import TOKEN
from database import database

# TODO add query commands for mods

PREFIX = "."
GUILD_IDS = [
    416021017522077708,
    818081019596636201,
    845005933766639658,
    913003554225131530,
    930562118359588904
]


client = commands.Bot(
    command_prefix=PREFIX,
    intents=disnake.Intents.all(),
)

class MyHelpCommand(commands.MinimalHelpCommand):
    async def send_pages(self):
        destination = self.get_destination()
        e = disnake.Embed(color=0x00FF00, description="")
        for page in self.paginator.pages:
            e.description += page
        await destination.send(embed=e)

def load_extensions():
    for i in os.listdir("cogs"):
        if not i.startswith("_"):
            client.load_extension(f"cogs.{i[:-3]}")

def main():
    client.help_command = MyHelpCommand()
    load_extensions()
    client.run(TOKEN)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        warn("keyboard interrupt")
    except Exception as e:
        warn(e)
    finally:
        database.close()








"""
import disnake
from disnake.ext import commands
from disnake import ApplicationCommandInteraction


class Fun(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.slash_command(name="avatar", description="gets a users avatar")
    async def get_avatar(
        self, inter: ApplicationCommandInteraction, member: disnake.Member = None
    ):
        member = member or inter.author
        em = disnake.Embed(color=0xD3D3D3, title=f"{member}'s avatar")
        em.set_image(url=member.avatar.url)
        await inter.send(embed=em, ephemeral=True)



    @commands.slash_command(
        name="invite",
        description="returns the bots invite and lets you invite the bot to any server",
    )
    async def invite_bot(self, inter: ApplicationCommandInteraction):
        URL = "https://discord.com/api/oauth2/authorize?client_id=923632746230857798&permissions=8&scope=bot%20applications.commands"
        em = disnake.Embed(color=0xD3D3D3, title="Click me to Invite!", url=URL)
        em.set_author(name=self.client.user, icon_url=self.client.user.avatar.url)
        await inter.send(embed=em, ephemeral=True)



    @commands.slash_command(
        name="ping",
        description="returns bot latency",
    )
    async def get_ping(self, inter: ApplicationCommandInteraction):
        em = disnake.Embed(
            title="Pong! 🏓",
            color=0xD3D3D3,
            description=f"Latency: {round(self.client.latency * 1000)}ms",
        )
        await inter.send(embed=em, ephemeral=True)


def setup(client):
    client.add_cog(Fun(client))
"""