import asyncio
import random

import disnake
from disnake import ApplicationCommandInteraction as Aci
from disnake.ext import commands
from disnake.ext.commands import errors

from __main__ import GUILD_IDS
from models.components import YesNoButton, LowerHigherGuessButton, BlackJackButton
from models.deck import Deck
from models.hand import Hand

from easydb import database
from utils import *


class Games(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.slash_command(
        name = "gamble",
        # guild_ids   = GUILD_IDS,
        description = "Gamble your coins for a chance to triple them (limit 1k)")
    async def _gamble(self, inter: Aci, amount: int):
        confirmation_needed = False
        if amount < 10 or amount > 1000:
            limit_em = disnake.Embed(
                color = 0xff0000,
                title = "Gambling range is 10 - 1000 coins"
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
            conf_btn = YesNoButton(intended_user = inter.author)
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
        if random.random() >= 0.75:
            if confirmation_needed:
                await inter.edit_original_message(embed = win_em, view = None)
            else:
                await inter.send(embed = win_em)
            database.give(924293465997705286, inter.author.id, amount * 3)
        else:
            if confirmation_needed:
                await inter.edit_original_message(embed = lose_em, view = None)
            else:
                await inter.send(embed = lose_em)
            database.give(inter.author.id, 924293465997705286, amount)

    @commands.cooldown(1, 30, commands.BucketType.user)
    @commands.slash_command(
        name = "guess",
        # guild_ids   = GUILD_IDS,
        description = "Guess if a number is higher or lower than another")
    async def _guess(self, inter: Aci):
        secret = random.randint(0, 10000)
        sample = random.randint(2000, 7000)
        reward = random.randint(30, 100)
        og_btn = LowerHigherGuessButton(intended_user = inter.author)
        og_em = disnake.Embed(
            color = 0x00ff00,
            title = "Guess number",
            description = f"is {sample} lower or higher than the secret number?"
        )
        win_em = disnake.Embed(
            color = 0x00ff00,
            title = "Correct guess",
            description = f"You won {reward} coins"
        )
        jack_em = disnake.Embed(
            color = 0x00ff00,
            title = "JACKPOT?!??!",
            description = f"HOLY SHIT HOW?!? You won {reward * 10} coins!!!"
        )
        lose_em = disnake.Embed(
            color = 0xff0000,
            title = f"You lost, bahaha",
            description = "Better luck next time"
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

    @commands.slash_command(
        name = "blackjack",
        guild_ids = GUILD_IDS,
        description = "bet money and play blackjack"
    )
    async def _blackjack(self, inter: Aci, *, bet: int):
        if bet > database[924293465997705286].money:
            em = disnake.Embed(
                color = 0xff0000,
                title = "You don't have enough money",
                description = "You can't bet that much"
            )
            await inter.send(embed = em)
            return

        if 20 > bet > 5000:
            em = disnake.Embed(
                color = 0xff0000,
                title = "You can't bet that much",
                description = "You can bet between 20 and 5000"
            )
            await inter.send(embed = em)
            return

        deck = Deck()
        player = Hand()
        dealer = Hand()

        player.add_card(deck.draw())
        player.add_card(deck.draw())

        dealer.add_card(deck.draw())

        def create_em(p, d) -> disnake.Embed:
            score_em = disnake.Embed(
                color = 0x00ff00,
            )
            score_em.add_field(
                name = f"You have: {p.value}",
                value = f"{p.str_cards}",
                inline = False
            )
            score_em.add_field(
                name = f"Dealer has: {d.value}",
                value = f"{d.str_cards}",
                inline = False
            )
            return score_em

        await inter.send(embed = create_em(player, dealer))

        while player.value < 21:

            action_btn = BlackJackButton(intended_user = inter.author)
            await inter.edit_original_message(embed = create_em(player, dealer), view = action_btn)
            await action_btn.wait()

            if action_btn.choice == "hit":
                action_btn.choice = None
                player.add_card(deck.draw())
                await inter.edit_original_message(embed = create_em(player, dealer))
                await asyncio.sleep(1)
            else:
                await inter.edit_original_message(embed = create_em(player, dealer), view = None)
                break

        while dealer.value < 17:
            if player.value >= 21:
                break
            dealer.add_card(deck.draw())
            await inter.edit_original_message(embed = create_em(player, dealer), view = None)
            await asyncio.sleep(1)

        if player.value > 21:
            em = disnake.Embed(
                color = 0xff0000,
                title = "You busted",
                description = f"you lost {bet} coins"
            )
            await inter.send(embed = em)
            database.give(inter.author.id, 924293465997705286, bet)
        elif dealer.value > 21:
            em = disnake.Embed(
                color = 0x00ff00,
                title = "Dealer busted",
                description = f"you won {bet * 3} coins"
            )
            await inter.send(embed = em)
            database.give(924293465997705286, inter.author.id, bet * 3)
        elif player.value > dealer.value:
            em = disnake.Embed(
                color = 0x00ff00,
                title = "You won",
                description = f"you won {bet * 3} coins"
            )
            await inter.send(embed = em)
            database.give(924293465997705286, inter.author.id, bet * 3)
        elif player.value < dealer.value:
            em = disnake.Embed(
                color = 0xff0000,
                title = "Dealer won",
                description = f"you lost {bet} coins"
            )
            await inter.send(embed = em)
            database.give(inter.author.id, 924293465997705286, bet)
        else:
            em = disnake.Embed(
                color = 0xff0000,
                title = "Tie",
                description = f"you get your {bet} coins back"
            )
            await inter.send(embed = em)


def setup(client):
    client.add_cog(Games(client))
