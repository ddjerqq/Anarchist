import discord
from discord.ext import commands


class Information(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name="help")
    async def _help_command(self, ctx, _type: str = None):
        em = discord.Embed(title="Categories", color=0x00ff00)
        em.set_footer(
            text="type `.help [category] for help with a specific category or command`"
        )
        if not _type:
            em.set_author(name="Help")
            categories = "**Currency**\n**Information**"
            em.description = categories
        elif _type.lower() == "currency":
            em.title = "Currency Commands"
            currency_commands = [
                "**Balance**",
                "**Work**",
                "**Give**",
            ]
            currency_commands = ", ".join(currency_commands)
            em.description = currency_commands
        await ctx.send(embed=em)

    @commands.command(name="info")
    async def _info(self, ctx: commands.Context, user: discord.Member = None):
        if not user:
            user = ctx.author

        embed: discord.Embed = discord.Embed(
            title = f"{user.name}#{user.discriminator}'s info", 
            color = 0x00ff00
        )
        embed.add_field(
            name="creation time", 
            value=str(user.created_at), 
            inline=False)
        embed.add_field(
            name="id", 
            value=user.id, 
            inline=False)
        embed.add_field(
            name="is bot?", 
            value=user.bot, 
            inline=False)
        embed.set_image(
            url = user.avatar_url)

        await ctx.send(embed=embed)

    @commands.command(name = "invite", aliases = ["inv"])
    async def _invite(self, ctx: commands.Context):
        embed = discord.Embed(
            title = "Click me to Invite!", 
            url = "https://discord.com/api/oauth2/authorize?client_id=924293465997705286&permissions=275884665968&scope=bot"
            )
        embed.set_author(
            name = self.client.user, 
            icon_url = self.client.user.avatar_url
            )
        await ctx.reply(embed = embed)

def setup(client: discord.Client):
    client.add_cog(Information(client))
