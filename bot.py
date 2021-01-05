import os
import discord
from discord.ext import commands
from random import choice



client = commands.Bot(command_prefix=commands.when_mentioned_or("."),
                      description='Welcome to club \' Novo Selo Underground\'')


@client.command()
async def load(ctx, ext):
    client.load_extension(f"Cogs.{ext}")


@client.command()
async def unload(ctx, ext):
    client.unload_extension(f"Cogs.{ext}")

for filename in os.listdir("./Cogs"):
    if filename.endswith(".py"):
        client.load_extension(f"Cogs.{filename[:-3]}")

# @client.command(name="leave", help="This command makes the bot leave your voice channel", aliases=["l"])
# async def leave(ctx):
#     """Leaves a voice channel"""
#     await ctx.channel.purge(limit=1)
#     vc = ctx.guild.voice_client
#     if vc is None:
#         return
#     else:
#         await vc.disconnect()

# @client.command(name="join", help="This command makes the bot join your voice channel", aliases=["j"])
# async def join(ctx, embed_object):
#     """Joins a voice channel"""
#     await ctx.channel.purge(limit=1)
#     vc = ctx.guild.voice_client
#     channel = ctx.author.voice.channel
#     if channel:
#         if vc is None:
#             await channel.connect()
#         else:
#             await vc.move_to(channel)
#     else:
#         embed_object.title = "You must be in a voice channel"
#         await channel.send(embed=embed_object)
#         return
#




#
# @client.command(help="This command controls the bot's volume", aliases=["v", "vol"], name="Volume")
# async def volume(ctx, *, volume):
#     global initial_volume
#     volume = float(volume)
#     if ((0 - volume) * (200 - volume)) <= 0:
#         new_volume = float(volume / 100)
#         player.volume = new_volume
#         initial_volume = new_volume
#         await ctx.channel.send(f"The volume is now {volume:g}%")
#     else:
#         await ctx.channel.send(f"The volume cannot be {volume:g}")
#

@client.command()
async def stop(ctx):
    vc = ctx.voice_client
    vc.stop()


"Only people with the role of \"Novoselec\" can use this command"


@client.command(aliases=["c", "clean"],
                help='This command clears messages in the current text channel [USE WITH CAUTION]')
@commands.has_any_role("Novoselec", "Popa")
async def clear(ctx, *, amount=0):
    if amount == 0 or amount == 1:
        amount = 2
    elif amount > 50:
        await ctx.channel.send("Cannot delete more than 50 at once")
        return
    elif amount >= 2:
        amount += 1
    await ctx.channel.purge(limit=amount)  # limit = amount


@client.command(aliases=['plzmeme', 'mem'])
async def meme(ctx):
    await ctx.channel.send('Currently Disabled')
    return
    # await ctx.channel.purge(limit=1)
    # await ctx.channel.send(file=discord.File(".\\memes\\" + random.choice(os.listdir(".\\memes\\"))))


@client.command()
async def hentai(ctx):
    # await ctx.channel.send('Currently Disabled')
    # return
    await ctx.channel.purge(limit=1)
    await ctx.channel.send(file=discord.File(choice(["./why.png", "nani.jpg"])))


@client.event
async def on_ready():
    active = discord.Activity(
        type=discord.ActivityType.listening, name="The sound of code")
    await client.change_presence(status=discord.Status.do_not_disturb, activity=active)
    print('Bot is ready.')


client.run('Nzg2OTM1MjU1NTAwMDYyNzMw.X9NokQ.Uyhi-aNcmJmshZVIBtDt460HxU8')
