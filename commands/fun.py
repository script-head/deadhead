import asyncio
import cat
import os
import hashlib

from discord.ext import commands
from utils.tools import *
from utils.unicode import *
from utils.fun.lists import *
from utils.fun.fortunes import fortunes
from utils import imagetools
from PIL import Image
from utils.language import Language

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def say(self, ctx, *, message:str):
        """Make the bot say whatever you want it to say"""
        try:
            await ctx.message.delete()
        except:
            pass
        await ctx.send(strip_global_mentions(message, ctx))

    @commands.command()
    async def cat(self, ctx):
        """Sends a random cute catto gif because cats are soooo cuteeee <3 >.<"""
        # Watch Nero spam this command until the bot crashes
        await ctx.channel.trigger_typing()
        cat.getCat(directory="data", filename="cat", format="gif")
        await asyncio.sleep(1) # This is so the bot has enough time to download the file
        await ctx.send(file=discord.File("data/cat.gif", "cat.gif"))

    @commands.command()
    async def f(self, ctx):
        """Press F to pay your respects"""
        await ctx.send(Language.get("fun.respects", ctx).format(ctx.author, random.randint(1, 10000)))

    @commands.command()
    async def nicememe(self, ctx):
        """Nice Meme!"""
        await ctx.send("http://niceme.me")

    @commands.command()
    async def yiffinhell(self, ctx):
        """snek yiff"""
        await ctx.channel.trigger_typing()
        await ctx.send(file=discord.File("assets/imgs/yiffinhell.png"))

    @commands.command()
    async def spam(self, ctx):
        """SPAM SPAM SPAM"""
        await ctx.channel.trigger_typing()
        await ctx.send(file=discord.File("assets/imgs/spam.png"))

    @commands.command()
    async def internetrules(self, ctx):
        """The rules of the internet"""
        await ctx.channel.trigger_typing()
        await ctx.send(file=discord.File("assets/InternetRules.txt"))

    @commands.command()
    async def quoteaf(self, ctx):
        """Don't quote me on that"""
        await ctx.channel.trigger_typing()
        await ctx.send(file=discord.File("assets/imgs/quotes/{}.png".format(random.randint(1, len([file for file in os.listdir("assets/imgs/quotes")])))))

    @commands.command()
    async def b1nzy(self, ctx):
        """b1nzy pls no ;-;"""
        await ctx.channel.trigger_typing()
        await ctx.send(file=discord.File("assets/imgs/b1nzy_with_banhammer.png"))

    @commands.command()
    async def cykablyat(self, ctx):
        """Cyka blyat!"""
        await ctx.channel.trigger_typing()
        await ctx.send(file=discord.File("assets/imgs/cykablyat.jpg"))

    @commands.command()
    async def sombra(self, ctx):
        """Boop me Sombra <3"""
        await ctx.send(sombra)

    @commands.command()
    async def lenny(self, ctx):
        """<Insert lenny face here>"""
        await ctx.send(lenny)

    @commands.command()
    async def psat(self, ctx):
        """Please."""
        await ctx.send(random.choice(psat_memes))

    @commands.command(name="8ball")
    async def ball(self, ctx, *, question:str):
        """It's just python random don't take it seriously kthx"""
        await ctx.send("{}: {}".format(ctx.author.name, random.choice(magic_conch_shell)))

    @commands.command()
    async def insult(self, ctx, *, user:str):
        """Insult those ass wipes"""
        await ctx.send("{} {}".format(user, random.choice(insults)))

    @commands.command()
    async def actdrunk(self, ctx):
        """I got drunk on halloween in 2016 it was great"""
        await ctx.send(random.choice(drunkaf))

    @commands.command()
    async def rate(self, ctx, user:discord.User=None):
        """Have the bot rate yourself or another user (rigged af)"""
        if user is None or user.id == ctx.author.id:
            await ctx.send(Language.get("fun.rate_author", ctx))
        elif user == self.bot.user:
            await ctx.send(Language.get("fun.rate_self", ctx))
        else:
            await ctx.send(Language.get("fun.rate_user", ctx).format(user.name, random.randint(0, 10)))

    @commands.command()
    async def honk(self, ctx):
        """Honk honk mother fucka"""
        await ctx.send(random.choice(honkhonkfgt))

    @commands.command()
    async def plzmsgme(self, ctx, *, message:str):
        """Makes the bot DM you with the specified message"""
        await ctx.author.send(message)
        await ctx.send(Language.get("fun.plzmsgme", ctx))

    @commands.command()
    async def quote(self, ctx, id:int):
        """Quotes a message with the specified message ID"""
        try:
            message = await ctx.channel.fetch_message(id)
        except discord.errors.NotFound:
            await ctx.send(Language.get("bot.no_message_found", ctx).format(id))
            return
        embed = make_message_embed(message.author, message.author.color, message.content, formatUser=True)
        timestamp = message.created_at
        if message.edited_at:
            timestamp = message.edited_at
        embed.timestamp = timestamp
        await ctx.send(embed=embed)

    @commands.command()
    async def twentyoneify(self, ctx, *, input:str):
        """EVERYTHING NEEDS TWENTY ØNE PILØTS!"""
        await ctx.send(input.replace("O", "Ø").replace("o", "ø"))

    @commands.command()
    async def spellout(self, ctx, *, msg:str):
        """S P E L L O U T"""
        await ctx.send(" ".join(list(msg.upper())))

    @commands.command()
    async def trigger(self, ctx, *, member:discord.Member=None):
        """Triggers a user"""
        await ctx.channel.trigger_typing()
        if member is None:
            member = ctx.author
        download_file(get_avatar(member, animate=False), "data/trigger.png")
        avatar = Image.open("data/trigger.png")
        triggered = imagetools.rescale(Image.open("assets/imgs/pillow/triggered.jpg"), avatar.size)
        position = 0, avatar.getbbox()[3] - triggered.getbbox()[3]
        avatar.paste(triggered, position)
        avatar.save("data/trigger.png")
        await ctx.send(file=discord.File("data/trigger.png"))

    @commands.command()
    async def memegen(self, ctx, name:str, line1:str, line2:str):
        """Run r!memelist of the list of memes. Example: r!memegen snek \"No booper\" \"do NOT!\""""
        def escape_literals(url):
            return url.replace("-", "--").replace("_", "__").replace("?", "~q").replace(" ", "%20").replace("''", "\"")
        url = "https://memegen.link/{}/{}/{}.jpg".format(name, escape_literals(line1), escape_literals(line2))
        file = url_to_bytes(url)
        await ctx.send(file=discord.File(file["content"], file["filename"]))

    @commands.command()
    async def memelist(self, ctx):
        """Gets a list of names for the memegen command"""
        await ctx.channel.trigger_typing()
        await ctx.send(file=discord.File("assets/MemeList.txt"))

    @commands.command()
    async def blackandwhite(self, ctx, user:discord.Member=None):
        """Turns your avatar or the specified user's avatar black and white"""
        await ctx.channel.trigger_typing()
        if user is None:
            user = ctx.author
        download_file(get_avatar(user, animate=False), "data/blackandwhite.png")
        avatar = Image.open("data/blackandwhite.png").convert("L")
        avatar.save("data/blackandwhite.png")
        await ctx.send(file=discord.File("data/blackandwhite.png"))

    @commands.command()
    async def headpat(self, ctx):
        """Posts a random headpat from headp.at"""
        pats = requests.get("http://headp.at/js/pats.json").json()
        pat = random.choice(pats)
        file = url_to_bytes("http://headp.at/pats/{}".format(pat))
        await ctx.send(file=discord.File(file["content"], file["filename"]))

    @commands.command()
    async def thiscommanddoesfuckingnothing(self, ctx):
        """It doesn't do a fucking thing (or does it? OwO)"""
        await ctx.wait_for("reaction_add", check=lambda reaction, user: user.id == ctx.message.author.id and reaction.message == ctx.message)
        await ctx.send(Language.get("fun.nothing", ctx).format(ctx.author.mention))

    @commands.command()
    async def reverse(self, ctx, *, msg:str):
        """ffuts esreveR"""
        await ctx.send(msg[::-1])

    @commands.command()
    async def react(self, ctx, id:int, emote:str):
        """Reacts to a message with the specifed message id and the specified emote"""
        try:
             message = await ctx.channel.fetch_message(id)
        except discord.errors.NotFound:
            await ctx.send(Language.get("bot.no_message_found", ctx).format(id))
            return
        emote_id = extract_emote_id(emote)
        if emote_id is not None:
            server_emote = discord.utils.get(list(self.bot.get_all_emojis), id=emote_id)
            if server_emote is not None:
                emote = server_emote
            else:
                await ctx.send(Language.get("fun.no_emote_found", ctx))
                return
        try:
            await ctx.add_reaction(message, emote)
        except discord.errors.Forbidden:
            await ctx.send(Language.get("fun.no_reaction_perms", ctx))
        except discord.errors.HTTPException:
            await ctx.send(Language.get("fun.invalid_emote", ctx))

    @commands.command()
    async def intellect(self, ctx, *, msg:str):
        """Me, an intellectual"""
        await ctx.channel.trigger_typing()
        intellectify = ""
        for char in msg:
            intellectify += random.choice([char.upper(), char.lower()])
        await ctx.send(intellectify)

    @commands.command()
    async def encodemorse(self, ctx, *, msg:str):
        """Encode something into morse code"""
        encoded_message = ""
        for char in list(msg.upper()):
            encoded_message += encode_morse[char] + " "
        await ctx.send(encoded_message)

    @commands.command()
    async def decodemorse(self, ctx, *, msg:str):
        """Decode something from morse code"""
        decoded_message = ""
        for char in msg.split():
            if char == " ":
                continue
            decoded_message += decode_morse[char]
        await ctx.send(decoded_message)

    @commands.command()
    async def randomnumber(self, ctx, *, digits:int=1):
        """Generates a random number with the specified length of digits"""
        number = ""
        for i in range(digits):
            number += str(random.randint(0, 9))
        await ctx.send(number)

    @commands.command()
    async def rolldice(self, ctx):
        """Roll some die"""
        await ctx.send("You rolled a {}!".format(random.randint(1, 6)))

    @commands.command()
    async def md5(self, ctx, *, msg:str):
        """Convert something to MD5"""
        await ctx.send("`{}`".format(hashlib.md5(bytes(msg.encode("utf-8"))).hexdigest()))\

    @commands.command()
    async def sha256(self, ctx, *, msg:str):
        """Convert something to sha256"""
        await ctx.send("`{}`".format(hashlib.sha256(bytes(msg.encode("utf-8"))).hexdigest()))

    @commands.command()
    async def sha512(self, ctx, *, msg:str):
        """Convert something to sha512"""
        await ctx.send("`{}`".format(hashlib.sha512(bytes(msg.encode("utf-8"))).hexdigest()))

    @commands.command()
    async def uppercase(self, ctx, *, msg:str):
        """UPPERCASE DIS"""
        await ctx.send(msg.upper())

    @commands.command()
    async def lowercase(self, ctx, *, msg:str):
        """lowercase dis"""
        await ctx.send(msg.lower())

    @commands.command()
    async def fight(self, ctx, user:str=None, *, weapon:str=None):
        """Fight someone with something"""
        if user is None or user.lower() == ctx.author.mention or user == ctx.author.name.lower() or ctx.guild is not None and ctx.author.nick is not None and user == ctx.author.nick.lower():
            await ctx.send("{} fought themself but only ended up in a mental hospital!".format(ctx.author.mention))
            return
        if weapon is None:
            await ctx.send("{0} tried to fight {1} with nothing so {1} beat the breaks off of them!".format(ctx.author.mention, user))
            return
        await ctx.send("{} used **{}** on **{}** {}".format(ctx.author.mention, weapon, user, random.choice(fight_results).replace("%user%", user).replace("%attacker%", ctx.author.mention)))

    @commands.command()
    async def nou(self, ctx):
        """no u"""
        await ctx.send("no u")

    @commands.command()
    async def cowsay(self, ctx, type:str, *, message:str):
        """moo"""
        try:
            cow = cowList[type.lower()]
        except KeyError:
            await ctx.send("`{}` is not a usable character type. Run **{}cows** for a list of cows.".format(type, ctx.prefix))
            return
        msg = "```{}```".format(cow.milk(message))
        if len(msg) > 2000:
            await ctx.send("Sorry, the message length with the cow in it has a total character length of {}. Discord only allows 2000 characters per message.".format(len(msg)))
            return
        await ctx.send(msg)

    @commands.command()
    async def fortune(self, ctx):
        """Get your fortune read, not as authentic as a fortune cookie."""
        await ctx.send("```{}```".format(random.choice(fortunes)))

    @commands.command()
    async def cows(self, ctx):
        """Cow list for the cowsay command"""
        await ctx.send("Current list of cows:```{}```".format(", ".join(cowList.keys())))

    @commands.command()
    async def neko(self, ctx, type:str):
        """Gets an image from nekos.life"""
        if type == "sfwlist":
            await ctx.send("```{}```".format(", ".join(sfw_neko_types)))
            return
        elif type == "nsfwlist":
            if not ctx.channel.is_nsfw():
                await ctx.send("I can only list nsfw types in a nsfw channel.")
            else:
                await ctx.send("```{}```".format(", ".join(nsfw_neko_types)))
            return
        elif type in nsfw_neko_types:
            if not ctx.channel.is_nsfw():
                await ctx.send("This type can only be displayed in nsfw channels.")
                return
        elif type not in sfw_neko_types:
            await ctx.send("Please run `{0}neko sfwlist` for sfw image types, and `{0}neko nsfwlist` for nsfw image types.".format(ctx.prefix))
            return
        await ctx.send(embed=get_neko_image(type, ctx.author))

    @commands.command()
    async def owo(self, ctx, *, text:str):
        """OwO, owoify something >w<"""
        await ctx.send(owoify(text))

def setup(bot):
    bot.add_cog(Fun(bot))
