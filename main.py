# built-ins
import os

# 3rd party libraries
import discord
from discord.ext import commands

# local imports
from utils import *
from supersecrets import TOKEN
from database import database

# TODO add query commands for mods
# TODO HOOK THE FUCKING BLOCKCHAIN ALREADY JESUS

PREFIX = "."

client = commands.Bot(
    command_prefix = PREFIX,
    intents        = discord.Intents.all(),
    help_command   = None
    )

def load_extensions():
    for i in os.listdir("cogs"):
        client.load_extension(f"cogs.{i[:-3]}")

def main():
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
        database.generate_csv()