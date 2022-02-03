import random

import disnake
from disnake import ApplicationCommandInteraction as Aci
from disnake.ext import commands
from disnake.ext.commands import errors

# from __main__ import PREFIX
from __main__ import GUILD_IDS
from models.components import YesNoButton, LowerHigherGuessButton
from easydb import database
from utils import *


class Jobs(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.cooldown(1, 60, commands.BucketType.user)
    @commands.slash_command(
        name        = "work",
        description = f"work and earn 50 coins, you can use this command every minute",
        # guild_ids   = GUILD_IDS
    )
    async def _work(self, inter: Aci):
        async with inter.channel.typing():
            em = disnake.Embed(
                color = 0x00FF00, 
                title = f"Nice work!",
                description= "You earned 50 coins"
                )
            await inter.send(embed = em)
            database.give(924293465997705286, inter.author.id, 50)
            database.update()

    @_work.error
    async def _work_error(self, ctx: commands.Context, _error):
        if isinstance(_error, errors.CommandOnCooldown):
            em = disnake.Embed(
                color       = 0xFF0000,
                title       = f"You are on cooldown!",
                description = f"You can work again in {round(_error.retry_after)} seconds"
            )
            await ctx.send(embed = em)
        else:
            rgb(_error, 0xff0000)

    @commands.slash_command(
        name        = "gamble",
        # guild_ids   = GUILD_IDS,
        description = "Gamble your coins for a chance to triple them (limit 500)")
    async def _gamble(self, inter: Aci, amount: int):
        confirmation_needed = False
        if amount < 10 or amount > 500:
            limit_em = disnake.Embed(
                color = 0xff0000,
                title = "Gambling range is 10 - 500 coins"
            )
            await inter.send(embed = limit_em)
            return

        if database[inter.author.id].money < amount:
            not_enough_money_em = disnake.Embed(
                color = 0xff0000,
                title = "You don't have enough money genius!"
            )
            await inter.send(embed = not_enough_money_em)
            return

        if amount >= 100:
            confirmation_needed = True
            confirmation_em = disnake.Embed(
                color = 0xffff00,
                title = f"Do you **really** want to gamble {amount} coins?"
            )
            conf_btn = YesNoButton(intended_user=inter.author)
            await inter.send(view = conf_btn, embed = confirmation_em)
            
            await conf_btn.wait()

            if not conf_btn.choice:
                deny_gamble = disnake.Embed(
                    color = 0xff0000,
                    title = "Make your up mind next time",
                    description = "dumbass"
                )
                await inter.edit_original_message(embed = deny_gamble, view = None)
                return

        win_em = disnake.Embed(
                color = 0x00ff00,
                title = f"You won {amount * 3}",
                description = "**You're lucky**"
            )
        lose_em = disnake.Embed(
                color = 0xff0000,
                title = f"You lost {amount}",
                description = "**LMFAOO LOSER!!!**"
            )        
        if random.random() >= 0.80:
            if confirmation_needed:
                await inter.edit_original_message(embed = win_em, view = None)
            else:
                await inter.send(embed = win_em)
            database.give(924293465997705286, inter.author.id, amount * 4)
        else:
            if confirmation_needed:
                await inter.edit_original_message(embed = lose_em, view = None)
            else:
                await inter.send(embed = lose_em)
            database.give(inter.author.id, 924293465997705286, amount)

    @commands.cooldown(1, 30, commands.BucketType.user)
    @commands.slash_command(
        name        = "guess",
        # guild_ids   = GUILD_IDS,
        description = "Guess if a number is higher or lower than another")
    async def _guess(self, inter: Aci):
        secret = random.randint(0, 10000)
        sample = random.randint(2000, 7000)
        reward = random.randint(30, 100)
        og_btn = LowerHigherGuessButton(intended_user=inter.author)
        og_em  = disnake.Embed(
            color = 0x00ff00,
            title = "Guess number",
            description = f"is {sample} lower or higher than the secret number?"
        )
        win_em = disnake.Embed(
            color = 0x00ff00,
            title = "Correct guess",
            description= f"You won {reward} coins"
        )
        jack_em = disnake.Embed(
            color = 0x00ff00,
            title = "JACKPOT?!??!",
            description = f"HOLY SHIT HOW?!? You won {reward * 10} coins!!!"
        )
        lose_em = disnake.Embed(
            color = 0xff0000,
            title = f"You lost, bahaha",
            description= "Better luck next time"
        )

        await inter.send(embed = og_em, view = og_btn)
        await og_btn.wait()

        if (og_btn.choice == "higher" and sample > secret) or (og_btn.choice == "lower" and sample < secret):
            await inter.edit_original_message(embed = win_em, view = None)
            database.give(924293465997705286, inter.author.id, reward)
        elif og_btn.choice == "guess" and sample == secret:
            await inter.edit_original_message(embed = jack_em, view = None)
            database.give(924293465997705286, inter.author.id, reward * 10)
        else:
            await inter.edit_original_message(embed = lose_em, view = None)

    @_guess.error
    async def _guess_error(self, ctx: commands.Context, _error):
        if isinstance(_error, errors.CommandOnCooldown):
            em = disnake.Embed(
                color       = 0xFF0000,
                title       = f"You are on cooldown!",
                description = f"You can use this command again in {round(_error.retry_after)} seconds"
            )
            await ctx.send(embed = em)
        else:
            rgb(_error, 0xff0000)

    @commands.cooldown(1, 86400, commands.BucketType.user)
    @commands.slash_command(
        name = "daily",
        description = "use this command to claim your daily amount of coins",
        guild_ids = GUILD_IDS
    )
    async def _daily(self, inter: Aci):
        async with inter.channel.typing():
            database.give(924293465997705286, inter.author.id, 500)
        em = disnake.Embed(
            color = 0x00ff00,
            title = "Daily",
            description = f"You received 500 coins"
        )
        await inter.send(embed = em)

    @_daily.error
    async def _daily_error(self, ctx: commands.Context, _error):
        if isinstance(_error, errors.CommandOnCooldown):
            em = disnake.Embed(
                color       = 0xFF0000,
                title       = f"You have already collected your daily coins!",
                description = f"You can collect again in {round(_error.retry_after) // 86400} days"
            )
            await ctx.send(embed = em)
        else:
            rgb(_error, 0xff0000)


def setup(client):
    client.add_cog(Jobs(client))
