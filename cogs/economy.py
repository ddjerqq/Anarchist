import discord
from discord.ext import commands

from database import database

class Economy(commands.Cog):
    def __init__(self, client: discord.Client):
        self.client = client

    @commands.command(name = "give")
    async def give(self, ctx: commands.Context, user: discord.Member, amount: str) -> None:
        _id = user.id
        if amount.lower() == "all" or amount.lower() == "max":
            amount = database[ctx.author.id]["amount"]
        else:
            if int(amount) > 0:
                amount = int(amount)
            else:
                embed = discord.Embed( 
                    color = 0xff0000, 
                    title = f"what are you trying to do here 🤨⁉"
                )
                await ctx.send(embed = embed)
                return

        if database.give(ctx.author.id, _id, amount):
            embed = discord.Embed( 
                color = 0xff0000, 
                title = f"you successfully gave {database[_id]['name']} {amount} ⏣"
                )
            # embed2 = discord.Embed(
            #     color = 0xff0000, 
            #     title = f"{database[ctx.author.id]['name']} gave you {amount} coins"
            #     )
            # await dm_user(_id, embed = embed2)
        else:
            embed = discord.Embed( 
                color = 0xff0000, 
                title = f"you don't have enough money dumbass"
                )

        await ctx.send( embed = embed )

    @commands.command(name = "work")
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def work(self, ctx: commands.Context) -> None:
        database.work(ctx.author.id)
        embed = discord.Embed( 
            color = 0xff0000, 
            title = f"nice work! \nyou earned 25 ⏣"
            )
        await ctx.send( embed = embed )

    @commands.command(name = "bal", aliases = ["balanace"])
    async def balance(self, ctx: commands.Context, user: discord.Member = None) -> None:
        if not user: user = ctx.author
        _id = user.id
        
        embed = discord.Embed( 
            color = 0xff0000, 
            title = f"{database[_id]['name']}'s balance" 
            )
        embed.add_field(
            name = "total amount",
            value = f"{database[_id]['amount']} ⏣",
            inline = False 
            )
        await ctx.send( embed = embed )

def setup(client: discord.Client):
    client.add_cog(Economy(client))