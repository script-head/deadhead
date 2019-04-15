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
from utils.language import Language
from utils import checks
from twitch import TwitchClient
from googleapiclient.discovery import build
from datetime import datetime

config = Config()

halloween = date(2018, 10, 31)
christmas = date(2018, 12, 25)

twitch = TwitchClient(client_id=config._twitchClientID)
youtubeAPI = youtubeAPI = build("youtube", "v3", developerKey=config._googleAPIKey)

class Information(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def id(self, ctx, user:discord.User=None):
        """Gets your ID or if you @mention a user it gets their id"""
        if user is None:
            await ctx.send(Language.get("information.author_id", ctx).format(ctx.author.id))
        else:
            await ctx.send(Language.get("information.user_id", ctx).format(user.mention, user.id))

    @commands.guild_only()
    @commands.command()
    async def serverinfo(self, ctx):
        """Gets information on the current server"""
        guild = ctx.guild
        human_count = len([member for member in guild.members if not member.bot])
        bot_count = len(([member for member in guild.members if member.bot]))
        timeout_times = {60:Language.get("information.timeout_times.60", ctx), 300:Language.get("information.timeout_times.300", ctx), 900:Language.get("information.timeout_times.900", ctx), 1800:Language.get("information.timeout_times.1800", ctx), 3600:Language.get("information.timeout_times.3600", ctx)}
        fields = {Language.get("information.id", ctx):guild.id, Language.get("information.created_on", ctx):format_time(guild.created_at), Language.get("information.region", ctx):guild.region, Language.get("information.member_count_title", ctx).format(len(guild.members)):Language.get("information.member_count", ctx).format(human_count, bot_count), Language.get("information.channel_count_title", ctx).format(len(guild.channels)):Language.get("information.channel_count", ctx).format(len(guild.text_channels), len(guild.voice_channels)), Language.get("information.role_count", ctx):len(guild.roles), Language.get("information.owner", ctx):guild.owner, Language.get("information.owner_id", ctx):guild.owner_id, Language.get("information.afk_channel", ctx):guild.afk_channel, Language.get("information.afk_timeout", ctx):timeout_times[guild.afk_timeout], Language.get("information.verification_level", ctx):str(ctx.guild.verification_level).capitalize().replace("High", tableflip).replace("Extreme", doubleflip), Language.get("information.2fa_enabled", ctx):convert_to_bool(guild.mfa_level)}
        embed = make_list_embed(fields)
        embed.title = guild.name
        embed.color = 0xFF0000
        if guild.icon_url:
            embed.set_thumbnail(url=guild.icon_url)
        await ctx.send(embed=embed)

    @commands.guild_only()
    @commands.command()
    async def userinfo(self, ctx, *, user:discord.Member=None):
        """Gets your information or the information of the specified user"""
        if user is None:
            user = ctx.author
        game = None
        if user.activity:
            game = user.activity.name
        voice_channel = None
        self_mute = False
        self_deaf = False
        server_mute = False
        server_deaf = False
        if user.voice:
            voice_channel = user.voice.channel
            self_mute = user.voice.self_mute
            self_deaf = user.voice.self_deaf
            server_mute = user.voice.mute
            server_deaf = user.voice.deaf
        fields = {Language.get("information.id", ctx):user.id, Language.get("information.bot_account", ctx):user.bot, Language.get("information.created_on", ctx):format_time(user.created_at), Language.get("information.game", ctx):game, Language.get("information.status", ctx):user.status, Language.get("information.role_count", ctx):len(user.roles), Language.get("information.joined_on", ctx):format_time(user.joined_at), Language.get("information.nickname", ctx):user.nick, Language.get("information.voice_channel", ctx):voice_channel, Language.get("information.self_muted", ctx):self_mute, Language.get("information.self_deafened", ctx):self_deaf, Language.get("information.server_muted", ctx):server_mute, Language.get("information.server_deafened", ctx):server_deaf}
        embed = make_list_embed(fields)
        embed.title = str(user)
        embed.color = user.color
        embed.set_thumbnail(url=get_avatar(user))
        await ctx.send(embed=embed)

    @commands.guild_only()
    @commands.command()
    async def fuckyou(self, ctx, *, user: discord.Member = None):
        """Gets your information or the information of the specified user"""
        user = ctx.author
        fields = {"fuck":"you"}
        embed = make_list_embed(fields)
        embed.title = str(user)
        embed.color = user.color
        #embed.set_thumbnail(url=get_avatar(user))
        await ctx.send(embed=embed)

    @commands.command()
    async def avatar(self, ctx, *, user:discord.User=None):
        """Gets your avatar url or the avatar url of the specified user"""
        if user is None:
            user = ctx.author
        await ctx.send(Language.get("information.avatar", ctx).format(user.name, get_avatar(user)))

    @commands.command()
    async def defaultavatar(self, ctx, *, user:discord.User=None):
        """Gets your default avatar url or the default avatar url of the specified user"""
        if user is None:
            user = ctx.author
        await ctx.send(Language.get("information.default_avatar", ctx).format(user.mention, user.default_avatar_url))

    # Not gonna bother maintaining the roleinfo command anymore because
    # of permission changes and because its a giant block
    @commands.guild_only()
    @checks.is_dev()
    @commands.command(hidden=True)
    async def roleinfo(self, ctx, *, name:str):
        """Gets information on a role"""
        role = discord.utils.get(ctx.guild.roles, name=name)
        if role is None:
            await ctx.send("`{}` is not a valid role".format(name))
            return
        color = role.color
        if color == discord.Color(value=0x000000):
            color = None
        count = len([member for member in ctx.guild.members if discord.utils.get(member.roles, name=role.name)])
        perms = role.permissions
        permlist = "Can ban members: {}\nCan change nickname: {}\nCan connect to voice channels: {}\nCan create instant invites: {}\nCan deafen members: {}\nCan embed links: {}\nCan use external emojis: {}\nCan manage channel: {}\nCan manage emojis: {}\nCan manage messages: {}\nCan manage nicknames: {}\nCan manage roles: {}\nCan manage server: {}\nCan mention everyone: {}\nCan move members: {}\nCan mute members: {}\nCan read message history: {}\nCan send messages: {}\nCan speak: {}\nCan use voice activity: {}\nCan manage webbooks: {}\nCan add reactions: {}\nCan view audit logs: {}".format(perms.ban_members, perms.change_nickname, perms.connect, perms.create_instant_invite, perms.deafen_members, perms.embed_links, perms.external_emojis, perms.manage_channels, perms.manage_emojis, perms.manage_messages, perms.manage_nicknames, perms.manage_roles, perms.manage_guild, perms.mention_everyone, perms.move_members, perms.mute_members, perms.read_message_history, perms.send_messages, perms.speak, perms.use_voice_activation, perms.manage_webhooks, perms.add_reactions, perms.view_audit_log)
        await ctx.send(py.format("Name: \"{}\"\nID: {}\nColor: {}\nPosition: {}\nUser count: {}\nMentionable: {}\nDisplay separately: {}\n".format(role.name, role.id, color, role.position, count, role.mentionable, role.hoist) + permlist))

    @commands.command()
    async def emoteurl(self, ctx, *, emote:str):
        """Gets the url for a CUSTOM emote (meaning no unicode emotes)"""
        emote_id = extract_emote_id(emote)
        if emote_id is None:
            await ctx.send(Language.get("information.non-custom_emote", ctx))
            return
        extension = "png"
        if emote.startswith("<a"):
            extension = "gif"
        await ctx.send("https://discordapp.com/api/emojis/{}.{}".format(emote_id, extension))

    @commands.command()
    async def discrim(self, ctx, *, discriminator:str):
        """Gets a username#discriminator list of all users that the bot can see with the specified discriminator"""
        members = []
        for member in list(self.bot.get_all_members()):
            if member.discriminator == discriminator and str(member) not in members:
                members.append(str(member))
        if len(members) == 0:
            members = Language.get("information.no_discrims_found", ctx).format(discriminator)
        else:
            members = "```{}```".format(", ".join(members))
        await ctx.send(members)

    @commands.command()
    async def daystillhalloween(self, ctx):
        """Displays how many days until it's halloween"""
        await ctx.send(Language.get("information.days_till_halloween", ctx).format((halloween - date.today()).days))

    @commands.command()
    async def daystillchristmas(self, ctx):
        """Displays how many days until it's christmas"""
        await ctx.send(Language.get("information.days_till_christmas", ctx).format((christmas - date.today()).days))

    @commands.command(hidden=True)
    @checks.is_dev()
    async def getserverinfo(self, ctx, *, name:str):
        """Gets very basic server info on the server with the specified name"""
        guild = discord.utils.get(self.bot.guilds, name=name)
        if guild is None:
            await ctx.send("I could not find a server by the name of `{}`".format(name))
        else:
            await ctx.send("```Name: {}\nID: {}\nOwner: {}\nOwner ID: {}\nMember count: {}\nDate created: {}```".format(guild.name, guild.id, guild.owner, guild.owner.id, len(guild.members), format_time(guild.created_at)))

    @commands.command()
    async def isitdown(self, ctx, *, url:str):
        """Checks to see if a website is online or not"""
        await ctx.channel.trigger_typing()
        url = url.strip("<>")
        if not url.startswith("http://") and not url.startswith("https://"):
            url = "http://{}".format(url)
        try:
            starttime = time.time()
            requests.get(url, timeout=3)
            ping = Language.get("information.ping_time", ctx) % (time.time() - starttime)
            await ctx.send(Language.get("information.online_ping", ctx).format(url, ping))
        except:
            await ctx.send(Language.get("information.offline_ping", ctx).format(url))

    @commands.guild_only()
    @commands.command()
    async def getemotes(self, ctx):
        """Gets a list of the server's emotes"""
        emotes = ctx.guild.emojis
        if len(emotes) == 0:
            await ctx.send(Language.get("information.no_server_emotes", ctx))
            return
        emotes = ["`:{}:` = {}".format(emote.name, emote) for emote in emotes]
        await ctx.send("\n".join(emotes))

    @commands.command()
    async def osu(self, ctx, *, username:str):
        """Gets an osu! profile stats with the specified name"""
        if not config.enableOsu:
            await ctx.send(Language.get("information.osu_command_disabled", ctx))
            return
        try:
            import osuapi
        except ImportError:
            log.critical("The osu api is enabled, but the osuapi module was not found! Please run \"pip install osuapi\"")
            await ctx.send(Language.get("osu_import_fail", ctx))
            return
        await ctx.channel.trigger_typing()
        api = osuapi.OsuApi(config._osuKey, connector=osuapi.AHConnector())
        try:
            user = await api.get_user(username)
        except osuapi.HTTPError as e:
            if e.code == 401:
                log.critical("An invalid osu! api key was set, please check the config for instructions on how to get a proper api key!")
                await ctx.send(Language.get("information.osu_invalid_key", ctx))
                return
            else:
                log.critical("An unknown error occured while trying to get an osu! profile.")
                await ctx.send(Language.get("information.osu_unknown_error", ctx))
                return
        try:
            user = user[0]
        except IndexError:
            await ctx.send(Language.get("information.no_osu_profile_found", ctx).format(username))
            return
        fields = {Language.get("information.id", ctx):user.user_id, Language.get("information.country", ctx):user.country, Language.get("information.level", ctx):int(user.level), Language.get("information.hits", ctx):user.total_hits, Language.get("information.score", ctx):user.total_score, Language.get("information.accuracy", ctx):"{0:.2f}%".format(user.accuracy), Language.get("information.play_count", ctx):user.playcount, Language.get("information.ranked_score", ctx):user.ranked_score, Language.get("information.a_rank", ctx):user.count_rank_a, Language.get("information.s_rank", ctx):user.count_rank_s, Language.get("information.ss_rank", ctx):user.count_rank_ss}
        embed = make_list_embed(fields)
        embed.title = Language.get("information.osu_stats_title", ctx).format(user.username)
        embed.color = 0xFF00FF
        embed.set_thumbnail(url="http://s.ppy.sh/a/{}".format(user.user_id))
        await ctx.send(embed=embed)

    @commands.command()
    async def emoteinfo(self, ctx, *, emote:discord.Emoji):
        """Gets information on a custom emote (Only works for servers the bot is on)"""
        fields = {Language.get("information.name", ctx):emote.name, Language.get("information.id", ctx):emote.id, Language.get("information.server_origin", ctx):emote.guild.name, Language.get("information.created_on", ctx):format_time(emote.created_at), Language.get("information.colons_required", ctx):emote.require_colons, Language.get("information.managed_by_twitch", ctx):emote.managed}
        embed = make_list_embed(fields)
        embed.title = ":{}:".format(emote.name)
        embed.color = 0xFF0000
        embed.set_thumbnail(url=emote.url)
        await ctx.send(embed=embed)

    @commands.command()
    async def portscan(self, ctx, host:str, ports:str):
        """Uses nmap to scan the specified ports from the specified host"""
        await ctx.channel.trigger_typing()
        forbidden_hosts = ["localhost", "0.0.0.0", "127.0.0.1"]
        if host in forbidden_hosts:
            await ctx.send(Language.get("information.forbidden_host", ctx).format(host))
            return
        scanner = nmap.PortScanner()
        try:
            host = socket.gethostbyname(host)
        except socket.gaierror:
            await ctx.send("`{}` is not a valid address".format(host))
            return
        ports = scanner.scan(host, ports)["scan"][host]["tcp"]
        results = []
        for port, data in ports.items():
            service = data["name"]
            if service == "":
                service = Language.get("information.unknown", ctx)
            results.append(Language.get("information.port_status", ctx).format(port, service, data["state"]))
        await ctx.send(xl.format("\n".join(results)))

    @commands.command()
    async def getnumericip(self, ctx, address:str):
        """Resolves the numeric ip of a domain"""
        try:
            await ctx.send(socket.gethostbyname(address))
        except socket.gaierror:
            await ctx.send(Language.get("information.invalid_address", ctx).format(address))

    @commands.command()
    async def whois(self, ctx, domain:str):
        """Gets whois information on a domain"""
        try:
            info = pythonwhois.get_whois(domain)
        except pythonwhois.shared.WhoisException:
            await ctx.send(Language.get("information.root_server_not_found", ctx))
            return
        except KeyError:
            await ctx.send(Language.get("information.failed_domain_lookup", ctx))
            return
        if info["contacts"]["registrant"] is None:
            await ctx.send(embed=discord.Embed(title=Language.get("information.domain_available_title", ctx), description=Language.get("information.domain_available_description", ctx).format(domain), color=0x00FF00))
            return
        fields = {Language.get("information.registrar", ctx):info["registrar"][0], Language.get("information.registered_on", ctx):format_time(info["creation_date"][0]), Language.get("information.expires_on", ctx):format_time(info["expiration_date"][0]), Language.get("information.last_updated", ctx):format_time(info["updated_date"][0]), Language.get("information.name_servers", ctx):", ".join(info["nameservers"])}
        embed = make_list_embed(fields)
        embed.title = Language.get("information.domain_unavailable", ctx)
        embed.color = 0xFF0000
        await ctx.send(embed=embed)

    @commands.command()
    async def color(self, ctx, *, hexcode:str):
        """Displays the given hex color"""
        await ctx.channel.trigger_typing()
        if not hexcode.startswith("#"):
            hexcode = "#{}".format(hexcode)
        try:
            Image.new("RGBA", (50, 50), hexcode).save("data/color.png")
        except ValueError:
            await ctx.send(Language.get("bot.invalid_color", ctx).format(hexcode))
            return
        await ctx.send(file=discord.File("data/color.png", "{}.png".format(hexcode.strip("#"))))

    @commands.command()
    async def getuserbyid(self, ctx, id:int):
        """Gets a user by id"""
        user = discord.utils.get(list(self.bot.get_all_members()), id=id)
        if not user:
            await ctx.send(Language.get("information.no_mutual_servers", ctx).format(id))
            return
        if user.game:
            game = user.game.name
        fields = {Language.get("information.name", ctx):user.name, Language.get("information.discriminator", ctx):user.discriminator, Language.get("information.id", ctx):user.id, Language.get("information.statud", ctx):str(user.status).replace("dnd", "do not disturb"), Language.get("information.game", ctx):game, Language.get("information.boot", ctx):user.bot}
        embed = make_list_embed(fields)
        embed.title = str(user)
        embed.color = 0xFF0000
        embed.set_thumbnail(url=get_avatar(user))
        await ctx.send(embed=embed)

    @commands.guild_only()
    @commands.command()
    async def roleid(self, ctx, *, role:discord.Role):
        """Gets the id for the specified role"""
        await ctx.send(Language.get("information.role_id", ctx).format(role.name, role.id))

    @commands.command()
    async def timestamp(self, ctx):
        """Displays the current unix timestamp"""
        await ctx.send(str(int(datetime.now().timestamp())))

    @commands.command()
    async def spotify(self, ctx, user:discord.Member=None):
        """Get the current song that you or another user is playing"""
        if user is None:
            user = ctx.author
        activity = ctx.author.activity
        if activity is None:
            await ctx.send("{} is not playing anything on spotify!".format(user.display_name))
            return
        if activity.type == discord.ActivityType.listening and activity.name == "Spotify":
            embed = discord.Embed(description="\u200b")
            embed.add_field(name="Artists", value=", ".join(activity.artists))
            embed.add_field(name="Album", value=activity.album)
            embed.add_field(name="Duration", value=str(activity.duration)[3:].split(".", 1)[0])
            embed.title = "**{}**".format(activity.title)
            embed.set_thumbnail(url=activity.album_cover_url)
            embed.url = "https://open.spotify.com/track/{}".format(activity.track_id)
            embed.color = activity.color
            embed.set_footer(text="{} - is currently playing this song".format(ctx.author.display_name), icon_url=get_avatar(ctx.author))
            await ctx.send(embed=embed)
        else:
            await ctx.send("{} is not playing anything on spotify!".format(user.display_name))
            return

    @commands.command()
    async def twitch(self, ctx, *, name:str):
        """Gets a twitch channel's statistics."""
        if twitch is None:
            await ctx.send("The bot owner did not specify a twitch api key, therefore this command is disabled.")
            return
        try:
            channel = twitch.search.channels(name, limit=1)[0]
        except IndexError:
            await ctx.send("Could not find any channel by the name of **{}**".format(name))
            return
        stream =  twitch.streams.get_stream_by_user(channel["id"])
        streaming = False
        game = None
        if channel["game"]:
            game = channel["game"]
        fields = {"Broadcast Name":channel["status"], "For mature audiences":channel["mature"], "Game":game, "Created On":format_time(channel["created_at"]), "Total Views":format_number(channel["views"]), "Followers":format_number(channel["followers"])}
        if stream is not None:
            streaming = True
            fields["Live Viewers"] = format_number(stream["viewers"])
        fields["Live"] = streaming
        embed = make_list_embed(fields)
        if channel["logo"] is not None:
            embed.set_thumbnail(url=channel["logo"])
        embed.description = channel["description"]
        embed.title = channel["display_name"]
        embed.url = channel["url"]
        if streaming:
            embed.set_image(url=stream["preview"]["large"] + "?v={}".format(random.randint(0, 10000)))
            embed.color = 0xFF0000
        else:
            if channel["video_banner"] is not None:
                embed.set_image(url=channel["video_banner"])
            embed.color = 0x593695
        await ctx.send(embed=embed)

    @commands.command(hidden=True)
    @checks.is_dev()
    async def infodebug(self, ctx, *, shit:str):
        """This is the part where I make 20,000 typos before I get it right"""
        # "what the fuck is with your variable naming" - EJH2
        # seth seriously what the fuck - Robin
        import asyncio
        import os
        import random
        import re
        from datetime import datetime, timedelta
        try:
            rebug = eval(shit)
            if asyncio.iscoroutine(rebug):
                rebug = await rebug
            await ctx.send(py.format(rebug))
        except Exception as damnit:
            await ctx.send(py.format("{}: {}".format(type(damnit).__name__, damnit)))

    @commands.command()
    async def youtube(self, ctx, *, name:str):
        """Gets statistics on a youtube channel"""
        channel = get_youtube_channel(youtubeAPI, name)
        if channel is None:
            await ctx.send("No YouTube channel was found by the name of **{}**".format(name))
            return
        fields = {"Subscribers":format_number(int(channel["statistics"]["subscriberCount"])), "Subscriber Count Hidden":channel["statistics"]["hiddenSubscriberCount"], "Channel View Count":format_number(int(channel["statistics"]["viewCount"])), "Total Videos":format_number(int(channel["statistics"]["videoCount"]))}
        fields["Created On"] = format_time(datetime.strptime(channel["snippet"]["publishedAt"], "%Y-%m-%dT%H:%M:%S.000Z"))
        embed = make_list_embed(fields)
        try:
            embed.set_thumbnail(url=channel["snippet"]["thumbnails"]["high"]["url"])
        except KeyError:
            pass
        try:
            embed.set_image(url=channel["brandingSettings"]["image"]["bannerTvHighImageUrl"])
        except KeyError:
            pass
        embed.description = channel["snippet"]["description"]
        embed.color = 0xFF0000
        embed.title = channel["snippet"]["title"]
        embed.url = "https://youtube.com/channel/{}".format(channel["id"])
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Information(bot))
