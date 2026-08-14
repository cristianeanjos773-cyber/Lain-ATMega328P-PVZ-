import discord 
from discord.ext import commands

async def SendEmbed(ctx: commands.Context[commands.Bot], title: str, description: str, color: discord.Color, url: str | None):
        embed = discord.Embed(title=title, description=description, color=color)

        if url:
            embed.set_image(url=url)
            print(url)

        await ctx.send(embed=embed)