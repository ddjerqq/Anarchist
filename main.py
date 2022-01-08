# built-ins
import os

# ~~~~~~~~

# 3rd party libraries
import discord
from discord.ext import commands
from discord.ext import tasks
from itertools import cycle

# ~~~~~~~~~~~~~~~~~~~~~~~~

# local imports
from utils import *
from tokens import TOKEN
from database import Database

# ~~~~~~~~~~~~~~~~~~~~~~~

# globals
PREFIX = "!"
intents = discord.Intents.all()
client = commands.Bot(command_prefix=PREFIX, intents=intents)
database = Database(verbose=True)
# ~~~~~~~~~~~~~~~~~~~~~~~

# tasks
@tasks.loop(seconds=10)
async def change_status():
    statuses = cycle([f"{PREFIX}help", "My prefix is {PREFIX}", "rob anyone anytime 😈"])
    await client.change_presence(activity=discord.Game(next(statuses)))


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# events
@client.event
async def on_ready():
    # update member names in database
    for guild in client.guilds:
        async for member in guild.fetch_members(limit=None):
            if member.bot:
                continue
            if member.id not in database:
                database.add_user(member.id, member.name)
                log(f"user {member.name} added to database")
            else:
                tmp_user = database[member.id]
                if tmp_user["name"] != member.name:
                    tmp_user["name"] = member.name
                    database[member.id] = tmp_user
                    warn(
                        f"{tmp_user['name']}'s name updated to {database[member.id]['name']}"
                    )
                continue

    change_status.start()  # start loops
    ok("Bot is online")


# embed = discord.Embed( color = 0xff0000 )
# embed.add_field( name = "bank account", value = "bank money", inline = False )
# embed.add_field( name = "wallet account", value = "wallet money", inline = False )
# await ctx.send( embed = embed )

# commands
@client.command(name="getusers")
async def getuser(ctx: commands.Context, id: str) -> None:
    await ctx.send(database[int(id)])


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~

# commands
# TODO help command
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# THE BELOW MODIFIES THE HELP COMMAND TO MAKE IT AN EMBED


class MyHelpCommand(commands.MinimalHelpCommand):
    async def send_pages(self):
        destination = self.get_destination()
        e = discord.Embed(color=0xFF0000, description="")
        for page in self.paginator.pages:
            e.description += page
        await destination.send(embed=e)


client.help_command = MyHelpCommand()


# DO NOT CHANGE OR REMOVE THE ABOVE FOR THE EMBEDDED HELP COMMAND


def load_extensions() -> None:
    """
    Loads the extensions from cogs
    """
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            client.load_extension(f"cogs.{filename[:-3]}")


def main():
    load_extensions()
    client.run(TOKEN)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        error("keyboard interrupt")
    except Exception as e:
        error(e)
    finally:
        database.close()
        database.generate_csv()
