# built-ins
import os
import random

# 3rd party libraries
import discord
from discord.ext import commands
from discord.ext import tasks

# local imports
from utils import *
from supersecrets import TOKEN
from database import database

# ~~~~~~~~~~~~~~~~~~~~~~~

PREFIX = "."

client = commands.Bot(
    command_prefix = PREFIX, 
    intents        = discord.Intents.all(), 
    help_command   = None)

# TODO add query commands for mods

def load_extensions():
    for i in os.listdir("cogs"):
        client.load_extension(f"cogs.{i[:-3]}")
        print(f"{i:[-3]} loaded.")

def main():
    load_extensions()
    client.run(TOKEN)

if __name__ == "__main__":
    try:
        load_extensions()
        main()

    except KeyboardInterrupt:
        warn("keyboard interrupt")
    except Exception as e:
        warn(e)
    finally:
        database.close()
        database.generate_csv()
