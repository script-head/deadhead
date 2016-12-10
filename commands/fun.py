import asyncio
import cat
import random
import os

from discord.ext import commands
from utils.tools import *
from utils.unicode import *
from utils.fun.lists import *
from cleverbot import Cleverbot as cb

class Fun():
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def say(self, ctx, *, message:str):
        """Make the bot say whatever you want it to say"""
        try:
            await self.bot.delete_message(ctx.message)
        except:
            pass
        await self.bot.say(message)

    @commands.command(pass_context=True)
    async def cat(self, ctx):
        """Sends a random cute cat gifs because cats are soooo cuteeee <3 >.<"""
        await self.bot.send_typing(ctx.message.channel)
        cat.getCat(directory="data", filename="cat", format="gif")
        await asyncio.sleep(1) # This is so the bot has enough time to download the file
        await self.bot.send_file(ctx.message.channel, "data/cat.gif")
        # Watch Nero spam this command until the bot crashes

    @commands.command(pass_context=True)
    async def f(self, ctx):
        """Press F to pay your respects"""
        await self.bot.say("{} has paid their respects! Respects paid: {}".format(format_user(ctx.message.author), random.randint(1, 10000)))

    @commands.command()
    async def nicememe(self):
        """Nice Meme!"""
        await self.bot.say("http://niceme.me")

    @commands.command()
    async def tfw(self, *, tfw:str):
        """tfw this pointless command exists"""
        await self.bot.say("tfw {}: <https://www.youtube.com/watch?v=7wfYIMyS_dI>".format(tfw))

    @commands.command(pass_context=True)
    async def allahuakbar(self, ctx):
        """ALLAHU AKBAR!"""
        await self.bot.send_typing(ctx.message.channel)
        await self.bot.send_file(ctx.message.channel, "assets/imgs/allahuakbar.gif")

    @commands.command(pass_context=True)
    async def rekt(self, ctx):
        """#REKT"""
        await self.bot.send_typing(ctx.message.channel)
        await self.bot.send_file(ctx.message.channel, "assets/imgs/rekt.gif")

    @commands.command(pass_context=True)
    async def roasted(self, ctx):
        """MY NIGGA YOU JUST GOT ROASTED!"""
        await self.bot.send_typing(ctx.message.channel)
        await self.bot.send_file(ctx.message.channel, "assets/imgs/roasted.gif")

    @commands.command(pass_context=True)
    async def yiffinhell(self, ctx):
        """snek yiff"""
        await self.bot.send_typing(ctx.message.channel)
        await self.bot.send_file(ctx.message.channel, "assets/imgs/yiffinhell.png")

    @commands.command(pass_context=True)
    async def spam(self, ctx):
        """SPAM SPAM SPAM"""
        await self.bot.send_typing(ctx.message.channel)
        await self.bot.send_file(ctx.message.channel, "assets/imgs/spam.png")

    @commands.command(pass_context=True)
    async def internetrules(self, ctx):
        """The rules of the internet"""
        await self.bot.send_typing(ctx.message.channel)
        await self.bot.send_file(ctx.message.channel, "assets/InternetRules.txt")

    @commands.command(pass_context=True)
    async def quote(self, ctx):
        """Don't quote me on that"""
        await self.bot.send_typing(ctx.message.channel)
        await self.bot.send_file(ctx.message.channel, "assets/imgs/quotes/{}.png".format(random.randint(1, len([file for file in os.listdir("assets/imgs/quotes")]))))

    @commands.command(pass_context=True)
    async def b1nzy(self, ctx):
        """b1nzy pls no ;-;"""
        await self.bot.send_typing(ctx.message.channel)
        await self.bot.send_file(ctx.message.channel, "assets/imgs/b1nzy_with_banhammer.png")

    @commands.command(pass_context=True)
    async def cykablyat(self, ctx):
        """Cyka blyat!"""
        await self.bot.send_typing(ctx.message.channel)
        await self.bot.send_file(ctx.message.channel, "assets/imgs/cykablyat.jpg")

    @commands.command(pass_context=True)
    async def delet(self, ctx):
        """Delet this"""
        await self.bot.send_typing(ctx.message.channel)
        await self.bot.send_file(ctx.message.channel, "assets/imgs/delet_this.jpg")

    @commands.command()
    async def sombra(self):
        """Boop me Sombra <3"""
        await self.bot.say(sombra)

    @commands.command()
    async def lenny(self):
        """<Insert lenny face here>"""
        await self.bot.say(lenny)

    @commands.command()
    async def psat(self):
        """Please."""
        await self.bot.say(random.choice(psat_memes))

    @commands.command()
    async def alex(self):
        """ALEX IS A STUPID NIGERIAN!"""
        await self.bot.say("https://www.youtube.com/watch?v=GX5xQPhC6UY")

    @commands.command(pass_context=True)
    async def hoodaf(self, ctx):
        """Me in my hood"""
        await self.bot.send_typing(ctx.message.channel)
        await self.bot.send_file(ctx.message.channel, "assets/imgs/TheHood.gif")
        await self.bot.say("I look good in a hood, amirite?")

    @commands.command(pass_context=True, name="8ball")
    async def ball(self, ctx, *, question:str):
        """It's just python random don't take it seriously kthx"""
        await self.bot.say("{}: {}".format(ctx.message.author.name, random.choice(magic_conch_shell)))

    @commands.command()
    async def insult(self, *, user:str):
        """Insult those ass wipes"""
        await self.bot.say("{} {}".format(user, random.choice(insults)))

    @commands.command()
    async def actdrunk(self):
        """I got drunk on halloween in 2016 it was great"""
        await self.bot.say(random.choice(drunkaf))

    @commands.command()
    async def talk(self, *, message:str):
        """Talk to the bot"""
        await self.bot.say(cb().ask(message))

    @commands.command()
    async def rate(self, user:discord.User=None):
        """Have the bot rate yourself or another user"""
        if user is None:
            await self.bot.say("I rate you a {}/10".format(random.randint(0, 10)))
        else:
            await self.bot.say("I rate {} a {}/10".format(user.mention, random.randint(0, 10)))

    @commands.command()
    async def honk(self):
        """Honk honk mother fucker"""
        await self.bot.say(random.choice(honkhonkfgt))

    @commands.command(pass_context=True)
    async def triggered(self, ctx):
        """DID YOU JUST ASSUME MY GENDER? *TRIGGERED*"""
        await self.bot.send_typing(ctx.message.channel)
        await self.bot.send_file(ctx.message.channel, "assets/imgs/triggered.gif")

    @commands.command(pass_context=True)
    async def plzmsgme(self, ctx, *, message:str):
        """Makes the bot DM you with the specified message"""
        await self.bot.send_message(ctx.message.author, message)
        await self.bot.say(":ok_hand: check your DMs")

    @commands.command()
    async def fuckherrightinthepussy(self):
        """FUCK HER RIGHT IN THE PUSSY! #FHRITP"""
        await self.bot.say("https://www.youtube.com/watch?v=x7-nzLx4Oa0")

def setup(bot):
    bot.add_cog(Fun(bot))
