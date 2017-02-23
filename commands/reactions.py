from discord.ext import commands

class Reactions():
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ropestore(self):
        """Kill yourselve."""
        await self.bot.say("http://ropestore.org")

    @commands.command(pass_context=True)
    async def rekt(self, ctx):
        """#REKT"""
        await self.bot.send_typing(ctx.message.channel)
        await self.bot.send_file(ctx.message.channel, "assets/imgs/reactions/rekt.gif")

    @commands.command(pass_context=True)
    async def roasted(self, ctx):
        """MY NIGGA YOU JUST GOT ROASTED!"""
        await self.bot.send_typing(ctx.message.channel)
        await self.bot.send_file(ctx.message.channel, "assets/imgs/reactions/roasted.gif")

    @commands.command(pass_context=True)
    async def tableflip(self, ctx):
        # I hope this unicode doesn't break
        """(╯°□°）╯︵ ┻━┻"""
        await self.bot.send_typing(ctx.message.channel)
        await self.bot.send_file(ctx.message.channel, "assets/imgs/reactions/tableflip.gif")

    @commands.command(pass_context=True)
    async def unflip(self, ctx):
        # I hope this unicode doesn't break
        """┬─┬﻿ ノ( ゜-゜ノ)"""
        await self.bot.send_typing(ctx.message.channel)
        await self.bot.send_file(ctx.message.channel, "assets/imgs/reactions/unflip.gif")

    @commands.command(pass_context=True)
    async def triggered(self, ctx):
        """DID YOU JUST ASSUME MY GENDER? *TRIGGERED*"""
        await self.bot.send_typing(ctx.message.channel)
        await self.bot.send_file(ctx.message.channel, "assets/imgs/reactions/triggered.gif")

    @commands.command(pass_context=True)
    async def delet(self, ctx):
        """Delet this"""
        await self.bot.send_typing(ctx.message.channel)
        await self.bot.send_file(ctx.message.channel, "assets/imgs/reactions/delet_this.jpg")

    @commands.command(pass_context=True)
    async def what(self, ctx):
        """what?"""
        await self.bot.send_typing(ctx.message.channel)
        await self.bot.send_file(ctx.message.channel, "assets/imgs/reactions/what.gif")

    @commands.command(pass_context=True)
    async def weirdshit(self, ctx):
        """WHY ARE YOU POSTING WEIRD SHIT?!?!?!"""
        await self.bot.send_typing(ctx.message.channel)
        await self.bot.send_file(ctx.message.channel, "assets/imgs/reactions/weirdshit.jpg")

    @commands.command(pass_context=True)
    async def filth(self, ctx):
        """THIS IS ABSOLUTELY FILTHY!"""
        await self.bot.send_typing(ctx.message.channel)
        await self.bot.send_file(ctx.message.channel, "assets/imgs/reactions/filth.gif")

    @commands.command(pass_context=True)
    async def heckoff(self, ctx):
        """heck off fools"""
        await self.bot.send_typing(ctx.message.channel)
        await self.bot.send_file(ctx.message.channel, "assets/imgs/reactions/heckoff.png")

def setup(bot):
    bot.add_cog(Reactions(bot))
