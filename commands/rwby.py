import discord

from discord.ext import commands

class RWBY():
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def rwby(self, ctx):
        """Gives you the link to watch RWBY"""
        await ctx.send("You can watch RWBY here fam: https://roosterteeth.com/show/rwby")

    @commands.command()
    async def scream(self, ctx):
        """AAAAAAAAAAAAAAAAAAAA"""
        await ctx.channel.trigger_typing()
        await ctx.send(file=discord.File("assets/imgs/scream.png"))

    @commands.command()
    async def heil(self, ctx):
        """sieg heil"""
        await ctx.channel.trigger_typing()
        await ctx.send(file=discord.File("assets/imgs/blake_heil.png"))

    @commands.command()
    async def characterinfo(self, ctx):
        """Gives you character information on Ruby Rose"""
        await ctx.send("Here is some character information about me!\n```Name: Ruby Rose\nAge: 16\nRace: Human\nWeapon: Crescent Rose\nOutfit Colors: Red, Black\nAccessories: Rose Symbol, Ammunition Clips, Pouch, Cloak, Hood\nHandedness: Left\nComplexion: Pale White\nHeight: 5'2\" (1.57 meters)\nHair Color: Black and Red\nEye Color: Silver\nAura Color: Red\nSemblance: Speed\nPrevious Occupation: Student```")


def setup(bot):
    bot.add_cog(RWBY(bot))
