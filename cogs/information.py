import disnake
from disnake.ext import commands
from disnake import ApplicationCommandInteraction

from __main__ import GUILD_IDS

from database import database


class Information(commands.Cog):
    def __init__(self, client: disnake.client.Client):
        self.client = client

    @commands.slash_command(
        name        = "blockchain", 
        aliases     = ["valid"],
        description = "check if the blockchain is valid",
        guild_ids   = GUILD_IDS
        )
    async def _blockchain(self, inter: ApplicationCommandInteraction):
        em = disnake.Embed(title="is Blockchain valid?")

        if database.is_blockchain_valid:
            em.description = "**Yes**"
            em.color = 0x34ab0c
        else:
            em.description = "**No!!!**"
            em.color = 0xab2f0c

        await inter.send(embed = em)


    @commands.slash_command(
        name        = "invite", 
        aliases     = ["inv"],
        description = "gives you the link to invite the bot to your server",
        guild_ids   = GUILD_IDS
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
        guild_ids   = GUILD_IDS
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
        guild_ids   = GUILD_IDS
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

def setup(client: disnake.Client):
    client.add_cog(Information(client))