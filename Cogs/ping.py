from discord.ext import commands


class Dev(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name='ping', help='This command returns the latency')
    async def ping(self, ctx):
        await ctx.send(f'**Pong** `Latency :{round(self.client.latency * 1000)} ms.`')

    @commands.Cog.listener()
    async def on_ready(self):
        print("Ping cog loaded")


def setup(client):
    client.add_cog(Dev(client))