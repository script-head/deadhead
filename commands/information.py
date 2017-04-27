import time
import nmap
import socket
import pythonwhois

from discord.ext import commands
from datetime import date
from utils.tools import *
from utils.logger import log
from utils.config import Config
from utils.unicode import *
from PIL import Image
config = Config()

halloween = date(2017, 10, 31)
christmas = date(2017, 12, 25)

class Information():
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def id(self, ctx, user:discord.User=None):
        """Gets your ID or if you @mention a user it gets their id"""
        if user is None:
            await self.bot.say("Your ID is `{}`".format(ctx.message.author.id))
        else:
            await self.bot.say("{}'s ID is `{}`".format(user.mention, user.id))

    @commands.command(pass_context=True)
    async def serverinfo(self, ctx):
        """Gets information on the current server"""
        server = ctx.message.server
        if not server.afk_channel:
            afk_channel = None
        else:
            afk_channel = server.afk_channel.name
        fields = {"ID":server.id, "Created on":format_time(server.created_at), "Region":server.region, "Member Count":len(server.members), "Channel Count":len(server.channels), "Role Count":len(server.roles), "Owner":server.owner, "Owner ID":server.owner_id, "AFK Channel":afk_channel, "AFK Timeout":"{} seconds".format(server.afk_timeout), "Verification Level":str(ctx.message.server.verification_level).capitalize().replace("High", tableflip), "2FA Enabled":convert_to_bool(server.mfa_level)}
        embed = make_list_embed(fields)
        embed.title = server.name
        embed.color = 0xFF0000
        if server.icon_url is not None:
            embed.set_thumbnail(url=server.icon_url)
        await self.bot.say(embed=embed)

    @commands.command(pass_context=True)
    async def userinfo(self, ctx, *, user:discord.Member=None):
        """Gets your information or the information of the specified user"""
        if user is None:
            user = ctx.message.author
        game = None
        if user.game:
            game = user.game.name
        fields = {"ID":user.id, "Bot Account":user.bot, "Created on":format_time(user.created_at), "Game":game, "Status":user.status, "Role Count":len(user.roles), "Joined on":format_time(user.joined_at), "Nickname":user.nick, "Voice Channel":user.voice.voice_channel, "Self Muted":user.voice.self_mute, "Self Deafened":user.voice.self_deaf, "Server Muted":user.voice.mute, "Server Deafened":user.voice.deaf}
        embed = make_list_embed(fields)
        embed.title = str(user)
        embed.color = user.color
        embed.set_thumbnail(url=get_avatar(user))
        await self.bot.say(embed=embed)

    @commands.command(pass_context=True)
    async def avatar(self, ctx, *, user:discord.User=None):
        """Gets your avatar url or the avatar url of the specified user"""
        if user is None:
            user = ctx.message.author
        await self.bot.say("{}'s avatar url is: {}".format(user.mention, get_avatar(user)))

    @commands.command(pass_context=True)
    async def defaultavatar(self, ctx, *, user:discord.User=None):
        """Gets your default avatar url or the default avatar url of the specified user"""
        if user is None:
            user = ctx.message.author
        await self.bot.say("{}'s default avatar url is: {}".format(user.mention, user.default_avatar_url))

    @commands.command(pass_context=True)
    async def roleinfo(self, ctx, *, name:str):
        """Gets information on a role"""
        role = discord.utils.get(ctx.message.server.roles, name=name)
        if role is None:
            await self.bot.say("`{}` is not a valid role".format(name))
            return
        color = role.color
        if color == discord.Color(value=0x000000):
            color = None
        count = len([member for member in ctx.message.server.members if discord.utils.get(member.roles, name=role.name)])
        perms = role.permissions
        permlist = "Can ban members: {}\nCan change nickname: {}\nCan connect to voice channels: {}\nCan create instant invites: {}\nCan deafen members: {}\nCan embed links: {}\nCan use external emojis: {}\nCan manage channel: {}\nCan manage emojis: {}\nCan manage messages: {}\nCan manage nicknames: {}\nCan manage roles: {}\nCan manage server: {}\nCan mention everyone: {}\nCan move members: {}\nCan mute members: {}\nCan read message history: {}\nCan send messages: {}\nCan speak: {}\nCan use voice activity: {}\nCan manage webbooks: {}\nCan add reactions: {}".format(perms.ban_members, perms.change_nickname, perms.connect, perms.create_instant_invite, perms.deafen_members, perms.embed_links, perms.external_emojis, perms.manage_channels, perms.manage_emojis, perms.manage_messages, perms.manage_nicknames, perms.manage_roles, perms.manage_server, perms.mention_everyone, perms.move_members, perms.mute_members, perms.read_message_history, perms.send_messages, perms.speak,                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               perms.use_voice_activation, perms.manage_webhooks, perms.add_reactions)
        await self.bot.say(py.format("Name: \"{}\"\nID: {}\nColor: {}\nPosition: {}\nUser count: {}\nMentionable: {}\nDisplay separately: {}".format(role.name, role.id, color, role.position, count, role.mentionable, role.hoist) + permlist))

    @commands.command()
    async def emoteurl(self, *, emote:str):
        """Gets the url for a CUSTOM emote (meaning no unicode emotes)"""
        emote_id = None
        try:
            if extract_emote_id(emote) is not None:
                emote_id = extract_emote_id(emote)
        except:
            pass
        if emote_id is None:
            await self.bot.say("That is not a custom emote")
            return
        await self.bot.say("https://discordapp.com/api/emojis/{}.png".format(emote_id))

    @commands.command()
    async def discrim(self, *, discriminator:str):
        """Gets a username#discriminator list of all users that the bot can see with the specified discriminator"""
        members = []
        for member in list(self.bot.get_all_members()):
            if member.discriminator == discriminator and str(member) not in members:
                members.append(str(member))
        if len(members) == 0:
            members = "I could not find any users in any of the servers I'm in with a discriminator of `{}`".format(discriminator)
        else:
            members = "```{}```".format(", ".join(members))
        await self.bot.say(members)

    @commands.command()
    async def daystillhalloween(self):
        """Displays how many days until it's halloween"""
        await self.bot.say("Days until halloween: `{} days`".format((halloween - date.today()).days))

    @commands.command()
    async def daystillchristmas(self):
        """Displays how many days until it's christmas"""
        await self.bot.say("Days until christmas: `{} days`".format((christmas - date.today()).days))

    @commands.command()
    async def getserverinfo(self, *, name:str):
        """Gets very basic server info on the server with the specified name"""
        server = discord.utils.get(self.bot.servers, name=name)
        if server is None:
            await self.bot.say("I could not find a server by the name of `{}`".format(name))
        else:
            await self.bot.say("```Name: {}\nID: {}\nOwner: {}\nOwner ID: {}\nMember count: {}\nDate created: {}```".format(server.name, server.id, server.owner, server.owner.id, len(server.members), server.created_at))

    @commands.command(pass_context=True)
    async def isitdown(self, ctx, *, url:str):
        """Checks to see if a website is online or not"""
        await self.bot.send_typing(ctx.message.channel)
        url = url.strip("<>")
        if not url.startswith("http://") and not url.startswith("https://"):
            url = "http://{}".format(url)
        try:
            starttime = time.time()
            requests.get(url, timeout=3)
            ping = "%.01f seconds" % (time.time() - starttime)
            await self.bot.say("`{}` is online. Ping time is `{}`".format(url, ping))
        except:
            await self.bot.say("`{}` is offline.".format(url))

    @commands.command(pass_context=True)
    async def getemotes(self, ctx):
        """Gets a list of the server's emotes"""
        emotes = ctx.message.server.emojis
        if len(emotes) == 0:
            await self.bot.say("This server doesn't have any emotes!")
            return
        emotes = ["`:{}:` = {}".format(emote.name, emote) for emote in emotes]
        await self.bot.say("\n".join(emotes))

    @commands.command(pass_context=True)
    async def osu(self, ctx, *, username:str):
        """Gets an osu! profile stats with the specified name"""
        if not config.enableOsu:
            await self.bot.say("The osu! command has been disabled.")
            return
        try:
            import osuapi
        except ImportError:
            log.critical("The osu api is enabled, but the osuapi module was not found! Please run \"pip install osuapi\"")
            await self.bot.say("Couldn't import the osu! api module, contact the bot developer!")
            return
        await self.bot.send_typing(ctx.message.channel)
        api = osuapi.OsuApi(config._osuKey, connector=osuapi.AHConnector())
        try:
            user = await api.get_user(username)
        except osuapi.HTTPError as e:
            if e.code == 401:
                log.critical("An invalid osu! api key was set, please check the config for instructions on how to get a proper api key!")
                await self.bot.say("An invalid osu! api key was set, contact the bot developer!")
                return
            else:
                log.critical("An unknown error occured while trying to get an osu! profile.")
                await self.bot.say("An unknown error occured while trying to get that user's osu! profile, contact the bot developer!")
                return
        try:
            user = user[0]
        except IndexError:
            await self.bot.say("Could find any osu! profile named `{}`".format(username))
            return
        fields = {"ID":user.user_id, "Country":user.country, "Level":int(user.level), "Hits":user.total_hits, "Score":user.total_score, "Accuracy":"{0:.2f}%".format(user.accuracy), "Play Count":user.playcount, "Ranked Score":user.ranked_score, "A rank":user.count_rank_a, "S rank":user.count_rank_s, "SS rank":user.count_rank_ss}
        embed = make_list_embed(fields)
        embed.title = "{}'s Osu! Stats".format(user.username)
        embed.color = 0xFF00FF
        embed.set_thumbnail(url="http://s.ppy.sh/a/{}".format(user.user_id))
        await self.bot.say(embed=embed)

    @commands.command()
    async def emoteinfo(self, *, emote:discord.Emoji):
        """Gets information on a custom emote (Only works for servers the bot is on)"""
        fields = {"Name":emote.name, "ID":emote.id, "Server Origin":emote.server.name, "Created On":format_time(emote.created_at), "Colons Required":emote.require_colons, "Managed by Twitch":emote.managed}
        embed = make_list_embed(fields)
        embed.title = ":{}:".format(emote.name)
        embed.color = 0xFF0000
        embed.set_thumbnail(url=emote.url)
        await self.bot.say(embed=embed)

    @commands.command(pass_context=True)
    async def portscan(self, ctx, host:str, ports:str):
        """Uses nmap to scan the specified ports from the specified host"""
        await self.bot.send_typing(ctx.message.channel)
        scanner = nmap.PortScanner()
        try:
            host = socket.gethostbyname(host)
        except socket.gaierror:
            await self.bot.say("`{}` is not a valid address".format(host))
            return
        ports = scanner.scan(host, ports)["scan"][host]["tcp"]
        results = []
        for port, data in ports.items():
            service = data["name"]
            if service == "":
                service = "unknown"
            results.append("Port {}({}): {}".format(port, service, data["state"]))
        await self.bot.say(xl.format("\n".join(results)))

    @commands.command()
    async def getnumericip(self, address:str):
        """Resolves the numeric ip of a domain"""
        try:
            await self.bot.say(socket.gethostbyname(address))
        except socket.gaierror:
            await self.bot.say("`{}` is not a valid address".format(address))

    @commands.command()
    async def whois(self, domain:str):
        """Gets whois information on a domain"""
        try:
            info = pythonwhois.get_whois(domain)
        except pythonwhois.shared.WhoisException:
            await self.bot.say("Could not find the root server for that TLD")
            return
        except KeyError:
            await self.bot.say("Failed to lookup domain")
            return
        if info["contacts"]["registrant"] is None:
            await self.bot.say(embed=discord.Embed(title="Domain Available", description="`{}` is available for registration".format(domain), color=0x00FF00))
            return
        fields = {"Registrar":info["registrar"][0], "Registered on":format_time(info["creation_date"][0]), "Expires on":format_time(info["expiration_date"][0]), "Last updated":format_time(info["updated_date"][0]), "Name Servers":", ".join(info["nameservers"])}
        embed = make_list_embed(fields)
        embed.title = "Domain Unavailable"
        embed.color = 0xFF0000
        await self.bot.say(embed=embed)

    @commands.command(pass_context=True)
    async def color(self, ctx, *, hex:str):
        """Displays the given hex color"""
        await self.bot.send_typing(ctx.message.channel)
        if not hex.startswith("#"):
            hex = "#{}".format(hex)
        try:
            Image.new("RGBA", (50, 50), hex).save("data/color.png")
        except ValueError:
            await self.bot.say("`{}` is not a valid hex color".format(hex))
            return
        await self.bot.send_file(ctx.message.channel, "data/color.png")

    @commands.command()
    async def getuserbyid(self, id:str):
        """Gets a user by id"""
        user = discord.utils.get(list(self.bot.get_all_members()), id=id)
        if not user:
            await self.bot.say("Could not find any user in my mutual servers with an ID of `{}`".format(id))
            return
        if user.game:
            game = user.game.name
        fields = {"Name":user.name, "Discriminator":user.discriminator, "ID":user.id, "Status":str(user.status).replace("dnd", "do not disturb"), "Game":game, "Bot":user.bot}
        embed = make_list_embed(fields)
        embed.title = str(user)
        embed.color = 0xFF0000
        embed.set_thumbnail(url=get_avatar(user))
        await self.bot.say(embed=embed)

    @commands.command()
    async def roleid(self, role:discord.Role):
        """Gets the id for the specified role"""
        await self.bot.say("The role ID for `{}` is `{}`".format(role.name, role.id))

def setup(bot):
    bot.add_cog(Information(bot))
