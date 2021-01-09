from discord.ext import commands
import bot
import discord
class Code(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(help="This command prints out the source code of the bot")
    async def code(self, ctx, *, request_file=None):
        if request_file is None:
            embed_obj = discord.Embed(colour=discord.Colour.dark_purple(), title=f"Please pass in as an argument the section of the code "
                             "you want to get,\nFor example \".code Dev\" or \".code Player\"\n"
                             f"You can see the different sections in the \".help\" command")
            await ctx.channel.send(embed=embed_obj)

        else:
            try:
                with open(f"Cogs/{request_file}.py") as f:
                    page_list = [""]
                    contents = f.readlines()
                    char_count, page_index = 0, 0
                    for index in range(len(contents)):
                        char_count += len(contents[index])
                        if char_count > 1900:
                            page_index +=1
                            char_count = 0
                            page_list.append(contents[index])
                            continue
                        page_list[page_index] += contents[index]
                for page in page_list:
                    await ctx.channel.send(f"{bot.triple_curly}py\n{page}\n{bot.triple_curly}")
            except FileNotFoundError:
                print("file does not exist")



def setup(client):
    client.add_cog(Code(client))