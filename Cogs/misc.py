from discord.ext import commands
from random import choice
from discord import File


class Misc(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(help="Are you going to dare?", name="Hentai", aliases=["h"])
    async def hentai(self, ctx):
        await ctx.channel.purge(limit=1)
        await ctx.channel.send(file=File(choice(["./why.png", "nani.jpg"])))

    @commands.Cog.listener()
    async def on_ready(self):
        print("Misc cog loaded")


def setup(client):
    client.add_cog(Misc(client))