from discord.ext import commands

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def help(self, ctx, *cogs):
        """Gives the link to the bot docs"""
        await ctx.send("For help with the bot, visit https://deadhead.scripthead.me")

def setup(bot):
    bot.add_cog(Help(bot))
