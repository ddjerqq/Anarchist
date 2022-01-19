import disnake
from disnake.ext import commands
from disnake import ApplicationCommandInteraction
from disnake.ext.commands import errors

from __main__ import GUILD_IDS
from __main__ import PREFIX

from database import database
from supersecrets import salt

class Information(commands.Cog):
    def __init__(self, client: disnake.client.Client):
        self.client = client

    @commands.slash_command(
        name        = "blockchain", 
        aliases     = ["valid"],
        description = "check if the blockchain is valid",
        #guild_ids   = GUILD_IDS
        )
    async def _blockchain(self, inter: ApplicationCommandInteraction):
        em = disnake.Embed(title="is Blockchain valid?")

        if database.is_blockchain_valid:
            em.description = "**Yes**"
            em.color = 0x00ff00
        else:
            em.description = "**No!!!**"
            em.color = 0xff0000

        await inter.send(embed = em)


    @commands.slash_command(
        name        = "invite", 
        aliases     = ["inv"],
        description = "gives you the link to invite the bot to your server",
        #guild_ids   = GUILD_IDS
        )
    async def _invite(self, inter: ApplicationCommandInteraction):
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
    async def _ping(self, inter: ApplicationCommandInteraction):
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
    async def _notifications(self, inter: ApplicationCommandInteraction):
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
        description = "set password to use for authentication"
    )
    async def _password(self, inter: ApplicationCommandInteraction, password: str = None) -> None:
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
            await inter.reply(embed = change_pw_em)
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
    async def _change(self, inter: ApplicationCommandInteraction, old_password: str, new_password: str) -> None:        
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