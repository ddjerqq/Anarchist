# from __main__ import PREFIX
import disnake
from disnake.ext import commands
from disnake import ApplicationCommandInteraction as Aci
from disnake.ext.commands import errors

# from __main__ import GUILD_IDS
from easydb import database
from models.block import Block
from models.components import YesNoButton
from models.user import User
from utils import *


class Currency(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.slash_command(
        name        = "bal",
        description = f"Get your, or someone else's balance",
        # guild_ids   = GUILD_IDS
    )
    async def _bal(self, inter: Aci, user: disnake.Member = None):
        if not user:
            user = inter.author

        if user.id == self.client.user.id:
            em = disnake.Embed(
                color = 0x00FF00,
                title = f"National bank reserve",
                description = f"{User.from_id(user.id, database).money} coins"
            )
            await inter.send(embed = em)

        em = disnake.Embed(
            color       = 0x00FF00,
            title       = f"{User.from_id(user.id, database).username}'s balance",
            description = f"{User.from_id(user.id, database).money} coins"
        )
        await inter.send(embed = em)

    @commands.user_command(
        name        = "balance",
        description = f"Get this users balance",
        # guild_ids   = GUILD_IDS
    )
    async def _bal_user_command(self, inter: Aci, user: disnake.Member):
        if user.id == self.client.user.id:
            em = disnake.Embed(
                color = 0x00FF00,
                title = f"National bank reserve",
                description = f"{User.from_id(user.id, database).money} coins"
            )
            await inter.send(embed = em)
        else:
            em = disnake.Embed(
                color       = 0x00FF00,
                title       = f"{User.from_id(user.id, database).username}'s balance",
                description = f"{User.from_id(user.id, database).money} coins"
            )
            await inter.send(embed = em)

    @commands.slash_command(
        name        = "give",
        description = f"Give a user some coins, minimum transaction is 10 ⏣",
        # guild_ids   = GUILD_IDS
    )
    async def _give(self, inter: Aci, user: disnake.Member, amount: int) -> None:
        em_minimum_transaction = disnake.Embed(
            color=0xFF0000, 
            title=f"Minimum transaction is 10 coins"
        )
        em_no_money = disnake.Embed(
            title = "You don't have enough money",
            color = 0xff0000,
            description = f"Try working you lazy ass hoe"
        )
        em_confirm = disnake.Embed(
            color = 0x00ff00,
            title = "Confirm transaction",
            description = f"Do you **really** want to give {user.name} {amount} coins?"
        )
        em_cancelled = disnake.Embed(
            color = 0xff0000,
            title = "Transaction cancelled by sender",
            description = "Make your mind up next time"
        )
        em_success = disnake.Embed(
            color = 0x00ff00,
            title = "Transaction successful",
            description = f"You sent {user.name} {amount} coins"
        )
        em_notif = disnake.Embed(
            title = "You got money",
            color = 0x00ff00,
            description = f"{inter.author.name} gave you {amount} coins"
        )
        if inter.author.avatar.url:
            em_notif.set_thumbnail(
                url = inter.author.avatar.url
            )
        em_notif.set_footer(
            text = f"Block: #{Block.last_block(database).index}"
        )

        btn_confirm = YesNoButton(intended_user=inter.author)
        
        if amount < 10:
            await inter.send(embed = em_minimum_transaction)
            return

        if amount <= database[inter.author.id].money:
            await inter.send(embed = em_confirm, view = btn_confirm)
            await btn_confirm.wait()
            if not btn_confirm.choice:
                await inter.edit_original_message(embed = em_cancelled)
                return

            async with inter.channel.typing():
                await inter.edit_original_message(embed = em_success, view = None)
                if database[user.id].notifications:
                    await user.send(embed = em_notif)
                database.give(inter.author.id, user.id, amount)
        else:
            await inter.send(em_no_money)

    @_give.error
    async def _give_error(self, ctx: commands.Context, _error) -> None:
        em_member_404 = disnake.Embed(
                color = 0xFF0000,
                title = f"Member could not be found"
            )
        if isinstance(_error, errors.MemberNotFound):
            await ctx.send(embed=em_member_404)
        else:
            rgb(_error, 0xff0000)


def setup(client):
    client.add_cog(Currency(client))
