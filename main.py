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

disnake.channel.VoiceChannel

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
