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


@client.command(name = "help")
async def help_command(ctx, _type: str = None):
    em = discord.Embed(title="Categories", color=0xFF0000)
    em.set_footer(
        text="type `.help [category] for help with a specific category or command`"
    )
    if not _type:
        em.set_author(name="Help")
        categories = "**Currency**\n**Information**"
        em.description = categories
    elif _type.lower() == "currency":
        em.title = "Currency Commands"
        currency_commands = [
            "**Balance**",
            "**Rob**",
            "**Work**",
            "**Deposit**",
            "**Withdraw**",
            "**Give**",
        ]
        currency_commands = ", ".join(currency_commands)
        em.description = currency_commands
    await ctx.send(embed=em)

@client.command(name = "info")
async def info(ctx: commands.Context, user: discord.Member = None):
    if not user: 
        user = ctx.author

    embed: discord.Embed = discord.Embed( 
        title = f"{user.name}#{user.discriminator}'s info", 
        color = 0xff0000
        )
    embed.add_field( 
        name   = "creation time",
        value  = str(user.created_at),
        inline = False
        )
    embed.add_field( 
        name   = "id",
        value  = user.id,
        inline = False
        )
    embed.add_field( 
        name   = "is bot?",
        value  = user.bot,
        inline = False
        )
    embed.set_image(
        url = user.avatar_url
    )

    await ctx.send(embed=embed)

#TODO add query commands for mods




def load_extensions() -> None:
    for file_name in os.listdir("./cogs"):
        if file_name.endswith(".py"):
            client.load_extension(f"cogs.{file_name[:-3]}")

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