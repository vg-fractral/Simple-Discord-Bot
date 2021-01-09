from asyncio import get_event_loop
import discord
from discord.ext import commands
from youtube_dl import YoutubeDL


purple = discord.Colour.dark_purple()


class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.3):
        super().__init__(source, volume)
        self.data = data

    @classmethod
    async def from_url(cls, query, volume):
        loop = get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(query, download=False))
        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        youtube_url = data.get('webpage_url')
        author = data.get("uploader")
        audio_stream_url = data['url']
        thumbnail_url = data.get("thumbnail")
        title = data.get("title")

        embed_template = discord.Embed(colour=purple, type="rich", description=f"**{author}**",
                                       url=youtube_url, title=title)
        embed_template.set_image(url=thumbnail_url)

        return cls(discord.FFmpegPCMAudio(audio_stream_url, **FFMPEG_OPTIONS), data=data, volume=volume), embed_template


YTDL_FORMAT_OPTIONS = {
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
ytdl = YoutubeDL(YTDL_FORMAT_OPTIONS)
FFMPEG_OPTIONS = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn'
}


class Player(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.volume = 0.3
        self.last_song = None
        self.b_vc = None
        self.player = None

    @commands.command(aliases=["p"], help="This command plays music from youtube", name="Play")
    async def play(self, ctx, *, query=None):
        """PLay a song from YouTube-DL"""
        txt_channel = ctx.channel
        embed_object = discord.Embed(colour=purple, type="rich")
        if query is None:
            embed_object.title = "Please give me something to look for :mag_right:"
            await txt_channel.send(embed=embed_object)
            return
        else:
            await self.join(ctx)
            if ctx.author.voice is None:
                return
            self.last_song = query
            self.b_vc = ctx.voice_client
            async with ctx.typing():
                self.player, youtube_embed = await YTDLSource.from_url(query, volume=self.volume)
                self.b_vc.play(self.player, after=lambda e: print(f"Player err {e}") if e else None)
                await txt_channel.send(embed=youtube_embed)

    @commands.command(help='This command replays the last song that has been played', aliases=["re", "pl", "rp"],
                      name="Replay")
    async def replay(self, ctx):
        await self.play(ctx, query=self.last_song)

    @commands.command(help="This command makes the bot join your voice channel", aliases=["j"], name="Join")
    async def join(self, ctx):
        """Joins a voice channel"""
        embed_object = discord.Embed(colour=purple, type="rich")
        u_vc = ctx.author.voice or None
        txt_channel = ctx.channel
        await txt_channel.purge(limit=1)
        if u_vc:
            await u_vc.channel.connect()
            return
        else:
            embed_object.title = "You must be in a voice channel"
            await txt_channel.send(embed=embed_object)
            return

    @commands.command(help="This command controls the bot's volume", aliases=["v", "vol"], name="Volume")
    async def volume(self, ctx, *, volume=None):
        txt_channel = ctx.channel
        await txt_channel.purge(limit=1)
        embed_object = discord.Embed(colour=purple, type="rich")
        if volume is None:
            embed_object.title = f"The volume is {self.volume * 100:g}%"
            await txt_channel.send(embed=embed_object)
            return
        try:
            volume = float(volume)
        except Exception:
            embed_object.title=f"The volume cannot be \"{volume}\""
            txt_channel.send(embed=embed_object)
            return
        if ((volume - 0) * (volume - 130)) <= 0:
            self.volume = float(volume / 100)
            if self.player:
                self.player.volume = self.volume
            embed_object.title = f"The volume is now {volume:g}%"
            await txt_channel.send(embed=embed_object)
        else:
            embed_object.title = f"The volume cannot be {volume:g}\nThe volume must be within the range of 0 - 130"
            await txt_channel.send(embed=embed_object)

    @commands.command(aliases=["s"], help="This command stops the audio player of the bot", name="Stop")
    async def stop(self, ctx):
        if self.b_vc and self.b_vc.is_playing():
            self.b_vc.stop()
        else:
            embed_object = discord.Embed(colour=purple, type="rich", title="The bot is not playing at the moment")
            await ctx.channel.send(embed=embed_object)

    @commands.Cog.listener()
    async def on_ready(self):
        print("play cog loaded")


def setup(client):
    client.add_cog(Player(client))
