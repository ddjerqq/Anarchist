import disnake
from disnake.ext import commands
from disnake import ApplicationCommandInteraction as Aci

# from __main__ import GUILD_IDS
from easydb import database
from supersecrets import password_hash, check_password
from models.user import User
from models.block import Block


class Information(commands.Cog):
    def __init__(self, client: disnake.client.Client):
        self.client = client

    @commands.slash_command(
        name        = "leaderboard", 
        description = "Get the top 15 users worldwide",
        # guild_ids   = GUILD_IDS
        )
    async def _leaderboard(self, inter: Aci):
        em = disnake.Embed(
            title=f"Global leaderboard",
            color=0x00FF00,
        )

        with database as c:
            c.execute("""
            SELECT username, money FROM users
            WHERE id<>924293465997705286
            ORDER BY money DESC
            LIMIT 16
            """)
            top15 = c.fetchall()

        for index, user in enumerate(top15):
            em.add_field(
                name   = f"#{index} {user[0]}",
                value  = f"{user[1]} coins",
                inline = False,
            )
        await inter.send(embed=em)
    
    @commands.slash_command(
        name        = "block",
        description = "Get the most recent block",
        # guild_ids   = GUILD_IDS
    )
    async def _block(self, inter: Aci, *, block_id: int = None):
        if block_id is not None:
            block = Block.from_index(block_id, database)
            if block is None:
                block = Block.last_block(database)
        else:
            with database as c:
                c.execute("""
                SELECT * FROM blockchain
                WHERE id=(SELECT MAX(id) FROM blockchain)
                """)
                block = Block.from_db(c.fetchone())

        em = disnake.Embed(
            title = f"Block #{block.index}",
            color = 0x00ff00
        )
        em.add_field(
            name = "Sender",
            value = f"Name: {database[block.sender_id].username} \n`ID: {block.sender_id}`",
            inline = True
        )
        em.add_field(
            name = "Receiver",
            value = f"Name: {database[block.receiver_id].username} \n`ID: {block.sender_id}`",
            inline = True
        )
        em.add_field(
            name = "Amount",
            value = f"{block.amount} coins",
            inline = True
        )
        em.add_field(
            name = "Previous hash",
            value = f"`{block.previous_hash}`",
            inline = False
        )
        em.set_footer(
            text = "Timestamp:  " + block.timestamp
        )

        await inter.send(embed = em)

    @commands.slash_command(
        name        = "help",
        description = "get help for commands",
        # guild_ids   = GUILD_IDS
    )
    async def _help(self, inter: Aci):
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
        # guild_ids   = GUILD_IDS
        )
    async def _invite(self, inter: Aci):
        em = disnake.Embed(
            title = "Click me to invite!",
            url   = "https://discord.com/api/oauth2/authorize?client_id=924293465997705286&permissions=277025507392&scope=bot%20applications.commands",
        )
        em.set_author(name=self.client.user, icon_url=self.client.user.avatar.url)
        await inter.send(embed=em)
    
    @commands.slash_command(
        name        = "ping", 
        description = "measure bot latency",
        # guild_ids   = GUILD_IDS
        )
    async def _ping(self, inter: Aci):
        latency = round(self.client.latency * 1000)

        match latency:
            case _ if latency < 50:
                color = 0x00ff00
            case _ if latency < 100:
                color = 0x439e16
            case _ if latency < 250:
                color = 0x759e16
            case _ if latency < 500:
                color = 0xbd8215
            case _ if latency < 750:
                color = 0xcf380e
            case _:
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
        # guild_ids   = GUILD_IDS
        )
    async def _notifications(self, inter: Aci):
        disable = disnake.Embed(
            title = "Notifications disabled ❌",
            color = 0xff0000
        )
        enable = disnake.Embed(
            title = "Notifications enabled ✅",
            color = 0x00ff00
        )

        with database as c:
            c.execute("""
            SELECT notifications FROM users
            WHERE id=?
            """, (inter.author.id,))
            notifications = c.fetchone()[0]

            if notifications == 1:
                await inter.send(embed = disable)
                c.execute("""
                UPDATE users SET notifications=0
                WHERE id=?
                """, (inter.author.id,))
            else:
                c.execute("""
                UPDATE users SET notifications=1
                WHERE id=?
                """, (inter.author.id,))
                await inter.send(embed = enable)

    @commands.slash_command(
        name = "password",
        description = "set a password to use for authentication, **we do not store your passwords**"
    )
    async def _password(self, inter: Aci, password: str = None):
        no_password_em = disnake.Embed(
                title = "missing required argument password ❌",
                color = 0xff0000,
                description = f"to set your password use /password your password"
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
            description = f"if you want to change it, use /change old new"
            )

        if database[inter.author.id].authentication:
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
            invalid_pw_em.description += "password should have at least one **number**\n"
        if not any(char.isupper() for char in password):
            valid = False
            invalid_pw_em.description += "password should have at least **one uppercase** letter\n"
        if not any(char.islower() for char in password):
            valid = False
            invalid_pw_em.description += "password should have at least one **lowercase** letter\n"
        if not valid:
            await inter.send(embed = invalid_pw_em)
            return
        else:
            with database as c:
                c.execute("""
                UPDATE users SET authorization=?
                WHERE id=?
                """, (password_hash(password), inter.author.id))
            await inter.send(embed = success_set_em)

    @commands.slash_command(
        name = "change",
        description = "change password"
    )
    async def _change(self, inter: Aci, old_password: str, new_password: str):
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

        with database as c:
            c.execute("""
            SELECT authorization FROM users
            WHERE id=?
            """, (inter.author.id,))
            user_pw_hash = c.fetchone()[0]

        if check_password(user_pw_hash, old_password):
            valid = True
            if len(new_password) < 8:
                valid = False
                invalid_pw_em.description += "password should be **at least 8** characters\n"
            if len(new_password) > 32:
                valid = False
                invalid_pw_em.description += "password should **not** be **more than 32 characters**\n"
            if not any(char.isdigit() for char in new_password):
                valid = False
                invalid_pw_em.description += "password should have at least one **number**\n"
            if not any(char.isupper() for char in new_password):
                valid = False
                invalid_pw_em.description += "password should have at least **one uppercase** letter\n"
            if not any(char.islower() for char in new_password):
                valid = False
                invalid_pw_em.description += "password should have at least one **lowercase** letter\n"
            if not valid:
                await inter.send(embed = invalid_pw_em)
                return
            else:
                with database as c:
                    c.execute("""
                    UPDATE users SET authorization=?
                    WHERE id=?
                    """, (password_hash(new_password), inter.author.id))
                await inter.send(embed = success_em)
        else:
            await inter.send(embed = fail_em)


def setup(client):
    client.add_cog(Information(client))
