from datetime import datetime

import disnake
from disnake.ext import commands
from disnake import ApplicationCommandInteraction as ACI
from disnake.ext.commands import errors

from __main__ import GUILD_IDS
from __main__ import PREFIX
from helpers.bot_helper import embed_from_block
from database import database
from supersecrets import salt

class Information(commands.Cog):
    def __init__(self, client: disnake.client.Client):
        self.client = client

    @commands.slash_command(
        name        = "rank", 
        description = "Get the top 10 users in this server",
        #guild_ids   = GUILD_IDS
        )
    async def _rank(self, inter: ACI):
        users = []
        async for user in inter.guild.fetch_members(limit=None):
            if not user.bot:
                users.append(database[user.id])

        sorted_users = sorted(users, key=lambda x: x.amount, reverse=True)[0:10]

        em = disnake.Embed(
            title=f"{inter.guild.name} leaderboard",
            color=0x00FF00,
        )
        for index, user in enumerate(sorted_users):
            em.add_field(
                name   = f"#{index + 1} {user.name}",
                value  = f"{user.amount} ⏣",
                inline = False,
            )
        await inter.send(embed=em)

    @commands.slash_command(
        name        = "leaderboard", 
        description = "Get the top 10 users globally",
        #guild_ids   = GUILD_IDS
        )
    async def _leaderboard(self, inter: ACI):
        sorted_users = sorted(database.users, key = lambda x: x.amount, reverse=True)[0:11]
        em = disnake.Embed(
            title=f"Global leaderboard",
            color=0x00FF00,
        )
        for index, user in enumerate(sorted_users):
            if not index: continue #skip bank user
            em.add_field(
                name   = f"#{index} {user.name}",
                value  = f"{user.amount} ⏣",
                inline = False,
            )
        await inter.send(embed=em)
    
    @commands.slash_command(
        name        = "block",
        description = "Get the most recent block, or provide an ID",
        #guild_ids   = GUILD_IDS
    )
    async def _block(self, inter: ACI, *, block_id: int = None):
        if block_id and block_id < len(database.blockchain):
            block = database.blockchain[block_id]
        else:
            block = database.blockchain[-1]
        em = embed_from_block(block)
        await inter.send(embed = em)

    #TODO GET BLOCK BY ID FOR OPEN FREEDOM LAWS
    @commands.slash_command(
        name        = "help",
        description = "get help for commands",
        #guild_ids   = GUILD_IDS
    )
    async def _help(self, inter: ACI):
        em = disnake.Embed(
            title  = "Anarchist help",
            color  = 0x00ff00
        )
        em.add_field(
            name  = "/bal",
            value = "Get your balance"
        )
        em.add_field(
            name  = "/bal @user",
            value = "Get balance of the given user"
        )
        em.add_field(
            name  = "/give @user amount",
            value = "Give a user an amount of coins"
        )
        em.add_field(
            name  = "/work",
            value = "Work and earn 50 coins. \n(You can only work once a minute)"
        )
        em.add_field(
            name  = "/rank",
            value = "Display the top 10 users in the server"
        )
        em.add_field(
            name  = "/leaderboard",
            value = "Display the top 10 users globally"
        )
        em.add_field(
            name  = "/password password",
            value = "Set a password to use for confirmations\nPlease use this command in bot dms"
        )
        em.add_field(
            name  = "/change old_password new_password",
            value = "change your current password"
        )
        em.add_field(
            name  = "/notifications",
            value = "Toggle notifications"
        )
        em.add_field(
            name  = "/block",
            value = "Get the most recent block"
        )
        em.add_field(
            name  = "/blockchain",
            value = "Get the blockchain status"
        )
        em.add_field(
            name  = "/invite",
            value = "Get a link to invite Anarchist to your server"
        )
        em.add_field(
            name  = "/ping",
            value = "Measure bot latency"
        )


        await inter.send(embed = em)


    @commands.slash_command(
        name        = "invite", 
        description = "gives you the link to invite the bot to your server",
        #guild_ids   = GUILD_IDS
        )
    async def _invite(self, inter: ACI):
        em = disnake.Embed(
            title = "Click me to invite!",
            url   = "https://discord.com/api/oauth2/authorize?client_id=924293465997705286&permissions=277025507392&scope=bot%20applications.commands",
        )
        em.set_author(name=self.client.user, icon_url=self.client.user.avatar.url)
        await inter.send(embed=em)
    
    @commands.slash_command(
        name        = "ping", 
        description = "measure bot latency",
        #guild_ids   = GUILD_IDS
        )
    async def _ping(self, inter: ACI):
        latency = round(self.client.latency * 1000)
        
        if   latency <= 50:
            color = 0x00ff00
        elif latency <= 100:
            color = 0x439e16
        elif latency <= 250:
            color = 0x759e16
        elif latency <= 500:
            color = 0xbd8215
        elif latency <= 750:
            color = 0xcf380e
        else:
            color = 0xff0000
        em = disnake.Embed(
            title = "Pong",
            color = color,
            description = f"latency: {latency}ms"
        )
        await inter.send(embed = em)

    @commands.slash_command(
        name        = "notifications", 
        description = "toggle DM notifications on/off",
        #guild_ids   = GUILD_IDS
        )
    async def _notifications(self, inter: ACI):
        disable = disnake.Embed(
            title = "Notifications disabled ❌",
            color = 0xff0000
        )
        enable = disnake.Embed(
            title = "Notifications enabled ✅",
            color = 0x00ff00
        )
        if database[inter.author.id].notifications:
            database[inter.author.id].notifications = False
            await inter.send(embed = disable)
        else:
            database[inter.author.id].notifications = True
            await inter.send(embed = enable)


    @commands.slash_command(
        name = "password",
        description = "set a password to use for authentication"
    )
    async def _password(self, inter: ACI, password: str = None):
        no_password_em = disnake.Embed(
                title = "missing required argument password ❌",
                color = 0xff0000,
                description = f"to set your password use {PREFIX}password yourpassword"
            )
        invalid_pw_em  = disnake.Embed(
            title = "Invalid password ❌",
            color = 0xff0000,
            description = ""
            )
        success_set_em = disnake.Embed(
            title = "You successfully set your password ✅",
            color = 0x00ff00
            )
        change_pw_em   = disnake.Embed(
            title = "You already have a password set. 🔰",
            color = 0xffff00,
            description = f"if you want to change it, use {PREFIX}change"
            )

        if database[inter.author.id].auth != "0":
            await inter.send(embed = change_pw_em)
            return

        if not password:
            await inter.send(embed = no_password_em)
            return

        valid = True

        if len(password) < 6:
            valid = False
            invalid_pw_em.description += "password should be **at least 8** characters\n"
        if len(password) > 24:
            valid = False
            invalid_pw_em.description += "password should **not** be **more than 32 characters**\n"
        if not any(char.isdigit() for char in password):
            valid = False
            invalid_pw_em.description += "password should have atleast one **number**\n"
        if not any(char.isupper() for char in password):
            valid = False
            invalid_pw_em.description += "password should have atleast **one uppercase** letter\n"
        if not any(char.islower() for char in password):
            valid = False
            invalid_pw_em.description += "password should have atleast one **lowercase** letter\n"
        if not valid:
            await inter.send(embed = invalid_pw_em)
            return
        else:
            database[inter.author.id].auth = salt(password)
            await inter.send(embed = success_set_em)

    @commands.slash_command(
        name = "change",
        description = "change password"
    )
    async def _change(self, inter: ACI, old_password: str, new_password: str):        
        fail_em = disnake.Embed(
            title = "passwords do not match ❌",
            color = 0xff0000
            )
        success_em = disnake.Embed(
            title = "You successfully changed your password ✅",
            color = 0x00ff00
            )
        invalid_pw_em  = disnake.Embed(
            title = "Invalid password ❌",
            color = 0xff0000,
            description = ""
            )

        if salt(old_password) == database[inter.author.id].auth:
            valid = True
            if len(new_password) < 6:
                valid = False
                invalid_pw_em.description += "password should be **at least 8** characters\n"
            if len(new_password) > 24:
                valid = False
                invalid_pw_em.description += "password should **not** be **more than 32 characters**\n"
            if not any(char.isdigit() for char in new_password):
                valid = False
                invalid_pw_em.description += "password should have atleast one **number**\n"
            if not any(char.isupper() for char in new_password):
                valid = False
                invalid_pw_em.description += "password should have atleast **one uppercase** letter\n"
            if not any(char.islower() for char in new_password):
                valid = False
                invalid_pw_em.description += "password should have atleast one **lowercase** letter\n"
            if not valid:
                await inter.send(embed = invalid_pw_em)
                return
            else:
                database[inter.author.id].auth = salt(new_password)
                await inter.send(embed = success_em)
        else:
            await inter.send(embed = fail_em)

def setup(client: disnake.Client):
    client.add_cog(Information(client))