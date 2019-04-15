import discord

from discord.ext import commands

class Reactions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ropestore(self, ctx):
        """Kill yourselve."""
        await ctx.send("http://ropestore.org")

    @commands.command()
    async def rekt(self, ctx):
        """#REKT"""
        await ctx.channel.trigger_typing()
        await ctx.send(file=discord.File("assets/imgs/reactions/rekt.gif"))

    @commands.command()
    async def roasted(self, ctx):
        """MY NIGGA YOU JUST GOT ROASTED!"""
        await ctx.channel.trigger_typing()
        await ctx.send(file=discord.File("assets/imgs/reactions/roasted.gif"))

    @commands.command()
    async def tableflip(self, ctx):
        # I hope this unicode doesn't break
        """(╯°□°）╯︵ ┻━┻"""
        await ctx.channel.trigger_typing()
        await ctx.send(file=discord.File("assets/imgs/reactions/tableflip.gif"))

    @commands.command()
    async def unflip(self, ctx):
        # I hope this unicode doesn't break
        """┬─┬﻿ ノ( ゜-゜ノ)"""
        await ctx.channel.trigger_typing()
        await ctx.send(file=discord.File("assets/imgs/reactions/unflip.gif"))

    @commands.command()
    async def triggered(self, ctx):
        """DID YOU JUST ASSUME MY GENDER? *TRIGGERED*"""
        await ctx.channel.trigger_typing()
        await ctx.send(file=discord.File("assets/imgs/reactions/triggered.gif"))

    @commands.command()
    async def delet(self, ctx):
        """Delet this"""
        await ctx.channel.trigger_typing()
        await ctx.send(file=discord.File("assets/imgs/reactions/delet_this.png"))

    @commands.command()
    async def what(self, ctx):
        """what?"""
        await ctx.channel.trigger_typing()
        await ctx.send(file=discord.File("assets/imgs/reactions/what.gif"))

    @commands.command()
    async def weirdshit(self, ctx):
        """WHY ARE YOU POSTING WEIRD SHIT?!?!?!"""
        await ctx.channel.trigger_typing()
        await ctx.send(file=discord.File("assets/imgs/reactions/weirdshit.jpg"))

    @commands.command()
    async def filth(self, ctx):
        """THIS IS ABSOLUTELY FILTHY!"""
        await ctx.channel.trigger_typing()
        await ctx.send(file=discord.File("assets/imgs/reactions/filth.gif"))

    @commands.command()
    async def heckoff(self, ctx):
        """heck off fools"""
        await ctx.channel.trigger_typing()
        await ctx.send(file=discord.File("assets/imgs/reactions/heckoff.png"))

    @commands.command()
    async def lewd(self, ctx):
        """WOAH THERE THAT'S LEWD!"""
        await ctx.channel.trigger_typing()
        await ctx.send(file=discord.File("assets/imgs/reactions/lewd.gif"))

    @commands.command()
    async def nolewding(self, ctx):
        """No lewding!"""
        await ctx.channel.trigger_typing()
        await ctx.send(file=discord.File("assets/imgs/reactions/nolewding.jpg"))

    @commands.command()
    async def repost(self, ctx):
        """It's just a repost smh"""
        await ctx.channel.trigger_typing()
        await ctx.send(file=discord.File("assets/imgs/reactions/repost.gif"))

    @commands.command()
    async def boi(self, ctx):
        """BOI"""
        await ctx.channel.trigger_typing()
        await ctx.send(file=discord.File("assets/imgs/reactions/boi.jpg"))

    @commands.command()
    async def facepalm(self, ctx):
        """when someone is retarded"""
        await ctx.channel.trigger_typing()
        await ctx.send(file=discord.File("assets/imgs/reactions/facepalm.gif"))

    @commands.command()
    async def facedesk(self, ctx):
        """when someone is REALLY retarded"""
        await ctx.channel.trigger_typing()
        await ctx.send(file=discord.File("assets/imgs/reactions/facedesk.gif"))

def setup(bot):
    bot.add_cog(Reactions(bot))
