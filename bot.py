import os
import discord
from discord.ext import commands
from random import choice

triple_curly = "```"

client = commands.Bot(command_prefix=commands.when_mentioned_or("."),
                      description='Welcome to club Novo Selo Underground')

for filename in os.listdir("./Cogs"):
    if filename.endswith(".py"):
        client.load_extension(f"Cogs.{filename[:-3]}")


@client.command()
async def hentai(ctx):
    await ctx.channel.purge(limit=1)
    await ctx.channel.send(file=discord.File(choice(["./why.png", "nani.jpg"])))


@client.event
async def on_ready():
    active = discord.Activity(
        type=discord.ActivityType.listening, name="The sound of code")
    await client.change_presence(status=discord.Status.online, activity=active)
    print("Bot is online")


client.run('Nzg2OTM1MjU1NTAwMDYyNzMw.X9NokQ.Uyhi-aNcmJmshZVIBtDt460HxU8')
