import disnake

from utils import *


async def dm_user(
    user: disnake.Member, *, message: str = None, embed: disnake.Embed = None
) -> None:
    """
    dm an user by their id
    ~~~~~~~~~~~~~~~~~~~~~~~
    Args:
        user (disnake.Member): who you want to send the DM to.
        *
        message (str): the message you want to send, don't set this to anything if you want to send an embed.
        embed (disnake.Embed): send an embed
    """
    if not message:
        await user.send(embed=embed)
    elif not embed:
        await user.send(message)
    else:
        warn("what are you sending this user?")
