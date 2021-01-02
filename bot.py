import discord
from discord.ext import commands, tasks
import os
from os import path
import random
import youtube_dl
import asyncio

last_song_name = "empty"
coloring = ("css", 'diff', 'fix', 'json', 'ini', 'cs', 'tex')

client = commands.Bot(command_prefix=commands.when_mentioned_or("."), description='Welcome to club \' Underground Novo Selo\'' )  # bot client holds the bot.

#######################################################################################################
youtube_dl.utils.bug_reports_message = lambda: ''
ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': './cached_music/%(extractor)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0',  # bind to ipv4 since ipv6 addresses cause issues sometimes\
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)


class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=1): # volume = 0.5
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))
        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]
        webpage_url = data.get('webpage_url')

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data), webpage_url

########################################################################################################




@client.command()
async def join(ctx):
        """Joins a voice channel"""
        if ctx.guild.voice_client is None:
            await ctx.author.voice.channel.connect()
        else:
            await ctx.voice_client.move_to(ctx.author.voice.channel)

@client.command()
async def leave(ctx):
    await ctx.channel.purge(limit=1)
    voice_client = ctx.guild.voice_client
    if voice_client is not None:
        await voice_client.disconnect()
        return
    return   # the bot is currently not active in the given server.

@client.event
async def on_member_join(member):
    channel = discord.utils.get(member.guild.channels, name="general")
    await channel.send (f'**{member}** Влезе в holywood (͡o‿O͡)')


@client.command(name='ping', help='This command returns the latency')
async def ping(ctx):
    await ctx.send(f'**Pong** `Latency :{round(client.latency * 1000)} ms.`')


@client.command(aliases=["p"])
async def play(ctx, *, query=None):
    await ctx.channel.purge(limit=1)
    if ctx.author.voice is not None:
        if query is None:
            await ctx.channel.send('Give me a song to look for �')
            return
        else:
            voice_channel = ctx.author.voice.channel
            if ctx.voice_client is None:
                vc = await voice_channel.connect()
            else:
                await ctx.voice_client.move_to(voice_channel)
                vc = ctx.voice_client
            async with ctx.typing():
                global last_song_name
                player, url = await YTDLSource.from_url(query, loop=client.loop)
                last_song_name = url #cache the last soung for .pl command
                vc.play(player, after=lambda e: print("Player err %s" %e) if e else None)
                mention = ctx.author.mention
                await ctx.send(f'>>> Now playing :\n```{random.choice(coloring)}\n [{player.title}]```\n {url} {mention}')
                # await asyncio.sleep(5)
                # await vc.disconnect()
    else:
        await ctx.channel.send("You must be in a voice channel")
        return


@client.command()
async def skip(ctx):
    pass ##todo


@client.command(aliases=['PR', 'playrandom'])
async def pr(ctx):
    await ctx.channel.send('Currently Disabled')
    return


@client.command(help='This command plays the last soung played')
async def pl(ctx):
    if ctx.author.voice is not None:
        if last_song_name == "empty":
            await ctx.channel.send('Looks like the bot just started up and ther are is no hisotry')
            return
        else:
            await ctx.channel.purge(limit=1)
            voice_channel = ctx.author.voice.channel
            if ctx.voice_client is None:
                vc = await voice_channel.connect()
            else:
                await ctx.voice_client.move_to(voice_channel)
                vc = ctx.voice_client
            async with ctx.typing():
                player, url = await YTDLSource.from_url(last_song_name, loop=client.loop)
                vc.play(player, after=lambda e: print("Player err %s" %e) if e else None)
                mention = ctx.author.mention
                await ctx.send(f'>>> Now playing :\n```{random.choice(coloring)}\n [{player.title}]```\n {url} {mention}')
    else:
        await ctx.channel.send("You must be in a voice channel")
        return

"Only people with the role of \"Novoselec\" can use this command"
@client.command(aliases=["c","clean"],help='This command clears messages in the current text channel [USE WITH CAUTION]')
@commands.has_role("Novoselec")
async def clear(ctx, *, amount=0):
    if amount == 0 or amount == 1:
        amount = 2
    elif amount > 50:
        await ctx.channel.send("Cannot delete more than 50 at once")
        return
    elif amount >= 2:
        amount+=1
    await ctx.channel.purge(limit=amount)  # limit = amount




@ client.command(aliases=['plzmeme', 'mem'])
async def meme(ctx):
    await ctx.channel.send('Currently Disabled')
    return
    # await ctx.channel.purge(limit=1)
    # await ctx.channel.send(file=discord.File(".\\memes\\" + random.choice(os.listdir(".\\memes\\"))))


@ client.command()
async def hentai(ctx):
    await ctx.channel.send('Currently Disabled')
    return
    # await ctx.channel.purge(limit=1)
    # await ctx.channel.send(file=discord.File("nani.jpg"))

@client.event
async def on_ready():
    active = discord.Activity(
        type=discord.ActivityType.listening, name="The sound of code")
    await client.change_presence(status=discord.Status.do_not_disturb, activity=active)
    print('Bot is ready.')

client.run('')