import os
from dotenv import load_dotenv
import discord
from discord.ext import commands

triple_curly = "```"

"""Load the .env file into the Environment variables"""
load_dotenv(".env")


client = commands.Bot(command_prefix=commands.when_mentioned_or("."),
                      description='Welcome to club Novo Selo Underground')

for filename in os.listdir("./Cogs"):
    if filename.endswith(".py"):
        client.load_extension(f"Cogs.{filename[:-3]}")


@client.event
async def on_ready():
    active = discord.Activity(
        type=discord.ActivityType.listening, name="The sound of code")
    await client.change_presence(status=discord.Status.do_not_disturb, activity=active)
    print('Bot is ready.')


client.run(os.getenv("BOT_TOKEN"))
