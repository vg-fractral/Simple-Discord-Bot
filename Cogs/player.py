import discord
from discord.ext import commands
from asyncio import get_event_loop
from youtube_dl import YoutubeDL


class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, query, *, loop=None):
        loop = loop or get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(query, download=False))
        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        youtube_url = data.get('webpage_url')
        author = data.get("uploader")
        audio_stream_url = data['url']
        views = data.get("view_count")
        thumnail_url = data.get("thumbnail")
        return cls(discord.FFmpegPCMAudio(audio_stream_url, **FFMPEG_OPTIONS),
                   data=data), youtube_url, author, thumnail_url, views


ytdl_format_options = {
    'format': "bestaudio",
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
ytdl = YoutubeDL(ytdl_format_options)
FFMPEG_OPTIONS = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn'
}


class Player(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.volume = 0.5
        self.last_song = None
        self.bot_voice_client = None
        self.player = None

    @commands.command(aliases=["p"], help="This command plays music from youtube", name="Play")
    async def play(self, ctx, *, query=None):
        """PLay a song from YouTube-DL"""
        self.last_song = query
        txt_channel = ctx.channel
        embed_object = discord.Embed(colour=discord.Colour.dark_purple(), type="rich")
        if query is None:
            embed_object.title = "Please give me something to look for :mag_right:"
            await txt_channel.send(embed=embed_object)
            return
        else:
            await self.join(ctx)
            if ctx.author.voice is None:
                return
            self.bot_voice_client = ctx.voice_client
            async with ctx.typing():
                self.player, webpage_url, author, thumbnail_url, views = await YTDLSource.from_url(query)
                self.bot_voice_client.play(self.player, after=lambda e: print("Player err %s" % e) if e else None)
                self.player.volume = self.volume
                embed_object.description = (f"**{author}**  ==> {views:,}")
                embed_object.title = self.player.title
                embed_object.set_image(url=thumbnail_url)
                embed_object.url = webpage_url
                await txt_channel.send(embed=embed_object)

    @commands.command(help='This command replays the last song that has been played', aliases=["re", "pl", "rp"], name="Replay")
    async def replay(self, ctx):
        await self.play(ctx, query=self.last_song)

    @commands.command(help="This command makes the bot join your voice channel", aliases=["j"], name="Join")
    async def join(self, ctx):
        """Joins a voice channel"""
        embed_object = discord.Embed(colour=discord.Colour.dark_purple(), type="rich")
        bot_vc = ctx.guild.voice_client or None
        user_vc = ctx.author.voice or None
        txt_channel = ctx.channel
        await txt_channel.purge(limit=1)
        if user_vc:
            if bot_vc is None:
                await user_vc.channel.connect()
                return
            else:
                await bot_vc.move_to(user_vc.channel)
                return
        else:
            embed_object.title = "You must be in a voice channel"
            await txt_channel.send(embed=embed_object)
            return

    @commands.command(help="This command controls the bot's volume", aliases=["v", "vol"], name="Volume")
    async def volume(self, ctx, *, volume=None):
        embed_object = discord.Embed(colour=discord.Colour.dark_purple(), type="rich")
        if volume is None:
            embed_object.title = f"The volume is {self.volume*100:g}%"
            await ctx.channel.send(embed=embed_object)
            return
        volume = float(volume)
        if ((volume - 0) * (volume-130)) <= 0:
            self.volume = float(volume / 100)
            if self.player:
                self.player.volume = self.volume
            embed_object.title = f"The volume is now {volume:g}%"
            await ctx.channel.send(embed=embed_object)
        else:
            embed_object.title =f"The volume cannot be {volume:g}\n The volume must be within the range of 0 - 130"
            await ctx.channel.send(embed=embed_object)

    @commands.command(aliases=["s"], help="This command stops the audio player of the bot", name="Stop")
    async def stop(self, ctx):
        if self.bot_voice_client and self.bot_voice_client.is_playing():
            self.bot_voice_client.stop()
        else:
            embed_object = discord.Embed(colour=discord.Colour.dark_purple(), type="rich",
                                         title="The bot is not playing at the moment")
            await ctx.channel.send(embed=embed_object)


    @commands.command()
    async def que(self):
        pass

    @commands.Cog.listener()
    async def on_ready(self):
        print("play cog loaded")


def setup(client):
    client.add_cog(Player(client))
