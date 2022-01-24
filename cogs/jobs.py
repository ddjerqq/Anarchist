import random

import disnake
from disnake import ApplicationCommandInteraction as ACI
from disnake.ext import commands
from disnake.ext.commands import errors

from __main__ import PREFIX
from __main__ import GUILD_IDS
from models.buttons import YesNoButton, LowerHigherGuessButton
from database import database
from utils import *

class Jobs(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.cooldown(1, 60, commands.BucketType.user)
    @commands.slash_command(
        name        = "work",
        description = f"work and earn 50 coins, you can use this command every 30 seconds",
        #guild_ids   = GUILD_IDS
    )
    async def _work(self, inter: ACI):
        async with inter.channel.typing():
            em = disnake.Embed(
                color = 0x00FF00, 
                title = f"Nice work!",
                description= "You earned 50 coins"
                )
            await inter.send(embed = em)
            database.give("bank", inter.author.id, 50)

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
        name        = "test", 
        description = "test command made for testing",
        guild_ids   = GUILD_IDS
        )
    async def _test(self, inter: ACI):
        start = disnake.Embed(
            title = "test command",
            description = "click below to choose your fate",
            color = 0x00ff00
        )
        button = YesNoButton(intended_user=inter.author)
        
        await inter.send(view = button, embed = start)

        await button.wait()

        if button.choice:
            yes = disnake.Embed(
                title = "Yes",
                color = 0x00ff00
            )
            await inter.edit_original_message(embed = yes, view = None)
        else:
            no = disnake.Embed(
                title = "No",
                color = 0xff0000
            )
            await inter.edit_original_message(embed = no, view = None)

    @commands.slash_command(
        name        = "gamble",
        #guild_ids   = GUILD_IDS,
        description = "Gamble your coins for a chance to triple them (limit 500)")
    async def _gamble(self, inter: ACI, amount: int):
        confirmation_needed = False
        if amount < 10 or amount > 500:
            limit_em = disnake.Embed(
                color = 0xff0000,
                title = "Gambling range is 10 - 500 coins"
            )
            await inter.send(embed = limit_em)
            return
        if database[inter.author.id].amount < amount:
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
            await inter.send( view = conf_btn, embed = confirmation_em)
            
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
                description = "**LMAOO LOSER!!!**"
            )        
        if random.random() >= 0.75:
            if confirmation_needed:
                await inter.edit_original_message(embed = win_em, view = None)
            else:
                await inter.send(embed = win_em)
            database.give("bank", inter.author.id, amount * 3)
        else:
            if confirmation_needed:
                await inter.edit_original_message(embed = lose_em, view = None)
            else:
                await inter.send(embed = lose_em)
            database.give(inter.author.id, "bank", amount)  


    @commands.cooldown(1, 30, commands.BucketType.user)
    @commands.slash_command(
        name        = "guess",
        guild_ids   = GUILD_IDS,
        description = "Guess if a number is higher or lower than another")
    async def _guess(self, inter: ACI):
        secret = random.randint(0, 1000)
        sample = random.randint(300, 600)
        reward = random.randint(20, 50)
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
            title = "JACKOPOT?!??!",
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
            database.give("bank", inter.author.id, reward)
        elif og_btn.choice == "guess" and sample == secret:
            await inter.edit_original_message(embed = jack_em, view = None)
            database.give("bank", inter.author.id, reward * 10)
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

def setup(client):
    client.add_cog(Jobs(client))