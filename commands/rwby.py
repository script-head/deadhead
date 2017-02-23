from discord.ext import commands

class RWBY():
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def rwby(self):
        """Gives you the link to watch RWBY"""
        await self.bot.say("You can watch RWBY here fam: http://roosterteeth.com/show/rwby")

    @commands.command(pass_context=True)
    async def scream(self, ctx):
        """AAAAAAAAAAAAAAAAAAAA"""
        await self.bot.send_typing(ctx.message.channel)
        await self.bot.send_file(ctx.message.channel, "assets/imgs/scream.jpg")

    @commands.command(pass_context=True)
    async def heil(self, ctx):
        """sieg heil"""
        await self.bot.send_typing(ctx.message.channel)
        await self.bot.send_file(ctx.message.channel, "assets/imgs/blake_heil.png")

    @commands.command()
    async def characterinfo(self):
        """Gives you character information on Ruby Rose"""
        await self.bot.say("Here is some character information about me!\n```Name: Ruby Rose\nAge: 16\nRace: Human\nWeapon: Crescent Rose\nOutfit Colors: Red, Black\nAccessories: Rose Symbol, Ammunition Clips, Pouch, Cloak, Hood\nHandedness: Left\nComplexion: Pale White\nHeight: 5'2\" (1.57 meters)\nHair Color: Black and Red\nEye Color: Silver\nAura Color: Red\nSemblance: Speed\nPrevious Occupation: Student```")


def setup(bot):
    bot.add_cog(RWBY(bot))
