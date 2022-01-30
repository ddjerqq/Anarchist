# built-ins
import os
from itertools import cycle

# 3rd party libraries
import disnake
from disnake.ext import commands

# local imports
from utils import *
from supersecrets import TOKEN
from database import database

DEBUG = False
PREFIX = "?"
STATUSES = cycle([
    f"/help", 
    "worlds first crypto bot", 
    "ddjerqq#1048"
    ])

GUILD_IDS = [
    416021017522077708,
    818081019596636201,
    845005933766639658,
    913003554225131530,
    930562118359588904,
    840836206483734530,
    #336642139381301249
]

ANARCHIST = """
 █████╗  ███╗   ██╗  █████╗  ██████╗   ██████╗ ██╗  ██╗ ██╗ ███████╗ ████████╗
██╔══██╗ ████╗  ██║ ██╔══██╗ ██╔══██╗ ██╔════╝ ██║  ██║ ██║ ██╔════╝ ╚══██╔══╝
███████║ ██╔██╗ ██║ ███████║ ██████╔╝ ██║      ███████║ ██║ ███████╗    ██║   
██╔══██║ ██║╚██╗██║ ██╔══██║ ██╔══██╗ ██║      ██╔══██║ ██║ ╚════██║    ██║   
██║  ██║ ██║ ╚████║ ██║  ██║ ██║  ██║ ╚██████╗ ██║  ██║ ██║ ███████║    ██║   
╚═╝  ╚═╝ ╚═╝  ╚═══╝ ╚═╝  ╚═╝ ╚═╝  ╚═╝  ╚═════╝ ╚═╝  ╚═╝ ╚═╝ ╚══════╝    ╚═╝   
"""

# noinspection PyTypeChecker
client = commands.Bot(
    command_prefix=PREFIX,
    intents=disnake.Intents.all(),
    help_command=None
)


def anarchist():
    for char in ANARCHIST:
        if char == "█":
            rgb(char, 0xff0000, newline=False)
        else:
            rgb(char, 0xffffff, newline=False)


def load_extensions():
    for i in os.listdir("cogs"):
        if not i.startswith("_"):
            client.load_extension(f"cogs.{i[:-3]}")


def main():
    anarchist()
    load_extensions()
    client.run(TOKEN)


if __name__ == "__main__":
    if not DEBUG:
        try:
            main()
        except KeyboardInterrupt:
            warn("keyboard interrupt")
        except Exception as e:
            warn(e)
        finally:
            database.close()
    else:
        main()