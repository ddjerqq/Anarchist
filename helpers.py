import discord

from utils import *

async def dm_user(
    user: discord.Member,
    *,
    message: str           = None,
    embed:   discord.Embed = None ) -> None:
    """
        dm an user by their id
        ~~~~~~~~~~~~~~~~~~~~~~~
        Args:
            user (discord.Member): who you want to send the DM to.
            *
            message (str): the message you want to send, don't set this to anything if you want to send an embed.
            embed (discord.Embed): send an embed
    """
    if not message: await user.send(embed=embed)
    elif not embed: await user.send(message)
    else: warn("what are you sending this user?")