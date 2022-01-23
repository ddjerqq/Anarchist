import random

import disnake
from disnake import ApplicationCommandInteraction
from disnake.ext import commands
from disnake.ext.commands import errors

from __main__ import PREFIX
from __main__ import GUILD_IDS
from models.buttons import YesNoButton
from database import database
from utils import *

class Jobs(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.slash_command(
        name        = "test", 
        description = "test command made for testing",
        guild_ids   = GUILD_IDS
        )
    async def _test(self, inter: ApplicationCommandInteraction):
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
    async def _gamble(self, inter: ApplicationCommandInteraction, amount: int):
        if amount > 500:
            limit_em = disnake.Embed(
                color = 0xff0000,
                title = "Gambling limit is 500 coins"
            )
            await inter.send(embed = limit_em)
            return
        if database[inter.author.id].amount >= amount:
            confirmation_em = disnake.Embed(
                color = 0xffff00,
                title = f"Do you **really** want to gamble {amount} coins?"
            )
            confirmation_button = YesNoButton(intended_user=inter.author)
            await inter.send(
                view = confirmation_button, 
                embed = confirmation_em
                )
            
            await confirmation_button.wait()

            if confirmation_button.choice == True:
                if random.random() >= 0.75:
                    database.give("bank", inter.author.id, amount * 3)
                    state = disnake.Embed(
                        color = 0x00ff00,
                        title = f"You won {amount * 3}",
                        description = "**You're lucky**"
                    )
                else:
                    database.give(inter.author.id, "bank", amount)
                    state = disnake.Embed(
                        color = 0xff0000,
                        title = f"You lost {amount}",
                        description = "**LMAOO LOSER!!!**"
                    )
                await inter.send(embed = state, view = None)
            else:
                deny_gamble = disnake.Embed(
                    color = 0xff0000,
                    title = "Make up your mind next time",
                    description = "dumbass"
                )
                await inter.send(embed = deny_gamble, view = None)

        else:
            not_enough_money_em = disnake.Embed(
                color = 0xff0000,
                title = "You don't have enough money genius!"
            )
            await inter.send(embed = not_enough_money_em)

def setup(client):
    client.add_cog(Jobs(client))