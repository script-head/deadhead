import asyncio
import cat
import random
import os
import json

from discord.ext import commands
from utils.tools import *
from utils.unicode import *
from utils.fun.lists import *
from utils import imagetools
from PIL import Image
#from cleverbot import Cleverbot

class Fun():
    def __init__(self, bot):
        self.bot = bot
        #self.cb = Cleverbot()

    @commands.command(pass_context=True)
    async def say(self, ctx, *, message:str):
        """Make the bot say whatever you want it to say"""
        try:
            await self.bot.delete_message(ctx.message)
        except:
            pass
        await self.bot.say(strip_global_mentions(message, ctx))

    @commands.command(pass_context=True)
    async def cat(self, ctx):
        """Sends a random cute catto gif because cats are soooo cuteeee <3 >.<"""
        await self.bot.send_typing(ctx.message.channel)
        cat.getCat(directory="data", filename="cat", format="gif")
        await asyncio.sleep(1) # This is so the bot has enough time to download the file
        await self.bot.send_file(ctx.message.channel, "data/cat.gif")
        # Watch Nero spam this command until the bot crashes

    @commands.command(pass_context=True)
    async def f(self, ctx):
        """Press F to pay your respects"""
        await self.bot.say("`{}` has paid their respects! Respects paid: {}".format(ctx.message.author, random.randint(1, 10000)))

    @commands.command()
    async def nicememe(self):
        """Nice Meme!"""
        await self.bot.say("http://niceme.me")

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
    async def quoteaf(self, ctx):
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

    @commands.command(enabled=False)
    async def talk(self, *, message):
        """Talk to the bot"""
        #await self.bot.say(self.cb.ask(message))

    @commands.command(pass_context=True)
    async def rate(self, ctx, user:discord.User=None):
        """Have the bot rate yourself or another user (rigged af)"""
        if user is None or user.id == ctx.message.author.id:
            await self.bot.say("I rate you a 10/10")
        elif user == self.bot.user:
            await self.bot.say("I rate myself a -1/10")
        else:
            await self.bot.say("I rate {} a {}/10".format(user.name, random.randint(0, 10)))

    @commands.command()
    async def honk(self):
        """Honk honk mother fucka"""
        await self.bot.say(random.choice(honkhonkfgt))

    @commands.command(pass_context=True)
    async def plzmsgme(self, ctx, *, message:str):
        """Makes the bot DM you with the specified message"""
        await self.bot.send_message(ctx.message.author, message)
        await self.bot.say(":ok_hand: check your DMs")

    @commands.command(pass_context=True)
    async def quote(self, ctx, id:str):
        """Quotes a message with the specified message ID"""
        message = await self.bot.get_message(ctx.message.channel, id)
        if message is None:
            await self.bot.say("I could not find a message with an ID of `{}` in this channel".format(id))
            return
        embed = make_message_embed(message.author, message.author.color, message.content, formatUser=True)
        embed.timestamp = message.timestamp
        await self.bot.say(embed=embed)

    @commands.command()
    async def twentyoneify(self, *, input:str):
        """EVERYTHING NEEDS TWENTY ØNE PILØTS!"""
        await self.bot.say(input.replace("O", "Ø").replace("o", "ø"))

    @commands.command()
    async def spellout(self, *, msg:str):
        """S P E L L O U T"""
        await self.bot.say(" ".join(list(msg.upper())))

    @commands.command(pass_context=True)
    async def trigger(self, ctx, *, member:discord.Member=None):
        """Triggers a user"""
        await self.bot.send_typing(ctx.message.channel)
        if member is None:
            member = ctx.message.author
        download_file(get_avatar(member, animate=False), "data/trigger.png")
        avatar = Image.open("data/trigger.png")
        triggered = imagetools.rescale(Image.open("assets/imgs/pillow/triggered.jpg"), avatar.size)
        position = 0, avatar.getbbox()[3] - triggered.getbbox()[3]
        avatar.paste(triggered, position)
        avatar.save("data/trigger.png")
        await self.bot.send_file(ctx.message.channel, "data/trigger.png")

    @commands.command(pass_context=True)
    async def memegen(self, ctx, name:str, line1:str, line2:str):
        """Run r!memelist of the list of memes. Example: r!memegen snek \"No booper\" \"do NOT!\""""
        def escape_literals(url):
            return url.replace("-", "--").replace("_", "__").replace("?", "~q").replace(" ", "%20").replace("''", "\"")
        url = "https://memegen.link/{}/{}/{}.jpg".format(name, escape_literals(line1), escape_literals(line2))
        file = url_to_bytes(url)
        await self.bot.send_file(ctx.message.channel, file["content"], filename=file["filename"])

    @commands.command(pass_context=True)
    async def memelist(self, ctx):
        """Gets a list of names for the memegen command"""
        await self.bot.send_typing(ctx.message.channel)
        await self.bot.send_file(ctx.message.channel, "assets/MemeList.txt")

    @commands.command(pass_context=True)
    async def blackandwhite(self, ctx, user:discord.Member=None):
        """Turns your avatar or the specified user's avatar black and white"""
        await self.bot.send_typing(ctx.message.channel)
        if user is None:
            user = ctx.message.author
        download_file(get_avatar(user, animate=False), "data/blackandwhite.png")
        avatar = Image.open("data/blackandwhite.png").convert("L")
        avatar.save("data/blackandwhite.png")
        await self.bot.send_file(ctx.message.channel, "data/blackandwhite.png")

    @commands.command(pass_context=True)
    async def headpat(self, ctx):
        """Posts a random headpat from headp.at"""
        pats = json.loads(requests.get("http://headp.at/js/pats.json").json())
        pat = random.choice(pats)
        file = url_to_bytes("http://headp.at/pats/{}".format(pat))
        await self.bot.send_file(ctx.message.channel, file["content"], filename=file["filename"])

    @commands.command(pass_context=True)
    async def thiscommanddoesfuckingnothing(self, ctx):
        """It doesn't do a fucking thing (or does it? OwO)"""
        await self.bot.wait_for_reaction(message=ctx.message, user=ctx.message.author)
        await self.bot.say("{} OKAY OKAY YOU FOUND OUT WHAT IT DOES GG SCREENSHOT THIS AND DM `Seth#0346` OR USE `r!notifydev` FOR A HEAD PAT".format(ctx.message.author.mention))

    @commands.command()
    async def reverse(self, *, msg:str):
        """ffuts esreveR"""
        await self.bot.say(msg[::-1])

    @commands.command(pass_context=True)
    async def react(self, ctx, id:str, emote:str):
        """Reacts to a message with the specifed message id and the specified emote"""
        try:
             message = await self.bot.get_message(ctx.message.channel, id=id)
        except discord.errors.NotFound:
            await self.bot.say("No message in this channel was found with an ID of `{}`".format(id))
            return
        emote_id = extract_emote_id(emote)
        if emote_id is not None:
            server_emote = discord.utils.get(list(self.bot.get_all_emojis()), id=emote_id)
            if server_emote is not None:
                emote = server_emote
            else:
                await self.bot.say("I am not on the server that contains that emote")
                return
        try:
            await self.bot.add_reaction(message, emote)
        except discord.errors.Forbidden:
            await self.bot.say("I do not have the `Add Reactions` permission")
        except discord.errors.HTTPException:
            await self.bot.say("The emote specified is invalid")

    @commands.command()
    async def intellect(self, *, msg:str):
        """Me, an intellectual"""
        await self.bot.send_typing()
        intellectify = ""
        for char in msg:
            intellectify += random.choice([char.upper(), char.lower()])
        await self.bot.say(intellectify)

def setup(bot):
    bot.add_cog(Fun(bot))
