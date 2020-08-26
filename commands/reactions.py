import discord

from discord.ext import commands

class Reactions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

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
        """*TRIGGERED*"""
        await ctx.channel.trigger_typing()
        await ctx.send(file=discord.File("assets/imgs/reactions/triggered.gif"))

    @commands.command()
    async def delet(self, ctx):
        """Delet this"""
        await ctx.channel.trigger_typing()
        await ctx.send(file=discord.File("assets/imgs/reactions/delet_this.png"))

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
    async def repost(self, ctx):
        """It's just a repost smh"""
        await ctx.channel.trigger_typing()
        await ctx.send(file=discord.File("assets/imgs/reactions/repost.gif"))

    @commands.command()
    async def boi(self, ctx):
        """BOI"""
        await ctx.channel.trigger_typing()
        await ctx.send(file=discord.File("assets/imgs/reactions/boi.jpg"))

def setup(bot):
    bot.add_cog(Reactions(bot))
