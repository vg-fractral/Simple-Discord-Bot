from discord.ext import commands


class Clear(commands.Cog):
    def __int__(self, client):
        self.client = client

    @commands.command(aliases=["c", "clean"],
                    help='This command clears messages [USE WITH CAUTION]')
    @commands.has_any_role("Novoselec", "Popa")
    async def clear(self, ctx, *, amount=0):
        if amount == 0 or amount == 1:
            amount = 2
        elif amount > 50:
            await ctx.channel.send("Cannot delete more than 50 at once")
            return
        elif amount >= 2:
            amount += 1
        await ctx.channel.purge(limit=amount)  # limit = amount



def setup(client):
    client.add_cog(Clear(client))
