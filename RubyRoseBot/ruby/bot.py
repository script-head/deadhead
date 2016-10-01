import os
import sys
import time
import shlex
import shutil
import inspect
import discord
import asyncio
import traceback
import json
import io
import cleverbot
import re
import random
import aiohttp
import platform
import wikipedia
import wikipedia.exceptions
import wolframalpha
import requests
import threading
import cat

from discord import utils
from discord.object import Object
from discord.enums import ChannelType
from discord.voice_client import VoiceClient

from io import BytesIO
from functools import wraps
from textwrap import dedent
from datetime import timedelta, date
from random import choice, shuffle
from collections import defaultdict
from xml.dom import minidom

from ruby.playlist import Playlist
from ruby.player import MusicPlayer
from ruby.config import Config, ConfigDefaults
from ruby.permissions import Permissions, PermissionsDefaults
from ruby.playlist import Playlist
from ruby.utils import load_file, write_file, download_file, sane_round_int, extract_user_id
from ruby.mysql import *

from . import exceptions
from . import downloader
from .opus_loader import load_opus_lib
from .constants import VERSION as BOTVERSION
from .constants import DISCORD_MSG_CHAR_LIMIT, AUDIO_CACHE_PATH
from .constants import VER
from .constants import BDATE as BUILD
from .constants import MAINVER as MVER 
from .constants import BUILD_USERNAME as BUNAME 
from _operator import contains
from .unicode import memes

#I'm just going to pretend that I'm drunk. idk 
#American idiots yas
#dundundundundndndundudnundudnudndundudnundunudndndundudnudndundudnudnudndundundundudnudnudndundundudnudndndnundudndunud
#UDNDUNDUNDUNDUDNUDNDUNDUNDUNDUNDUNDUDNUDNDUNDUNDUNDUNDUNDUNDUNDNUDNDUNDUNDUNDUNDUNDUNDUDNUDNDNDUDNUDNUDNUDNDUUDNUDNU
# DONT WANNA BE AN AMERICAN IDIOT 
# CONTROLLED BY THE MEDIA
# what am i doing with my life
# UDNUDNDUNDUNDUNDUDNUDNUDNDU ND UNUNDU NDU NDUDUNDUNDUNDUNDUNDUNDUDNUUN
# *guitar intensifies*
# yes yes yes yes 
#I did this in RTB...fucking hell. whatever lol
#merlin is a retard
#watch him burn his house down
#-everyone
#
#wtf robin? - CreeperSeth

load_opus_lib()
st = time.time()
default_game = discord.Game(name="with team RWBY")
default_status = discord.Status.dnd
#Fookin fantastic amirite?

#Date vars
halloween = date(2016, 10, 31)

# The fucking changelog var
change_log = [
    "Commands:",
    "+ listservers",
    "+ getserverinfo",
    "+ plzmsgme",
    "+ about",
    "+ yiffinhell",
    "+ pressf",
    "+ halloween",
    "- nickreset",
    "+ halloween",
    "+ daystillhalloween", 
    "+ alex",
    "+ wtf",
    "+ changestatus",
    "- setgame",
    "- nope",
    "+ stream",
    "+ getemojis",
    "+ isitdown",
    "- spamandkys",
    "+ calc",
    "- listids",
    "+ thisishalloween",
    "Other stuff:",
    "Improved some code",
    "Organized some code better",
    "Replaced all ' with \" in strings because 1. I have OCD and it triggers it. 2. I don't use ' to open and close strings",
    "Removed a lot of the # comments that describe what the code does to piss off the people that are new to python discord bots kek"
]
# String vars
owner_id = "169597963507728384"
no_perm = "You do not have permission to use that command."

# Format vars
xl = "```xl\n{0}```"
py = "```py\n{0}```"

# Ansi escape var
ansi_escape = re.compile(r"(\x9B|\x1B\[)[0-?]*[ -\/]*[@-~]")

# Boolean vars
respond = True
cycle = False
lock_status = False

# Array vars
dis_games = [
    discord.Game(name="with Seth"),
    discord.Game(name="on Windows XP"),
    discord.Game(name="with Robin"),
    discord.Game(name="Super Smash Bros. Melee"),
    discord.Game(name="/help for help!"),
    discord.Game(name="with memes"),
    discord.Game(name="with some floof"),
    discord.Game(name="Doom (1993)"),
    discord.Game(name="Doom (2016)"),
    discord.Game(name="DramaNation"),
    discord.Game(name="on 4chan"),
    discord.Game(name="Guns N' Roses"),
    discord.Game(name="stalking Twitter"),
    discord.Game(name="Microsoft Messaging"),
    discord.Game(name="RWBY - Grimm Eclipse"),
    discord.Game(name="with lolis"),
    discord.Game(name="with team RWBY"),
    discord.Game(name="Cyka Strike: Blyat Offensive"),
    discord.Game(name="around with Crescent Rose"),
    discord.Game(name="Visual Studio 2015"),
    discord.Game(name="Grand Theft Auto V"),
    discord.Game(name="Team Fortress 2"),
    discord.Game(name="with VAC bans"),
    discord.Game(name="with Harambe"),
    discord.Game(name="with Master"),
    discord.Game(name="with Maxie"),
    discord.Game(name="with EJH2"),
    discord.Game(name="with discord admins"),
    discord.Game(name="<insert game name here>"),
    discord.Game(name=">inb4 ur mum kills us"),
    discord.Game(name="totally not streaming", url="https://www.twitch.tv/creeperseth", type=1),
    discord.Game(name="with MoonBot"),
    discord.Game(name="with Crimson Dragon"),
    discord.Game(name="with Napsta"),
    discord.Game(name="with Abstract"),
]
suicidalmemes = [
    "what the hell did you do idiot",
    "wtf ok idiot fool",
    "you killed him nice job.",
    "lmao you killed him gg on your killing :ok_hand:",
    "party on his death? lit",
    "fuckin fag wtf no.... y..."
]
throwaf = [
    "a keyboard",
    "a Playstation 4",
    "a PSP with Crash Bandicoot 2 on it",
    "a fur coat",
    "furtrash called art",
    "a british trash can",
    "a raincoat made with :heart:",
    "some shitty pencil, it's definitely useless",
    "a dragon",
    "a Lightning Dragon",
    "Maxie",
    "Robin",
    "a water bucket",
    "water",
    "a shamrock shake",
    "flowers",
    "some fisting",
    "a RoboNitori message",
    "a ice cream cone",
    "hot ass pie, and it's strawberry",
    "a strawberry ice cream cone",
    "Visual Studio 2015",
    "Toshiba Satellite laptop with Spotify, Guild Wars 2 and Visual Studio on it",
    "a compass",
    "honk honk",
    "pomfpomfpomf",
    "🌎",
    "a watermelone",
    "FUCKING PAPERCLIP",
    "HTTP Error 403",
    "Error 429",
    "`never`",
    "`an error that should be regretted of`",
    "Georgia",
    "New York",
    "Nevada",
    "Michigan",
    "Florida",
    "California",
    "TEEEEEEXASSSSSSS",
    "a climaxing dragon picture"
    "Nebraska",
    "an ok ok please message",
    "a pleb called EJH2",
    "15 dust bunnies, a water bottle, and a iron hammer to ban people with",
    "a broken glass (dance bitch)",
    "ok ok",
    "allergy pills",
    "a Chocolate Calculator",
    "probably not Bad Dragon toy",
    "aww yiss a piece of WORLD DOMINATION POWER",
    "a prime minister from Canada",
    "Indiana",
    "a coca-cola bottle",
    "a DJ System",
    "a fridge with wifi enabled",
    "a router",
    "a modem box",
    "a Napstabot",
    "another RoboNitori sentence",
    "a phone",
    "a fan",
    "a pair of earphones",
    "Excel document",
    "Paint Tool SAI painting",
    "Word Document",
    "Visual Studio Project",
    "nerd thing",
    "python 3.5 py",
    "fuckin office tool",
    "clippy",
    "dat boi meme",
    "random.jpeg",
    "Danny DeVito",
    "Deadpool",
    "a Lenovo Keyboard",
    "Life of Pablo",
    "a Mexican called Ambrosio",
    "the most obvious dick master",
    "Motopuffs",
    "the dick master called Motopuffs",
    "a weeaboo",
    "Ryulise, the stupid smash master",
    "death, at its finest",
    "morth, but not in its final form",
    "some flaccid sword",
    "Crescent Rose"
]
insults = [
    "is a fucking pedophile",
    "is a nigger",
    "is so insecure about his penis size because it is smaller than a babies",
    "is just a fucking sterotypical 12 year old saying shit like \"I fucked your mom\" and other shit",
    "is a fucking disguisting, disgraceful, ignorant, pathetic, and discriminative weeaboo!",
    "is a child molester",
    "has a kink with 80 year old men",
    "is the type of person who loves to fap to little girls",
    "has no other purpose in life other than to be retarded and waste people's time",
    "needs to kill itself",
    "is the definition of faggot",
    "has a gamertag, and it is I_Like_To_Rape_Children",
    "loves to fap to discord bots",
    "wants the d",
    "has no life",
    "is a furry",
    "is a furfag",
    "is a worthless piece of shit",
    "80 year old man",
    "lost his virginity to his grandpa",
    "supports abortion",
    "is a cuntrag",
    "is on the sex offender list"
]
honkhonkfgt = [
    "https://i.imgur.com/c53XQCI.gif",
    "https://i.imgur.com/ObWBP14.png",
    "https://i.imgur.com/RZP2tB4.jpg",
    "https://i.imgur.com/oxQ083P.gif",
    "https://i.imgur.com/byBB7ln.jpg",
    "https://i.imgur.com/NvUiLGG.gif",
    "https://i.imgur.com/QDyvO4x.jpg",
    "https://i.imgur.com/HtrRYSS.png",
    "https://i.imgur.com/bvrFQnX.jpg"
]
rubyshit = [
    "http://i.imgur.com/REtCqUO.gif",
    "http://i.imgur.com/yoc2AQk.gif",
    "http://i.imgur.com/tA07mlA.gif",
    "http://i.imgur.com/PMdpTO4.png",
    "http://i.imgur.com/e4B0qhY.jpg",
    "http://i.imgur.com/srgbPCX.gif",
    "http://i.imgur.com/osS1g42.gif",
    "http://i.imgur.com/qRUuMHv.png",
    "http://i.imgur.com/hsxgEzP.gif",
    "http://i.imgur.com/XbrofbY.gif",
    "http://i.imgur.com/ejD61ju.gif",
    "http://i.imgur.com/5R2rJjY.gif",
    "http://i.imgur.com/veuPR57.gif",
    "http://i.imgur.com/OQ7Cl5j.gif",
    "http://i.imgur.com/MuUyWnj.gif",
    "http://i.imgur.com/Hrto0aR.gif",
    "http://i.imgur.com/ueQMNbV.gif",
    "http://i.imgur.com/Ad6E834.gif",
    "http://i.imgur.com/5ZcLiqK.gif",
    "http://i.imgur.com/GOiRtlh.gif",
    "http://i.imgur.com/rqxkH3z.gif",
    "http://i.imgur.com/MvNwOGy.gif",
    "http://i.imgur.com/Dd5x9Af.gif"
]
magic_conch_shell = [
    "It is certain", 
    "It is decidedly so", 
    "Without a doubt", 
    "Yes definitely", 
    "You may rely on it", 
    "As I see it yes", 
    "Most likely", 
    "Outlook good", 
    "Yes", 
    "Signs point to yes", 
    "Reply hazy try again", 
    "Ask again later", 
    "Better not tell you now", 
    "Cannot predict now", 
    "Concentrate and ask again", 
    "Don't count on it", 
    "My reply is no", 
    "My sources say no", 
    "Outlook not so good", 
    "Very doubtful"
]
triggered = [
    "Don't fucking ping me ever again",
    ":eyes: **Did you just ping me?** Oh hellll no!",
    "Oh do you wanna see Jesus?",
    "\*Gets pinged then bans pinger*",
    "**D-D-DID YOU JUST PING ME?** BITCH I'LL BEAT YOUR FUCING ASSSKRFREXE4WV54\n\*TRIGGERED*"
]

# Regex for IP address
ipv4_regex = re.compile(r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b")
ipv6_regex = re.compile(r"(([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(ffff(:0{1,4}){0,1}:){0,1}((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])|([0-9a-fA-F]{1,4}:){1,4}:((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9]))")

class SkipState:
    def __init__(self):
        self.skippers = set()
        self.skip_msgs = set()

    @property
    def skip_count(self):
        return len(self.skippers)

    def reset(self):
        self.skippers.clear()
        self.skip_msgs.clear()

    def add_skipper(self, skipper, msg):
        self.skippers.add(skipper)
        self.skip_msgs.add(msg)
        return self.skip_count


class Response:
    def __init__(self, content, reply=False, delete_after=0):
        self.content = content
        self.reply = reply
        self.delete_after = delete_after


class Ruby(discord.Client):
    def __init__(self, config_file=ConfigDefaults.options_file, perms_file=PermissionsDefaults.perms_file):
        super().__init__()

        self.players = {}
        self.the_voice_clients = {}
        self.voice_client_connect_lock = asyncio.Lock()
        self.voice_client_move_lock = asyncio.Lock()
        self.aiosession = aiohttp.ClientSession(loop=self.loop)

        self.config = Config(config_file)
        self.permissions = Permissions(perms_file, grant_all=[self.config.owner_id])

        self.blacklist = set(load_file(self.config.blacklist_file))
        self.whitelist = set(load_file(self.config.whitelist_file))
        self.autoplaylist = load_file(self.config.auto_playlist_file)
        self.downloader = downloader.Downloader(download_folder="audio_cache")
        self.command_prefix = self.config.command_prefix

        self.exit_signal = None
        if not self.autoplaylist:
            print("Warning: Autoplaylist is empty, disabling.")
            self.config.auto_playlist = False

        self.http.user_agent += " Ruby/%s" % BOTVERSION

        ssd_defaults = {"last_np_msg": None, "auto_paused": False}
        self.server_specific_data = defaultdict(lambda: dict(ssd_defaults))

    def owner_only(func):
        @wraps(func)
        async def wrapper(self, *args, **kwargs):
            orig_msg = self._get_variable("message")

            if not orig_msg or orig_msg.author.id == self.config.owner_id:
                return await func(self, *args, **kwargs)
            else:
                raise exceptions.PermissionsError("Only the owner can use this command", expire_in=30)

        return wrapper

    @staticmethod
    def _fixg(x, dp=2):
        return ("{:.%sf}" % dp).format(x).rstrip("0").rstrip(".")

    def _get_variable(self, name):
        stack = inspect.stack()
        try:
            for frames in stack:
                current_locals = frames[0].f_locals
                if name in current_locals:
                    return current_locals[name]
        finally:
            del stack

    def _get_owner(self, voice=False):
        if voice:
            for server in self.servers:
                for channel in server.channels:
                    for m in channel.voice_members:
                        if m.id == self.config.owner_id:
                            return m
        else:
            return discord.utils.find(lambda m: m.id == self.config.owner_id, self.get_all_members())

    def _delete_old_audiocache(self, path=AUDIO_CACHE_PATH):
        try:
            shutil.rmtree(path)
            return True
        except:
            try:
                os.rename(path, path + "__")
            except:
                return False
            try:
                shutil.rmtree(path)
            except:
                os.rename(path + "__", path)
                return False

        return True

    async def log(self, string, channel=None):
        """
            Logs information to a Discord text channel
            :param channel: - The channel the information originates from
        """
        if channel:
            if self.config.log_subchannels:
                for i in set(self.config.log_subchannels):
                    subchannel = self.get_channel(i)
                    if not subchannel:
                        self.config.log_subchannels.remove(i)
                        print("[Warning] Bot can't find logging subchannel: {}".format(i))
                    else:
                        server = subchannel.server
                        if channel in server.channels:
                            await self.safe_send_message(subchannel, ":stopwatch: `{}` ".format(time.strftime(self.config.log_timeformat)) + string)

            if self.config.log_masterchannel:
                id = self.config.log_masterchannel
                master = self.get_channel(id)
                if not master:
                    self.config.log_masterchannel = None
                    print("[Warning] Bot can't find logging master channel: {}".format(id))
                else:
                    await self.safe_send_message(master, ":stopwatch: `{}` :mouse_three_button: `{}` ".format(time.strftime(self.config.log_timeformat), channel.server.name) + string)

        else:
            if self.config.log_masterchannel:
                id = self.config.log_masterchannel
                master = self.get_channel(id)
                if not master:
                    self.config.log_masterchannel = None
                    print("[Warning] Bot can't find logging master channel: {}".format(id))
                else:
                    await self.safe_send_message(master, ":stopwatch: `{}` ".format(time.strftime(self.config.log_timeformat)) + string)


    async def _auto_summon(self, channel=None):
        owner = self._get_owner(voice=True)
        if owner:
            self.safe_print("Found owner in voice channel \"%s\", attempting to join..." % owner.voice_channel.name)
            await self.cmd_summon(owner.voice_channel, owner, None)
            return owner.voice_channel

    async def _autojoin_channels(self):
        joined_servers = []

        for chid in self.config.autojoin_channels:
            channel = self.get_channel(chid)
            if channel.server in joined_servers:
                print("Already joined a channel in %s, skipping" % channel.server.name)
                continue

            if channel and channel.type == discord.ChannelType.voice:
                self.safe_print("Attempting to autojoin %s in %s" % (channel.name, channel.server.name))

                chperms = channel.permissions_for(channel.server.me)

                if not chperms.connect:
                    self.safe_print("No perms to join \"%s\"." % channel.name)
                    continue

                elif not chperms.speak:
                    self.safe_print("Unable to join \"%s\", can't speak." % channel.name)
                    continue

                try:
                    player = await self.get_player(channel, create=True)

                    if player.is_stopped:
                        player.play()

                    if self.config.auto_playlist:
                        await self.on_finished_playing(player)

                    joined_servers.append(channel.server)
                except Exception as e:
                    if self.config.log_exceptions:
                        await self.log(":warning: Could not join %s\n```python\n%s\n```" % (channel.name, traceback.print_exc()), channel)
                    print("Failed to join", channel.name)
            elif channel:
                if self.config.log_exceptions:
                    await self.log(":warning: Could not join %s because it is a text channel" % channel.name, channel)
                print("Not joining %s on %s, that's a text channel." % (channel.name, channel.server.name))

            else:
                print("Invalid channel id: " + chid)

    async def _wait_delete_msg(self, message, after):
        await asyncio.sleep(after)
        await self.safe_delete_message(message)

    async def _manual_delete_check(self, message, *, quiet=False):
        if self.config.delete_invoking:
            await self.safe_delete_message(message, quiet=quiet)

    async def _check_ignore_non_voice(self, msg):
        vc = msg.server.me.voice_channel

        if not vc or vc == msg.author.voice_channel:
            return True
        else:
            raise exceptions.PermissionsError(
                "you cannot use this command when not in the voice channel (%s)" % vc.name, expire_in=30)

    async def get_voice_client(self, channel):
        if isinstance(channel, Object):
            channel = self.get_channel(channel.id)

        if getattr(channel, "type", ChannelType.text) != ChannelType.voice:
            raise AttributeError("Channel passed must be a voice channel")

        with await self.voice_client_connect_lock:
            server = channel.server
            if server.id in self.the_voice_clients:
                return self.the_voice_clients[server.id]

            s_id = self.ws.wait_for("VOICE_STATE_UPDATE", lambda d: d.get("user_id") == self.user.id)
            _voice_data = self.ws.wait_for("VOICE_SERVER_UPDATE", lambda d: True)

            await self.ws.voice_state(server.id, channel.id)

            s_id_data = await asyncio.wait_for(s_id, timeout=10, loop=self.loop)
            voice_data = await asyncio.wait_for(_voice_data, timeout=10, loop=self.loop)
            session_id = s_id_data.get("session_id")

            kwargs = {
                "user": self.user,
                "channel": channel,
                "data": voice_data,
                "loop": self.loop,
                "session_id": session_id,
                "main_ws": self.ws
            }
            voice_client = VoiceClient(**kwargs)
            self.the_voice_clients[server.id] = voice_client

            retries = 3
            for x in range(retries):
                try:
                    await self.log(":mega: Attempting connection: `%s`" % server.name)
                    print("Attempting connection...")
                    await asyncio.wait_for(voice_client.connect(), timeout=10, loop=self.loop)
                    await self.log(":mega: Connected to: `%s`" % server.name)
                    print("Connection established.")
                    break
                except:
                    print("Failed to connect, retrying (%s/%s)..." % (x+1, retries))
                    await asyncio.sleep(1)
                    await self.ws.voice_state(server.id, None, self_mute=True)
                    await asyncio.sleep(1)

                    if x == retries-1:
                        await self.log(":warning: `%s`: Failed to connect" % server.name)
                        raise exceptions.HelpfulError(
                            "Cannot establish connection to voice chat.  "
                            "Something may be blocking outgoing UDP connections.",

                            "This may be an issue with a firewall blocking UDP.  "
                            "Figure out what is blocking UDP and disable it.  "
                            "It's most likely a system firewall or overbearing anti-virus firewall.  "
                        )

            return voice_client

    async def mute_voice_client(self, channel, mute):
        await self._update_voice_state(channel, mute=mute)

    async def deafen_voice_client(self, channel, deaf):
        await self._update_voice_state(channel, deaf=deaf)

    async def move_voice_client(self, channel):
        await self._update_voice_state(channel)

    async def disconnect_voice_client(self, server):
        if server.id not in self.the_voice_clients:
            return

        if server.id in self.players:
            self.players.pop(server.id).kill()

        await self.the_voice_clients.pop(server.id).disconnect()

    async def disconnect_all_voice_clients(self):
        for vc in self.the_voice_clients.copy():
            await self.disconnect_voice_client(self.the_voice_clients[vc].channel.server)

    async def _update_voice_state(self, channel, *, mute=False, deaf=False):
        if isinstance(channel, Object):
            channel = self.get_channel(channel.id)

        if getattr(channel, "type", ChannelType.text) != ChannelType.voice:
            raise AttributeError("Channel passed must be a voice channel")

        with await self.voice_client_move_lock:
            server = channel.server

            payload = {
                "op": 4,
                "d": {
                    "guild_id": server.id,
                    "channel_id": channel.id,
                    "self_mute": mute,
                    "self_deaf": deaf
                }
            }

            await self.ws.send(utils.to_json(payload))
            self.the_voice_clients[server.id].channel = channel

    async def get_player(self, channel, create=False):
        server = channel.server

        if server.id not in self.players:
            if not create:
                raise exceptions.CommandError(
                    "The bot is not in a voice channel.  "
                    "Use %ssummon to summon it to your voice channel." % self.config.command_prefix)

            voice_client = await self.get_voice_client(channel)

            playlist = Playlist(self)
            player = MusicPlayer(self, voice_client, playlist) \
                .on("play", self.on_play) \
                .on("resume", self.on_resume) \
                .on("pause", self.on_pause) \
                .on("stop", self.on_stop) \
                .on("finished-playing", self.on_finished_playing) \
                .on("entry-added", self.on_entry_added)

            player.skip_state = SkipState()
            self.players[server.id] = player

        return self.players[server.id]

    async def on_play(self, player, entry):
        await self.update_now_playing(entry)
        player.skip_state.reset()

        channel = entry.meta.get("channel", None)
        author = entry.meta.get("author", None)

        if channel and author:
            last_np_msg = self.server_specific_data[channel.server]["last_np_msg"]
            if last_np_msg and last_np_msg.channel == channel:

                async for lmsg in self.logs_from(channel, limit=1):
                    if lmsg != last_np_msg and last_np_msg:
                        await self.safe_delete_message(last_np_msg)
                    if self.config.log_interaction:
                        await self.log(":microphone: `%s` (requested by `%s`) is now playing in **%s**" % (entry.title, entry.meta["author"], player.voice_client.channel.name), channel)

                        self.server_specific_data[channel.server]["last_np_msg"] = None
                    break  # This is probably redundant

            if self.config.now_playing_mentions:
                newmsg = "%s - your song **%s** is now playing in %s!" % (
                    entry.meta["author"].mention, entry.title, player.voice_client.channel.name)
            else:
                newmsg = "Now playing in %s: **%s**" % (
                    player.voice_client.channel.name, entry.title)

            if self.server_specific_data[channel.server]["last_np_msg"]:
                self.server_specific_data[channel.server]["last_np_msg"] = await self.safe_edit_message(last_np_msg, newmsg, send_if_fail=True)
            else:
                self.server_specific_data[channel.server]["last_np_msg"] = await self.safe_send_message(channel, newmsg)

    async def on_resume(self, entry, **_):
        await self.update_now_playing(entry)

    async def on_pause(self, entry, **_):
        await self.update_now_playing(entry, True)

    async def on_stop(self, **_):
        await self.update_now_playing()

    async def on_finished_playing(self, player, **_):
        if not player.playlist.entries and not player.current_entry and self.config.auto_playlist:
            while self.autoplaylist:
                song_url = choice(self.autoplaylist)
                info = await self.downloader.safe_extract_info(player.playlist.loop, song_url, download=False, process=False)

                if not info:
                    self.autoplaylist.remove(song_url)
                    self.safe_print("[Info] Removing unplayable song from autoplaylist: %s" % song_url)
                    write_file(self.config.auto_playlist_file, self.autoplaylist)
                    continue

                if info.get("entries", None):
                    pass

                try:
                    await player.playlist.add_entry(song_url, channel=None, author=None)
                except exceptions.ExtractionError as e:
                    print("Error adding song from autoplaylist:", e)
                    continue

                break

            if not self.autoplaylist:
                print("[Warning] No playable songs in the autoplaylist, disabling.")
                self.config.auto_playlist = False

    async def on_entry_added(self, playlist, entry, **_):
        pass

    async def update_furry_playing_state(self, entry= None, is_paused=False):
        game = None
        
        if self.user.bot:
            activeplayers = sum(1 for p in self.players.values() if p.is_playing)
            if activeplayers < 1:
                asyncio.sleep(5)
                game = dis_games

        elif activeplayers > 1:
            pass

    async def update_now_playing(self, entry=None, is_paused=False):
        game = default_game

        if self.user.bot:
            activeplayers = sum(1 for p in self.players.values() if p.is_playing)
            if activeplayers > 1:
                entry = None
                game = discord.Game(name="on " + str(activeplayers) + " servers")

            elif activeplayers == 1:
                player = discord.utils.get(self.players.values(), is_playing=True)
                entry = player.current_entry

        if entry:
            prefix = u"\u275A\u275A " if is_paused else ""

            name = u"{}{}".format(prefix, entry.title)[:128]
            game = discord.Game(name=name)

        #await self.change_status(game)


    async def safe_send_message(self, dest, content, *, tts=False, expire_in=0, also_delete=None, quiet=False):
        msg = None
        try:
            msg = await self.send_message(dest, content, tts=tts)

            if msg and expire_in:
                asyncio.ensure_future(self._wait_delete_msg(msg, expire_in))

            if also_delete and isinstance(also_delete, discord.Message):
                asyncio.ensure_future(self._wait_delete_msg(also_delete, expire_in))

        except discord.Forbidden:
            if not quiet:
                self.safe_print("Warning: Cannot send message to %s, no permission" % dest.name)

        except discord.NotFound:
            if not quiet:
                self.safe_print("Warning: Cannot send message to %s, invalid channel?" % dest.name)

        return msg

    async def safe_delete_message(self, message, *, quiet=False):
        try:
            return await self.delete_message(message)

        except discord.Forbidden:
            if not quiet:
                self.safe_print("Warning: Cannot delete message \"%s\", no permission" % message.clean_content)

        except discord.NotFound:
            if not quiet:
                self.safe_print("Warning: Cannot delete message \"%s\", message not found" % message.clean_content)

    async def safe_edit_message(self, message, new, *, send_if_fail=False, quiet=False):
        try:
            return await self.edit_message(message, new)

        except discord.NotFound:
            if not quiet:
                self.safe_print("Warning: Cannot edit message \"%s\", message not found" % message.clean_content)
            if send_if_fail:
                if not quiet:
                    print("Sending instead")
                return await self.safe_send_message(message.channel, new)

    def safe_print(self, content, *, end="\n", flush=True):
        sys.stdout.buffer.write((content + end).encode("utf-8", "replace"))
        if flush: sys.stdout.flush()

    async def send_typing(self, destination):
        try:
            return await super().send_typing(destination)
        except discord.Forbidden:
            if self.config.debug_mode:
                print("Could not send typing to %s, no permssion" % destination)

    async def cycle_status(self):
        if cycle is True:
            await self.change_presence(game=random.choice(dis_games))
            await asyncio.sleep(15)
            await self.cycle_status()

    async def mod_log(self, server, thingtolog):
        log_channel = discord.utils.get(server.channels, name="mod-log")
        if log_channel:
            await self.send_message(log_channel, ":information_source: Moderator action: " + thingtolog)

    def format_user(self, insertnerovar):
        return insertnerovar.name + "#" + insertnerovar.discriminator

    def _cleanup(self):
        try:
            self.loop.run_until_complete(self.logout())
        except:
            pass

        pending = asyncio.Task.all_tasks()
        gathered = asyncio.gather(*pending)

        try:
            gathered.cancel()
            self.loop.run_until_complete(gathered)
            gathered.exception()
        except:
            pass

    # noinspection PyMethodOverriding
    def run(self):
        try:
            self.loop.run_until_complete(self.start(*self.config.auth))

        except discord.errors.LoginFailure:
            raise exceptions.HelpfulError(
                "Bot cannot login, bad credentials.",
                "Fix your Email or Password or Token in the options file.  "
                "Remember that each field should be on their own line.")

        finally:
            try:
                self._cleanup()
            except Exception as e:
                print("Error in cleanup:", e)

            self.loop.close()
            if self.exit_signal:
                raise self.exit_signal

    async def logout(self):
        for vc in self.the_voice_clients.values():
            try:
                await vc.disconnect()
            except:
                continue

        return await super().logout()

    async def on_error(self, event, *args, **kwargs):
        ex_type, ex, stack = sys.exc_info()

        if ex_type == exceptions.HelpfulError:
            print("Exception in", event)
            print(ex.message)

            await asyncio.sleep(2)  # don't ask
            await self.logout()

        elif issubclass(ex_type, exceptions.Signal):
            self.exit_signal = ex_type
            await self.logout()

        else:
            traceback.print_exc()

    async def on_ready(self):
        print("\rConnected!  Ruby v%s\n" % BOTVERSION)
        if self.config._abaltoken:
            print("Updating DBots Statistics...")
            r = requests.post("https://bots.discord.pw/api/bots/" + self.user.id + "/stats", json={"server_count": len(self.servers)},
                              headers={
                                  "Authorization": self.config._abaltoken})
            if r.status_code == "200":
                print("Discord Bots Server count updated.")
            elif r.status_code == "401":
                print("An error occurred!")
                

        if self.config.owner_id == self.user.id:
            raise exceptions.HelpfulError(
                "Your OwnerID is incorrect or you've used the wrong credentials.",

                "The bot needs its own account to function.  "
                "The OwnerID is the id of the owner, not the bot.  "
                "Figure out which one is which and use the correct information.")

        self.safe_print("Bot: %s/%s" % (self.user.id, self.format_user(self.user)))

        owner = self._get_owner(voice=True) or self._get_owner()
        if owner and self.servers:
            self.safe_print("Owner: %s/%s\n" % (owner.id, self.format_user(owner)))

        elif self.servers:
            print("Owner could not be found on any server (id: %s)\n" % self.config.owner_id)

        else:
            print("Owner unavailable, bot is not on any servers.")

        print()

        
        if self.config.log_masterchannel:
            print("Logging to master channel:")
            channel = self.get_channel(self.config.log_masterchannel)
            if channel:
                self.safe_print(" - %s/%s" % (channel.server.name.strip(), channel.name.strip()))
        if self.config.log_subchannels:
            print("Logging to subchannels:")
            chlist = [self.get_channel(i) for i in self.config.log_subchannels if i]
            [self.safe_print(" - %s/%s" % (ch.server.name.strip(), ch.name.strip())) for ch in chlist if ch]
        if self.config.log_masterchannel or self.config.log_subchannels:
            print("  Exceptions: " + ["Disabled", "Enabled"][self.config.log_exceptions])
            print("  Interaction: " + ["Disabled", "Enabled"][self.config.log_interaction])
            print("  Downloads: " + ["Disabled", "Enabled"][self.config.log_downloads])
            print("  Time Format: {}".format(self.config.log_timeformat))
        else:
            print("Not logging to any text channels")

        print()

        if self.config.bound_channels:
            print("Bound to text channels:")
            chlist = [self.get_channel(i) for i in self.config.bound_channels if i]
            [self.safe_print(" - %s/%s" % (ch.server.name.strip(), ch.name.strip())) for ch in chlist if ch]
        else:
            print("Not bound to any text channels")

        print()
        print("Options:")

        self.safe_print("  Command prefix: " + self.config.command_prefix)
        print("  Default volume: %s%%" % int(self.config.default_volume * 100))
        print("  Skip threshold: %s votes or %s%%" % (
            self.config.skips_required, self._fixg(self.config.skip_ratio_required * 100)))
        print("  Whitelist: " + ["Disabled", "Enabled"][self.config.white_list_check])
        print("  Now Playing @mentions: " + ["Disabled", "Enabled"][self.config.now_playing_mentions])
        print("  Auto-Summon: " + ["Disabled", "Enabled"][self.config.auto_summon])
        print("  Auto-Playlist: " + ["Disabled", "Enabled"][self.config.auto_playlist])
        print("  Auto-Pause: " + ["Disabled", "Enabled"][self.config.auto_pause])
        print("  Delete Messages: " + ["Disabled", "Enabled"][self.config.delete_messages])
        if self.config.delete_messages:
            print("  Delete Invoking: " + ["Disabled", "Enabled"][self.config.delete_invoking])
        print("  Downloaded songs will be %s" % ["deleted", "saved"][self.config.save_videos])
        print()

        await self.log(":mega: `{}#{}` ready".format(self.user.name, self.user.discriminator, time.strftime("%H:%M:%S"), time.strftime("%d/%m/%y")))

        if not self.config.save_videos and os.path.isdir(AUDIO_CACHE_PATH):
            if self._delete_old_audiocache():
                print("Deleting old audio cache")
                await self.log(":mega: The audio cache was cleared")
            else:
                print("Could not delete old audio cache, moving on.")
                await self.log(":warning: Tried to clear audio cache, encountered a problem")

        if self.config.autojoin_channels:
            await self._autojoin_channels()

        elif self.config.auto_summon:
            print("Attempting to autosummon...", flush=True)

            owner_vc = await self._auto_summon()

            if owner_vc:
                print("Done!", flush=True)
                if self.config.auto_playlist:
                    print("Starting auto-playlist")
                    await self.on_finished_playing(await self.get_player(owner_vc))
            else:
                print("Owner not found in a voice channel, could not autosummon.")
                if self.config.log_exceptions:
                    await self.log(":warning: Tried to autosummon, owner not found in a channel")
        if cycle is True:
            await self.cycle_status()
        else:
            await self.change_presence(game=default_game, status=default_status)

        print()
        # t-t-th-th-that's all folks!

    async def cmd_whitelist(self, message, option, username):
        """
        Usage:
            {command_prefix}whitelist [ + | - | add | remove ] @user

        Adds or removes the user to the whitelist.
        When the whitelist is enabled, whitelisted users are permitted to use bot commands.
        """

        user_id = extract_user_id(username)
        if not user_id:
            raise exceptions.CommandError("Invalid user specified")

        if option not in ["+", "-", "add", "remove"]:
            raise exceptions.CommandError(
                "Invalid switch \"%s\" used, use +, -, add, or remove" % option, expire_in=20
            )

        if option in ["+", "add"]:
            self.whitelist.add(user_id)
            write_file(self.config.whitelist_file, self.whitelist)

            return Response("user has been added to the whitelist", reply=True, delete_after=10)

        else:
            if user_id not in self.whitelist:
                return Response("user is not in the whitelist", reply=True, delete_after=10)

            else:
                self.whitelist.remove(user_id)
                write_file(self.config.whitelist_file, self.whitelist)

                return Response("user has been removed from the whitelist", reply=True, delete_after=10)

    async def cmd_insult(self, message, username):
        """
        Usage:
            {command_prefix}insult username

        Randomly insults the user specified.
        """

        tbhidfucknero = message.content[len(self.command_prefix + "insult "):].strip()
        return Response(tbhidfucknero + " " + random.choice(insults), delete_after=0)

    async def cmd_blacklist(self, message, option, username):
        """
        Usage:
            {command_prefix}blacklist [ + | - | add | remove ] @user

        Adds or removes the user to the blacklist.
        Blacklisted users are forbidden from using bot commands. Blacklisting a user also removes them from the whitelist.
        """

        user_id = extract_user_id(username)
        if not user_id:
            raise exceptions.CommandError("Invalid user specified", expire_in=30)

        if str(user_id) == self.config.owner_id:
            return Response("You can\'t blacklist the owner, you dingus", delete_after=10)

        if option not in ["+", "-", "add", "remove"]:
            raise exceptions.CommandError(
                "Invalid switch \"%s\" used, use +, -, add, or remove" % option, expire_in=20
            )

        if option in ["+", "add"]:
            self.blacklist.add(user_id)
            write_file(self.config.blacklist_file, self.blacklist)

            if user_id in self.whitelist:
                self.whitelist.remove(user_id)
                write_file(self.config.whitelist_file, self.whitelist)
                return Response(
                    "user has been added to the blacklist and removed from the whitelist",
                    reply=True, delete_after=10
                )

            else:
                return Response("user has been added to the blacklist", reply=True, delete_after=10)

        else:
            if user_id not in self.blacklist:
                return Response("user is not in the blacklist", reply=True, delete_after=10)

            else:
                self.blacklist.remove(user_id)
                write_file(self.config.blacklist_file, self.blacklist)

                return Response("user has been removed from the blacklist", reply=True, delete_after=10)

    async def cmd_play(self, player, channel, author, permissions, leftover_args, song_url):
        """
        Usage:
            {command_prefix}play song_link
            {command_prefix}play text to search for
        Adds the song to the playlist.  If a link is not provided, the first
        result from a youtube search is added to the queue.
        """

        song_url = song_url.strip("<>")

        if permissions.max_songs and player.playlist.count_for_user(author) >= permissions.max_songs:
            raise exceptions.PermissionsError(
                "You have reached your playlist item limit (%s)" % permissions.max_songs, expire_in=30
            )

        await self.send_typing(channel)

        if leftover_args:
            song_url = " ".join([song_url, *leftover_args])

        try:
            info = await self.downloader.extract_info(player.playlist.loop, song_url, download=False, process=False)
        except Exception as e:
            raise exceptions.CommandError(e, expire_in=30)

        if not info:
            raise exceptions.CommandError("That video cannot be played.", expire_in=30)

        if info.get("url", "").startswith("ytsearch"):
            info = await self.downloader.extract_info(
                player.playlist.loop,
                song_url,
                download=False,
                process=True,
                on_error=lambda e: asyncio.ensure_future(
                    self.safe_send_message(channel, "```\n%s\n```" % e, expire_in=120), loop=self.loop),
                retry_on_error=True
            )

            if not info:
                raise exceptions.CommandError(
                    "Error extracting info from search string, youtubedl returned no data.  "
                    "You may need to restart the bot if this continues to happen.", expire_in=30
                )

            if not all(info.get("entries", [])):
                return

            song_url = info["entries"][0]["webpage_url"]
            info = await self.downloader.extract_info(player.playlist.loop, song_url, download=False, process=False)


        if "entries" in info:
            if not permissions.allow_playlists and ":search" in info["extractor"] and len(info["entries"]) > 1:
                raise exceptions.PermissionsError("You are not allowed to request playlists", expire_in=30)

            num_songs = sum(1 for _ in info["entries"])

            if permissions.max_playlist_length and num_songs > permissions.max_playlist_length:
                raise exceptions.PermissionsError(
                    "Playlist has too many songs. (%s > %s)" % (num_songs, permissions.max_playlist_length),
                    expire_in=30
                )

            if permissions.max_songs and player.playlist.count_for_user(author) + num_songs > permissions.max_songs:
                raise exceptions.PermissionsError(
                    "Playlist entries + your already queued songs reached limit (%s + %s > %s)" % (
                        num_songs, player.playlist.count_for_user(author), permissions.max_songs),
                    expire_in=30
                )

            if info["extractor"].lower() in ["youtube:playlist", "soundcloud:set", "bandcamp:album"]:
                try:
                    return await self._cmd_play_playlist_async(player, channel, author, permissions, song_url,
                                                               info["extractor"])
                except exceptions.CommandError:
                    raise
                except Exception as e:
                    traceback.print_exc()
                    raise exceptions.CommandError("Error queuing playlist:\n%s" % e, expire_in=30)

            t0 = time.time()

            wait_per_song = 1.2

            procmesg = await self.safe_send_message(
                channel,
                "Gathering playlist information for {} songs{}".format(
                    num_songs,
                    ", ETA: {} seconds".format(self._fixg(
                        num_songs * wait_per_song)) if num_songs >= 10 else "."))

            await self.send_typing(channel)


            entry_list, position = await player.playlist.import_from(song_url, channel=channel, author=author)

            tnow = time.time()
            ttime = tnow - t0
            listlen = len(entry_list)
            drop_count = 0

            if permissions.max_song_length:
                for e in entry_list.copy():
                    if e.duration > permissions.max_song_length:
                        player.playlist.entries.remove(e)
                        entry_list.remove(e)
                        drop_count += 1
                if drop_count:
                    print("Dropped %s songs" % drop_count)

            print("Processed {} songs in {} seconds at {:.2f}s/song, {:+.2g}/song from expected ({}s)".format(
                listlen,
                self._fixg(ttime),
                ttime / listlen,
                ttime / listlen - wait_per_song,
                self._fixg(wait_per_song * num_songs))
            )

            await self.safe_delete_message(procmesg)

            if not listlen - drop_count:
                raise exceptions.CommandError(
                    "No songs were added, all songs were over max duration (%ss)" % permissions.max_song_length,
                    expire_in=30
                )

            reply_text = "Added **%s** songs to be played. Position in queue list: %s"
            btext = str(listlen - drop_count)

        else:
            if permissions.max_song_length and info.get("duration", 0) > permissions.max_song_length:
                raise exceptions.PermissionsError(
                    "Song duration exceeds limit (%s > %s)" % (info["duration"], permissions.max_song_length),
                    expire_in=30
                )

            try:
                entry, position = await player.playlist.add_entry(song_url, channel=channel, author=author)

            except exceptions.WrongEntryTypeError as e:
                if e.use_url == song_url:
                    print("[Warning] Determined incorrect entry type, but suggested url is the same.  Help.")

                if self.config.debug_mode:
                    print("[Info] Assumed url \"%s\" was a single entry, was actually a playlist" % song_url)
                    print("[Info] Using \"%s\" instead" % e.use_url)

                return await self.cmd_play(player, channel, author, permissions, leftover_args, e.use_url)

            reply_text = "Added **%s** to be played. Position in queue list: %s"
            btext = entry.title

        if position == 1 and player.is_stopped:
            position = "Up next!"
            reply_text %= (btext, position)

        else:
            try:
                time_until = await player.playlist.estimate_time_until(position, player)
                reply_text += " - estimated time until playing: %s"
            except:
                traceback.print_exc()
                time_until = ""

            reply_text %= (btext, position, time_until)

        return Response(reply_text, delete_after=30)

    async def _cmd_play_playlist_async(self, player, channel, author, permissions, playlist_url, extractor_type):
        """
        Secret handler to use the async wizardry to make playlist queuing non-"blocking"
        """

        await self.send_typing(channel)
        info = await self.downloader.extract_info(player.playlist.loop, playlist_url, download=False, process=False)

        if not info:
            raise exceptions.CommandError("That playlist cannot be played.")

        num_songs = sum(1 for _ in info["entries"])
        t0 = time.time()

        busymsg = await self.safe_send_message(
            channel, "Processing %s songs..." % num_songs)
        await self.send_typing(channel)

        if extractor_type == "youtube:playlist":
            try:
                entries_added = await player.playlist.async_process_youtube_playlist(
                    playlist_url, channel=channel, author=author)

            except Exception:
                traceback.print_exc()
                raise exceptions.CommandError("Error handling playlist %s queuing." % playlist_url, expire_in=30)

        elif extractor_type.lower() in ["soundcloud:set", "bandcamp:album"]:
            try:
                entries_added = await player.playlist.async_process_sc_bc_playlist(
                    playlist_url, channel=channel, author=author)

            except Exception:
                traceback.print_exc()
                raise exceptions.CommandError("Error handling playlist %s queuing." % playlist_url, expire_in=30)


        songs_processed = len(entries_added)
        drop_count = 0
        skipped = False

        if permissions.max_song_length:
            for e in entries_added.copy():
                if e.duration > permissions.max_song_length:
                    try:
                        player.playlist.entries.remove(e)
                        entries_added.remove(e)
                        drop_count += 1
                    except:
                        pass

            if drop_count:
                print("Dropped %s songs" % drop_count)

            if player.current_entry and player.current_entry.duration > permissions.max_song_length:
                await self.safe_delete_message(self.server_specific_data[channel.server]["last_np_msg"])
                self.server_specific_data[channel.server]["last_np_msg"] = None
                skipped = True
                player.skip()
                entries_added.pop()

        await self.safe_delete_message(busymsg)

        songs_added = len(entries_added)
        tnow = time.time()
        ttime = tnow - t0
        wait_per_song = 1.2

        print("Processed {}/{} songs in {} seconds at {:.2f}s/song, {:+.2g}/song from expected ({}s)".format(
            songs_processed,
            num_songs,
            self._fixg(ttime),
            ttime / num_songs,
            ttime / num_songs - wait_per_song,
            self._fixg(wait_per_song * num_songs))
        )

        if not songs_added:
            basetext = "No songs were added, all songs were over max duration (%ss)" % permissions.max_song_length
            if skipped:
                basetext += "\nAdditionally, the current song was skipped for being too long."

            raise exceptions.CommandError(basetext, expire_in=30)

        return Response("Enqueued {} songs to be played in {} seconds".format(
            songs_added, self._fixg(ttime, 1)), delete_after=30)

    async def cmd_search(self, player, channel, author, permissions, leftover_args):
        """
        Usage:
            {command_prefix}search [service] [number] query
        Searches a service for a video and adds it to the queue.
        - service: any one of the following services:
            - youtube (yt) (default if unspecified)
            - soundcloud (sc)
            - yahoo (yh)
        - number: return a number of video results and waits for user to choose one
          - defaults to 1 if unspecified
          - note: If your search query starts with a number,
                  you must put your query in quotes
            - ex: {command_prefix}search 2 "I ran seagulls"
        """

        if permissions.max_songs and player.playlist.count_for_user(author) > permissions.max_songs:
            raise exceptions.PermissionsError(
                "You have reached your playlist item limit (%s)" % permissions.max_songs,
                expire_in=30
            )

        def argcheck():
            if not leftover_args:
                raise exceptions.CommandError(
                    "Please specify a search query.\n%s" % dedent(
                        self.cmd_search.__doc__.format(command_prefix=self.config.command_prefix)),
                    expire_in=60
                )

        argcheck()

        try:
            leftover_args = shlex.split(" ".join(leftover_args))
        except ValueError:
            raise exceptions.CommandError("Please quote your search query properly.", expire_in=30)

        service = "youtube"
        items_requested = 3
        max_items = 10 
        services = {
            "youtube": "ytsearch",
            "soundcloud": "scsearch",
            "yahoo": "yvsearch",
            "yt": "ytsearch",
            "sc": "scsearch",
            "yh": "yvsearch"
        }

        if leftover_args[0] in services:
            service = leftover_args.pop(0)
            argcheck()

        if leftover_args[0].isdigit():
            items_requested = int(leftover_args.pop(0))
            argcheck()

            if items_requested > max_items:
                raise exceptions.CommandError("You cannot search for more than %s videos" % max_items)

        if leftover_args[0][0] in "\"'":
            lchar = leftover_args[0][0]
            leftover_args[0] = leftover_args[0].lstrip(lchar)
            leftover_args[-1] = leftover_args[-1].rstrip(lchar)

        search_query = "%s%s:%s" % (services[service], items_requested, " ".join(leftover_args))

        search_msg = await self.send_message(channel, "Searching for videos...")
        await self.send_typing(channel)

        try:
            info = await self.downloader.extract_info(player.playlist.loop, search_query, download=False, process=True)

        except Exception as e:
            await self.safe_edit_message(search_msg, str(e), send_if_fail=True)
            return
        else:
            await self.safe_delete_message(search_msg)

        if not info:
            return Response("No videos found.", delete_after=30)

        def check(m):
            return (
                m.content.lower()[0] in "yn" or
                m.content.lower().startswith("{}{}".format(self.config.command_prefix, "search")) or
                m.content.lower().startswith("exit"))

        for e in info["entries"]:
            result_message = await self.safe_send_message(channel, "Result %s/%s: %s" % (
                info["entries"].index(e) + 1, len(info["entries"]), e["webpage_url"]))

            confirm_message = await self.safe_send_message(channel, "Is this ok? Type `y`, `n` or `exit`")
            response_message = await self.wait_for_message(30, author=author, channel=channel, check=check)

            if not response_message:
                await self.safe_delete_message(result_message)
                await self.safe_delete_message(confirm_message)
                return Response("Ok nevermind.", delete_after=30)

            elif response_message.content.startswith(self.config.command_prefix) or \
                    response_message.content.lower().startswith("exit"):

                await self.safe_delete_message(result_message)
                await self.safe_delete_message(confirm_message)
                return

            if response_message.content.lower().startswith("y"):
                await self.safe_delete_message(result_message)
                await self.safe_delete_message(confirm_message)
                await self.safe_delete_message(response_message)

                await self.cmd_play(player, channel, author, permissions, [], e["webpage_url"])

                return Response("Alright, coming right up!", delete_after=30)
            else:
                await self.safe_delete_message(result_message)
                await self.safe_delete_message(confirm_message)
                await self.safe_delete_message(response_message)

        return Response("Oh well :frowning:", delete_after=30)

    async def cmd_np(self, player, channel, server, message):
        """
        Usage:
            {command_prefix}np
        Displays the current song in chat.
        """

        if player.current_entry:
            if self.server_specific_data[server]["last_np_msg"]:
                await self.safe_delete_message(self.server_specific_data[server]["last_np_msg"])
                self.server_specific_data[server]["last_np_msg"] = None

            song_progress = str(timedelta(seconds=player.progress)).lstrip("0").lstrip(":")
            song_total = str(timedelta(seconds=player.current_entry.duration)).lstrip("0").lstrip(":")
            prog_str = "`[%s/%s]`" % (song_progress, song_total)

            if player.current_entry.meta.get("channel", False) and player.current_entry.meta.get("author", False):
                np_text = "Now Playing: **%s** added by **%s** %s\n" % (
                    player.current_entry.title, player.current_entry.meta["author"].name, prog_str)
            else:
                np_text = "Now Playing: **%s** %s\n" % (player.current_entry.title, prog_str)

            self.server_specific_data[server]["last_np_msg"] = await self.safe_send_message(channel, np_text)
            await self._manual_delete_check(message)
        else:
            return Response(
                "There are no songs queued! Queue something with {}play.".format(self.config.command_prefix),
                delete_after=30
            )

    async def cmd_summon(self, message, channel, author, voice_channel):
        """
        Usage:
            {command_prefix}summon
        Call the bot to the summoner's voice channel.
        """

        if not author.voice_channel:
            raise exceptions.CommandError(
                "Get your lazy good for nothing ass in a voice channel before giving me demands bitch. (AUTHOR_NOT_IN_CHANNEL)")

        voice_client = self.the_voice_clients.get(channel.server.id, None)
        if voice_client and voice_client.channel.server == author.voice_channel.server:
            await self.safe_send_message(message.channel, "Joined ***" + message.author.voice_channel.name + "***.")
            await self.move_voice_client(author.voice_channel)
            return

        chperms = author.voice_channel.permissions_for(author.voice_channel.server.me)

        if not chperms.connect:
            self.safe_print("Cannot join channel \"%s\", no permission." % author.voice_channel.name)
            return Response(
                "```Cannot join channel \"%s\", no permission.```" % author.voice_channel.name,
                delete_after=25
            )

        elif not chperms.speak:
            self.safe_print("Will not join channel \"%s\", no permission to speak." % author.voice_channel.name)
            return Response(
                "```Will not join channel \"%s\", no permission to speak.```" % author.voice_channel.name,
                delete_after=25
            )

        player = await self.get_player(author.voice_channel, create=True)

        if player.is_stopped:
            player.play()

        if self.config.auto_playlist:
            await self.on_finished_playing(player)

    async def cmd_pause(self, message, player):
        """
        Usage:
            {command_prefix}pause
        Pauses playback of the current song.
        """

        if player.is_playing:
            await self.safe_send_message(message.channel, "Song paused.")
            player.pause()

        else:
            raise exceptions.CommandError("I'm not playing anything.", expire_in=30)

    async def cmd_resume(self, message, player):
        """
        Usage:
            {command_prefix}resume
        Resumes playback of a paused song.
        """

        if player.is_paused:
            await self.safe_send_message(message.channel, "Song resumed.")
            player.resume()

        else:
            raise exceptions.CommandError("I'm not playing anything, nor its not paused.", expire_in=30)

    async def cmd_shuffle(self, channel, player):
        """
        Usage:
            {command_prefix}shuffle
        Shuffles the playlist.
        """

        player.playlist.shuffle()

        cards = [":spades:", ":clubs:", ":hearts:", ":diamonds:"]
        hand = await self.send_message(channel, " ".join(cards))
        await asyncio.sleep(0.6)

        for x in range(4):
            shuffle(cards)
            await self.safe_edit_message(hand, " ".join(cards))
            await asyncio.sleep(0.6)

        await self.safe_delete_message(hand, quiet=True)
        return Response(":ok_hand: shuffled af", delete_after=15)

    async def cmd_clear(self, player, author):
        """
        Usage:
            {command_prefix}clear
        Clears the playlist.
        """

        player.playlist.clear()
        return Response(
            "Cleared the playlist.... I bet there\'s some stupid songs in there that killed it. Oh well, what happen must happen.",
            delete_after=20)

    async def cmd_skip(self, player, channel, author, message, permissions, voice_channel):
        """
        Usage:
            {command_prefix}skip
        Skips the current song when enough votes are cast, or by the bot owner.
        """

        if player.is_stopped:
            raise exceptions.CommandError("Can't skip....? I'm not playing anything!", expire_in=20)

        if not player.current_entry:
            if player.playlist.peek():
                if player.playlist.peek()._is_downloading:
                    print(player.playlist.peek()._waiting_futures[0].__dict__)
                    return Response("The next song (%s) is downloading, please wait." % player.playlist.peek())

                elif player.playlist.peek().is_downloaded:
                    print("The next song will be played shortly.  Please wait.")
                else:
                    print("Something odd is happening.  "
                          "You might want to restart the bot if it doesn't start working.")
            else:
                print("Something strange is happening.  "
                      "You might want to restart the bot if it doesn't start working.")

        if author.id == self.config.owner_id or permissions.instaskip:
            player.skip()
            await self._manual_delete_check(message)
            return

        num_voice = sum(1 for m in voice_channel.voice_members if not (
            m.deaf or m.self_deaf or m.id in [self.config.owner_id, self.user.id]))

        num_skips = player.skip_state.add_skipper(author.id, message)

        skips_remaining = min(self.config.skips_required,
                              sane_round_int(num_voice * self.config.skip_ratio_required)) - num_skips

        if skips_remaining <= 0:
            player.skip()
            return Response(
                "your skip for **{}** was acknowledged."
                "\nThe vote to skip has been passed.{}".format(
                    player.current_entry.title,
                    " Next song coming up!" if player.playlist.peek() else ""
                ),
                reply=True,
                delete_after=20
            )

        else:
            return Response(
                "your skip for **{}** was acknowledged."
                "\n**{}** more {} required to vote to skip this song.".format(
                    player.current_entry.title,
                    skips_remaining,
                    "person is" if skips_remaining == 1 else "people are"
                ),
                reply=True,
                delete_after=20
            )

    async def cmd_volume(self, message, player, new_volume=None):
        """
        Usage:
            {command_prefix}volume (+/-)[volume]
        Sets the playback volume. Accepted values are from 1 to 200.
        Putting + or - before the volume will make the volume change relative to the current volume.
        Volume past 100% is now accepted, but only use it if you want earbusting earrape.
        """

        if not new_volume:
            return Response("Current volume: `%s%%`" % int(player.volume * 200), reply=True, delete_after=20)

        relative = False
        if new_volume[0] in "+-":
            relative = True

        try:
            new_volume = int(new_volume)

        except ValueError:
            raise exceptions.CommandError(
                "{} <-- Really? I know you can do better. It\'s obviously some shameful decimal number, or it\'s not a fucking number. Think harder next time.".format(
                    new_volume), expire_in=20)

        if relative:
            vol_change = new_volume
            new_volume += (player.volume * 200)

        old_volume = int(player.volume * 200)

        if 0 < new_volume <= 200:
            player.volume = new_volume / 200.0

            return Response("updated volume from %d to %d" % (old_volume, new_volume), reply=True, delete_after=20)

        else:
            if relative:
                raise exceptions.CommandError(
                    "Unreasonable volume change provided: {}{:+} -> {}%.  Provide a change between {} and {:+}.".format(
                        old_volume, vol_change, old_volume + vol_change, 1 - old_volume, 200 - old_volume),
                    expire_in=20)
            else:
                raise exceptions.CommandError(
                    "Unreasonable volume provided: {}%. Choose a number that\"s 1-200.".format(new_volume),
                    expire_in=20)

    async def cmd_queue(self, channel, player):
        """
        Usage:
            {command_prefix}queue
        Prints the current song queue.
        """

        lines = []
        unlisted = 0
        andmoretext = "* ... and %s more*" % ("x" * len(player.playlist.entries))

        if player.current_entry:
            song_progress = str(timedelta(seconds=player.progress)).lstrip("0").lstrip(":")
            song_total = str(timedelta(seconds=player.current_entry.duration)).lstrip("0").lstrip(":")
            prog_str = "`[%s/%s]`" % (song_progress, song_total)

            if player.current_entry.meta.get("channel", False) and player.current_entry.meta.get("author", False):
                lines.append("Now Playing: **%s** added by **%s** %s\n" % (
                    player.current_entry.title, player.current_entry.meta["author"].name, prog_str))
            else:
                lines.append("Now Playing: **%s** %s\n" % (player.current_entry.title, prog_str))

        for i, item in enumerate(player.playlist, 1):
            if item.meta.get("channel", False) and item.meta.get("author", False):
                nextline = "`{}.` **{}** added by **{}**".format(i, item.title, item.meta["author"].name).strip()
            else:
                nextline = "`{}.` **{}**".format(i, item.title).strip()

            currentlinesum = sum(len(x) + 1 for x in lines)

            if currentlinesum + len(nextline) + len(andmoretext) > DISCORD_MSG_CHAR_LIMIT:
                if currentlinesum + len(andmoretext):
                    unlisted += 1
                    continue

            lines.append(nextline)

        if unlisted:
            lines.append("\n*... and %s more*" % unlisted)

        if not lines:
            lines.append(
                "No songs, queue something with {}play.".format(self.config.command_prefix))

        message = "\n".join(lines)
        return Response(message, delete_after=30)

    async def cmd_pldump(self, channel, song_url):
        """
        Usage:
            {command_prefix}pldump url
        Dumps the individual urls of a playlist
        """

        try:
            info = await self.downloader.extract_info(self.loop, song_url.strip("<>"), download=False, process=False)
        except Exception as e:
            raise exceptions.CommandError("Could not extract info from input url\n%s\n" % e, expire_in=25)

        if not info:
            raise exceptions.CommandError("Could not extract info from input url, no data.", expire_in=25)

        if not info.get("entries", None):

            if info.get("url", None) != info.get("webpage_url", info.get("url", None)):
                raise exceptions.CommandError("This does not seem to be a playlist.", expire_in=25)
            else:
                return await self.cmd_pldump(channel, info.get(""))

        linegens = defaultdict(lambda: None, **{
            "youtube": lambda d: "https://www.youtube.com/watch?v=%s" % d["id"],
            "soundcloud": lambda d: d["url"],
            "bandcamp": lambda d: d["url"]
        })

        exfunc = linegens[info["extractor"].split(":")[0]]

        if not exfunc:
            raise exceptions.CommandError("Could not extract info from input url, unsupported playlist type.",
                                          expire_in=25)

        with BytesIO() as fcontent:
            for item in info["entries"]:
                fcontent.write(exfunc(item).encode("utf8") + b"\n")

            fcontent.seek(0)
            await self.send_file(channel, fcontent, filename="playlist.txt",
                                 content="Here's the url dump for <%s>" % song_url)

        return Response(":mailbox_with_mail:", delete_after=20)

    async def cmd_perms(self, author, channel, server, permissions):
        """
        Usage:
            {command_prefix}perms

        Sends the user a list of their permissions.
        """

        lines = ["Command permissions in %s\n" % server.name, "```", "```"]

        for perm in permissions.__dict__:
            if perm in ["user_list"] or permissions.__dict__[perm] == set():
                continue

            lines.insert(len(lines) - 1, "%s: %s" % (perm, permissions.__dict__[perm]))

        await self.send_message(author, "\n".join(lines))
        return Response("Check them PMs fam", delete_after=20)

    async def cmd_dab(self, message):
        return Response("http://i.giphy.com/lae7QSMFxEkkE.gif", delete_after=0)

    async def cmd_help2(self):
        """
        Usage:
            {command_prefix}help

        Prints a help message"""

        helpmsg = "**Commands**\n```"
        commands = []

        for att in dir(self):
            if att.startswith("cmd_") and att != "cmd_help":
                command_name = att.replace("cmd_", "").lower()
                commands.append("{}{}".format(self.config.command_prefix, command_name))

        helpmsg += "\n".join(commands)
        helpmsg += "```"
        helpmsg += "http://ruby.creeperseth.com"

        return Response(helpmsg, reply=True, delete_after=60)

    async def cmd_ver(self):
        return Response("`Ver. " + VER + " " + BUILD + "`", delete_after=0)

    @owner_only
    async def cmd_setavatar(self, message, url=None):
        """
        Usage:
            {command_prefix}setavatar [url]
        Changes the bot's avatar.
        Attaching a file and leaving the url parameter blank also works.
        """

        if message.attachments:
            thing = message.attachments[0]["url"]
        else:
            thing = url.strip("<>")

        try:
            with aiohttp.Timeout(10):
                async with self.aiosession.get(thing) as res:
                    await self.edit_profile(avatar=await res.read())
        except Exception as e:
            raise exceptions.CommandError("Unable to change avatar: %s" % e, expire_in=20)

        return Response("Ooh, I look better in this picture, don't I?", delete_after=20)

    async def cmd_ban(self, message, username):
        """
        Usage: {command_prefix}ban @user
        Bans the user, and deletes 7 days of messages from the user prior to using the command.
        """
        user_id = extract_user_id(username)
        member = discord.utils.find(lambda mem: mem.id == str(user_id), message.channel.server.members)
        if not member:
            await self.send_message(message.channel, "User not found, make sure you are using a @mention")
            return
        mod_role_name = read_data_entry(message.server.id, "mod-role")
        botcommander = discord.utils.get(message.author.roles, name=mod_role_name)
        if not botcommander:
            raise exceptions.CommandError("ou must have the \""+ mod_role_name + "\" role in order to use that command.", expire_in=30)
        try:
            await self.ban(member, delete_message_days=7)
            neroishot = self.format_user(message.author)
            name = self.format_user(member)
            await self.mod_log(message.server, "`" + neroishot + "` banned `" + name + "`")
            return Response(neroishot + " banned " + name, delete_after=0)
        except discord.Forbidden:
            return Response("I do not have the proper permissions to ban that user.", reply=True)
        except discord.HTTPException:
            return Response("Banning failed due to HTTPException error.", reply=True)

    @owner_only
    async def cmd_ruby(self, message, client):
        """
        Ruby.
        default status, bye, sysinfo, dbupdate, cycle status, lock status
        Only CreeperSeth#9790 is allowed, or the Bot Owner if this isn't the main bot, Ruby Rose#2414
        """
        global random_game
        global cycle
        global lock_status
        if message.content[len(self.command_prefix + "ruby "):].strip() == "default status":
            await self.change_presence(game=default_game, status=default_status)
            return Response("(!) Set back to default status", delete_after=0)
        elif message.content[len(self.command_prefix + "ruby "):].strip() == "bye":
            await self.leave_server(message.server)
        elif message.content[len(self.command_prefix + "ruby "):].strip() == "cleargame":
            await self.change_presence(game=None)
            return Response("done", delete_after=15)
        elif message.content[len(self.command_prefix + "ruby "):].strip() == "sysinfo":
            await self.safe_send_message(message.channel, platform.uname())
        elif message.content[len(self.command_prefix + "ruby "):].strip() == "dbupdate":
            if not self.config._abaltoken:
                return Response("No Authorization token was specified in the config")
            abalscount = len(self.servers)
            r = requests.post("https://bots.discord.pw/api/bots/" + self.user.id + "/stats", json={"server_count": abalscount}, headers={"Authorization": self.config._abaltoken})
            if r.status_code == int(200):
                print("DBots Stats updated manually via ruby")
                await self.send_message(message.channel, "Updated Discord Bots server count!")
            else:
                print("Error occured while trying to update stats")
                await self.send_message(message.channel, "Error occurred when trying to update, here's the error code: {}".format(r.status_code))
        elif message.content[len(self.command_prefix + "ruby "):].strip() == "cycle status":
            if cycle is False:
                cycle = True
                await self.cycle_status()
            if cycle is True:
                cycle = False
                await self.change_presence(game=default_game, status=default_status)
            return Response("Cycling status is now " + str(cycle))
        elif message.content[len(self.command_prefix + "ruby "):].strip() == "lock status":
            if lock_status is False:
                lock_status = True
                return Response("Status is now locked")
            if lock_status is True:
                lock_status = False
                return Response("Status is no longer locked")

    async def cmd_hentai(self, message):
        await self.send_message(message.channel, "I know you love fapping to lolis, but come on bro, those lolis are on the internet... not in discord. Just look around and you will find them.")
        await self.log(":warning: lol attempted hentai detected. Username: `{}` Server: `{}`".format(message.author.name, message.server.name))
        #Watch Felix be all up in this one first

    async def cmd_e621(self, channel, message, tags):
        bot = discord.utils.get(message.server.members, name=self.user.name)
        nsfw = discord.utils.get(bot.roles, name="NSFW")
        nsfw_channel_name = read_data_entry(message.server.id, "nsfw-channel")
        if not channel.name == nsfw_channel_name:
            if not nsfw:
                raise exceptions.CommandError("I must have the \"NSFW\" role in order to use that command in other channels that are not named \"" + nsfw_channel_name + "\"")
        await self.send_typing(message.channel)
        boobs = message.content[len(self.command_prefix + "e621 "):].strip()
        download_file("https://e621.net/post/index.xml?tags=" + boobs, "data/e621.xml")
        xmldoc = minidom.parse("data/e621.xml")
        itemlist = xmldoc.getElementsByTagName("file_url")
        count = xmldoc.getElementsByTagName("posts")
        cnt = count[0].attributes["count"].value
        if (len(itemlist) == 0):
            await self.send_message(message.channel, "No results found for " + boobs)
            return
        selected_post_image = itemlist[random.randint(1, len(itemlist))].childNodes[0].data
        await self.send_message(message.channel, "Showing 1 of " + cnt + " results for " + boobs + "\n" + selected_post_image)
        
    async def cmd_rule34(self, channel, message, tags):
        bot = discord.utils.get(message.server.members, name=self.user.name)
        nsfw = discord.utils.get(bot.roles, name="NSFW")
        nsfw_channel_name = read_data_entry(message.server.id, "nsfw-channel")
        if not channel.name == nsfw_channel_name:
            if not nsfw:
                raise exceptions.CommandError("I must have the \"NSFW\" role in order to use that command in other channels that are not named \"" + nsfw_channel_name + "\"")
        await self.send_typing(message.channel)
        boobs = message.content[len(self.command_prefix + "rule34 "):].strip()
        download_file("http://rule34.xxx/index.php?page=dapi&s=post&q=index&tags=" + boobs, "data/rule34.xml")
        xmldoc = minidom.parse("data/rule34.xml")
        itemlist = xmldoc.getElementsByTagName("post")
        count = xmldoc.getElementsByTagName("posts")
        cnt = count[0].attributes["count"].value
        if (len(itemlist) == 0):
            await self.send_message(message.channel, "No results found for " + boobs)
            return
        selected_post_image = "http:" + itemlist[random.randint(1, len(itemlist))].attributes["file_url"].value
        await self.send_message(message.channel, "Showing 1 of " + cnt + " results for " + boobs + "\n" + selected_post_image)

    @owner_only
    async def cmd_renamebot(self, message):
        """
        Renames the bot.
            Part from the RTB System.
        """
        botrenamed = message.content[len(self.command_prefix + "renamebot "):].strip()
        await self.edit_profile(username=message.content[len(self.command_prefix + "renamebot "):].strip())
        return Response("Bot name changed to `" + botrenamed + "`", delete_after=5)
        if discord.errors.ClientException:
            return Response("Either you aren't a bot account, or you didn't put a name in. Either one.", delete_after=0)

    async def cmd_wiki(self, query:str, channel, message):
        """
        Wikipedia.
        Search the infinite pages!
        {}wikipedia (page)
        """
        cont2 = message.content[len(self.command_prefix + "wiki "):].strip()
        cont = re.sub(r"\s+", "_", query)
        q = wikipedia.page(query)
        await self.send_typing(channel)
        await self.send_message(message.channel, "{}:\n```\n{}\n```\nFor more information, visit <{}>".format(q.title,wikipedia.summary(query, sentences=5),q.url))
        await self.safe_send_message(message.channel, cont)
        if wikipedia.exceptions.PageError == True:
            await self.safe_send_message(message.channel, "Error 404. Try another.")
        elif wikipedia.exceptions.DisambiguationError == True:
            await self.safe_send_message(message.channel, "Too many alike searches, please narrow it down more...")

    async def cmd_rate(self, message):
        """
        Rate you or your idiot friends! They might not be idiots but still. It's with love <3
        {}rate (player/@mention/name/whatever)
        """
        drewisafurry = random.randint(1, 10) #I can't say how MUCH of a furry Drew is. Or known as Printendo
        if message.content[len(self.command_prefix + "rate "):].strip() == "<@163698730866966528>":
            await self.safe_send_message(message.channel, "I give myself a ***-1/10***, just because.") #But guess what, Emil's a fucking furry IN DENIAL, so that's even worse. Don't worry, at least Drew's sane.
        elif message.content[len(self.command_prefix + "rate "):].strip() != "<@163698730866966528>":
            await self.safe_send_message(message.channel, "I give `" + message.content[len(self.command_prefix + "rate "):].strip().replace("@everyone", ">insert attempt to tag everyone here").replace("@here", ">attempt to tag online users here") + "` a ***" + drewisafurry + "/10***")
        
    async def cmd_asshole(self, message):
        await self.send_file(message.channel, "imgs/asshole.jpg")

    async def cmd_lameme(self, message):
        await self.send_message(message.channel, "la meme xD xD xD")
        asyncio.sleep(5)
        await self.send_file(message.channel, "imgs/lameme.jpg")

    async def cmd_honk(self):
        return Response(random.choice(honkhonkfgt), delete_after=0)

    async def cmd_throw(self, message):
        if message.content[len(self.command_prefix + "throw "):].strip() == message.author.mention:
            return Response("throws " + random.choice(throwaf) + " towards you", delete_after=0)
        elif message.content == "/throw":
            return Response("throws " + random.choice(throwaf) + " towards you", delete_after=0)
        elif message.content[len(self.command_prefix + "throw "):].strip() == "<@!163698730866966528>":
            return Response("you are throwin ***NOTHIN*** to me, ok? ok.", delete_after=15)
        elif message.content[len(self.command_prefix + "throw "):].strip() != message.author.mention:
            return Response("throws " + random.choice(throwaf) + " to " + message.content[len(self.command_prefix + "throw "):].strip(), delete_after=0)

    async def cmd_notifydev(self, message, themessage):
        await self.send_typing(message.channel)
        await self.send_message(message.channel, "Alerted, might as well check your PMs.")
        await self.send_message(discord.User(id="169597963507728384"), "New message from `" + message.author.name + "` Discrim: `" + message.author.discriminator + "` ID: `" + message.author.id + "` Server Name: `" + message.author.server.name + "` Message: `" + message.content[len(self.command_prefix + "notifydev "):].strip() + "`")
        await self.send_message(message.author, "You have sent a message to <@169597963507728384>, the developer. Your message that was sent was `" + message.content[len(self.command_prefix + "notifydev "):].strip() + "`. You are not able to respond via the bot, <@169597963507728384> should send a message back to you shortly via PM.")
        await self.log(":information_source: Message sent to <@169597963507728384> via the notifydev command: `" + message.content[len(self.command_prefix + "notifydev "):].strip() + "`")

    async def cmd_fursecute(self, message, mentions, fursona):
        """
        Fursecution! Command totally not stolen from some Minecraft server.
        Usage: {command_prefix}fursecute @mention "furry species"
        """
        fursona = message.content[len(self.command_prefix + "fursecute " + mentions):].strip()
        await self.send_typing(message.channel)
        asyncio.sleep(15)
        await self.send_message(message.channel, "Uh-oh! Retard alert! Retard alert, class!")
        asyncio.sleep(15)
        await self.send_message(message.channel, mentions + ", do you really believe you're a " + fursona + ", bubblehead?!")
        asyncio.sleep(15)
        await self.send_message(message.channel, "Come on, you, you're going to have to sit in the dunce chair.")

    async def cmd_nick(self, message, username, thingy):
        try:
            thingy = message.content[len(self.command_prefix + "nick " + username):].strip()
            await self.change_nickname(username, thingy)
            await self.send_message(message.channel, "Changed nickname of " + username + "to " + thingy)
        except discord.errors.Forbidden:
            await self.send_message(message.channel, xl.format("Whoops, there's an error.\n discord.errors.Forbidden: FORBIDDEN (status code: 403): Privilege is too low... \n Discord bot is forbidden to change the users nickname."))

    @owner_only
    async def cmd_msgfags(self, message, id, reason):
        reason = message.content[len(self.command_prefix + "msgfags " + id):].strip()
        await self.send_message(discord.User(id=id), reason)
        await self.log(":information_source: " + message.author.name + "sent a warning to ID #: `" + id + "`")

    async def cmd_help(self):
        return Response("Help List: http://ruby.creeperseth.com Any other help? DM @CreeperSeth#9790 for more help, or do `" + self.command_prefix + "serverinv` to join Ruby's Fallout Shelter for some Ruby help somewhere.", delete_after=0)
    
    async def cmd_serverinv(self, author):
        await self.safe_send_message(author, "https://discord.gg/enDDbMC - If you came for help, ask for CreeperSeth. If the link is expired do `" + self.command_prefix + "notifydev` and report it")
        return Response(author.name + " I sent the link to my server in a DM")
    
    async def cmd_date(self):
        return Response(xl.format("Current Date: " + time.strftime("%A, %B %d, %Y") + "\n Current Time (Eastern): " + time.strftime("%I:%M:%S %p") + "Happy birthday to the ones today, you'd know who you are. <3"), delete_after=0)

    async def cmd_talk(client, message):
        cb1 = cleverbot.Cleverbot()
        unsplit = message.content.split("talk")
        split = unsplit[1]
        answer = (cb1.ask(split))
        await client.send_message(message.channel, message.author.name + ": " + answer)

    async def cmd_kill(self, client, message, author):
        """
        Usage: /kill (person)
            Pretty self explanitory.
        """
        if message.content[len(self.command_prefix + "kill"):].strip() != message.author.mention:
            await self.safe_send_message(message.channel, "You've killed " + message.content[len(self.command_prefix + "kill "):].strip() + " " + random.choice(suicidalmemes))
        elif message.content[len(self.command_prefix + "kill"):].strip() == "<@163698730866966528>":
            await self.safe_send_message(message.channel, "can u not im not gonna die")
        elif message.content[len(self.command_prefix + "kill"):].strip() == message.author.mention:
            await self.safe_send_message(message.channel, "<@" + message.author.id + ">" + " Nice one on your suicide. Just, it's so great.")

    async def cmd_say(self, client, message):
        """
        Usage: /say (message)
        """
        troyhasnodongs = message.content[len(self.command_prefix + "say "):].strip()
        return Response(troyhasnodongs.replace("@everyone", "everyone"), delete_after=0)

    async def cmd_ship(self, client, message, content):
        """
        Usage: /ship (person) x (person)
        """
        if message.content[len(self.command_prefix + "ship "):].strip() == "<@" + self.user.id + "> x <@" + self.user.id + ">":
            return Response("I hereby ship, myself.... forever.... alone........ ;-;", delete_after=0)
        elif message.content[len(self.command_prefix + "ship "):].strip() == message.author.id == message.author.id:
            return Response("hah, loner", delete_after=0)
        elif message.content[len(self.command_prefix + "ship "):].strip() != "<@" + self.user.id + "> x <@" + self.user.id + ">":
            return Response("I hereby ship " + message.content[len(self.command_prefix + "ship"):].strip() + "!", delete_after=0)

    async def cmd_createinv(self):
        return Response(str(discord.Invite.url), delete_after=0)

    async def cmd_info(self):
        return Response(xl.format("~~~~~~~~~Ruby~~~~~~~~\n Built by {}\n Bot Version: {}\n Build Date: {}\n Users: {}\n User Message Count: {}\n Servers: {}\n Channels: {}\n Private Channels: {}\n Discord Python Version: {}\n ~~~~~~~~~~~~~~~~~~~~~\n\n Need help? Use the \"{}help\" command or message CreeperSeth from the Discord server Rubys Fallout Shelter\n\n Do not have that? Then do \"{}serverinv\" to grab the invite.\n\nThis bot was originally RobTheBoat but forked and renamed to Ruby Rose with more commands and other stuff, thank Robin for some of the features in the bot!\n\nWant to find even more information? Then vist \"http://ruby.creeperseth.com\"\n").format(BUNAME, MVER, BUILD, len(set(self.get_all_members())), len(set(self.messages)), len(self.servers), len(set(self.get_all_channels())), len(set(self.private_channels)), discord.__version__, self.command_prefix, self.command_prefix), delete_after=0)
    
    async def cmd_debug(self, message):
        if (message.content.startswith(self.command_prefix + "debug ")):
            if message.author.id == owner_id or message.author.id == "117678528220233731":
                debug = message.content[len(self.command_prefix + "debug "):].strip()
                thing = None
                try:
                    thing = eval(debug)
                except Exception as e:
                    await self.send_message(message.channel, py.format(type(e).__name__ + ": " + str(e)))
                    return
                if asyncio.iscoroutine(thing):
                    thing = await thing
                    await self.send_message(message.channel, py.format(thing))
            else:
                await self.send_message(message.channel, no_perm)

    async def cmd_disconnect(self, server, message):
        await self.safe_send_message(message.channel, "Disconnected from the voice server.")
        await self.log(":mega: Disconnected from: `%s`" % server.name)
        await self.disconnect_voice_client(server)
        await self._manual_delete_check(message)

    @owner_only
    async def cmd_reboot(self, message):
        await self.safe_send_message(message.channel, "Bot is restarting, please wait...")
        await self.log(":warning: Bot is restarting")
        await self.disconnect_all_voice_clients()
        raise exceptions.RestartSignal

    @owner_only
    async def cmd_timetodie(self, message):
        await self.safe_send_message(message.channel, "Bot is shutting down...")
        await self.log(":warning: Bot is shutting down")
        await self.disconnect_all_voice_clients()
        raise exceptions.TerminateSignal

    @owner_only
    async def cmd_respond(self, author, dorespond):
        global respond
        if dorespond == "false":
            respond = False
            await self.change_presence(status=discord.Status.invisible)
            await self.disconnect_all_voice_clients()
            await self.log(":exclamation: `" + author.name + "` disabled command responses. `Not responding to commands.`")
            return Response("Not responding to commands", delete_after=15)
        elif dorespond == "true":
            respond = True
            await self.change_presence(game=default_game, status=default_status)
            await self.log(":exclamation: `" + author.name + "` enabled command responses. `Now responding to commands.`")
            return Response("Responding to commands", delete_after=15)
        else:
            return Response("Either \"true\" or \"false\"", delete_after=15)
        await self._manual_delete_check(message)

    async def cmd_rape(self, author):
        await self.log(":information_source: " + author.name + " just ran the command `/rape`, what the fuck...")
        return Response(author.mention + " what the actual fuck is wrong with you? Holy shit you need to be fucking taken to a concentration camp! Did you really think " + command_prefix + "rape was going to do something related to rape?")

    async def cmd_addrole(self, server, author, message, username, rolename):
        """
        Usage:
            {command_prefix}addrole @user rolename

        Adds a user to a role 
        """
        user_id = extract_user_id(username)
        user = discord.utils.find(lambda mem: mem.id == str(user_id), server.members)
        if not user:
            raise exceptions.CommandError("Invalid user specified")

        rname = message.content[len(self.command_prefix + "addrole " + username + " "):].strip()
        role = discord.utils.get(server.roles, name=rname)
        if not role:
            raise exceptions.CommandError("Invalid role specified")

        mod_role_name = read_data_entry(message.server.id, "mod-role")
        botcommander = discord.utils.get(author.roles, name=mod_role_name)
        if not botcommander:
            raise exceptions.CommandError("You must have the \"" + mod_role_name + "\" role in order to use that command.")
        try:
            await self.add_roles(user, role)
            await self.mod_log(server, "`" + self.format_user(author) + "` added the `" + role.name + "` role to `" + self.format_user(user) + "`")
            return Response("Successfully added the role `" + role.name + "` to " + self.format_user(user))
        except discord.errors.HTTPException: 
            raise exceptions.CommandError("I do not have the \"Manage Roles\" permission or the role you specified is higher than my highest role")

    async def cmd_removerole(self, server, author, message, username, rolename):
        """
        Usage:
            {command_prefix}removerole @user rolename

        Removes a user from a role 
        """
        user_id = extract_user_id(username)
        user = discord.utils.find(lambda mem: mem.id == str(user_id), server.members)
        if not user:
            raise exceptions.CommandError("Invalid user specified")

        rname = message.content[len(self.command_prefix + "removerole " + username + " "):].strip()
        role = discord.utils.get(server.roles, name=rname)
        if not role:
            raise exceptions.CommandError("Invalid role specified")

        mod_role_name = read_data_entry(message.server.id, "mod-role")
        botcommander = discord.utils.get(author.roles, name=mod_role_name)
        if not botcommander:
            raise exceptions.CommandError("You must have the \"" + mod_role_name + "\" role in order to use that command.")
        try:
            await self.remove_roles(user, role)
            await self.mod_log(server, "`" + self.format_user(author) + "` removed the `" + role.name + "` role from `" + self.format_user(user) + "`")
            return Response("Successfully removed the role `" + role.name + "` from " + self.format_user(user))
        except discord.errors.HTTPException: 
            raise exceptions.CommandError("I do not have the \"Manage Roles\" permission or the role you specified is higher than my highest role")

    @owner_only
    async def cmd_terminal(self, message):
        try:
            await self.send_typing(message.channel)
            msg = message.content[len(self.command_prefix + "terminal "):].strip()
            input = os.popen(msg)
            output = input.read()
            await self.send_message(message.channel, xl.format(output))
        except:
            return Response("Error, couldn't send command", delete_after=0)

    @owner_only
    async def cmd_uploadfile(self, message):
        await self.send_file(message.channel, message.content[len(self.command_prefix + "uploadfile "):].strip())
        if FileNotFoundError == True:
            await self.send_message(message.channel, "There was no such thing found in the system.")

    async def cmd_deval(self, message):
        if(message.content.startswith(self.command_prefix + "deval")):
            if message.author.id == owner_id or message.author.id == "117678528220233731":
                debug = message.content[len(self.command_prefix + "deval "):].strip()
                try:
                    debug = str(eval(debug))
                    await self.send_message(message.channel, py.format(debug))
                except Exception as e:
                    debug = traceback.format_exc()
                    debug = str(debug)
                    await self.send_message(message.channel, py.format(debug))
            else:
                await self.send_message(message.channel, no_perm)

    async def cmd_stats(client, message):
        await client.send_message(message.channel,
        "```xl\n ~~~~~~Ruby Stats~~~~~\n Built by {}\n Bot Version: {}\n Build Date: {}\n Users: {}\n User Message Count: {}\n Servers: {}\n Channels: {}\n Private Channels: {}\n Discord Python Version: {}\n Status: ok \n Date: {}\n Time: {}\n ~~~~~~~~~~~~~~~~~~~~~~~~~~\n```".format(
        BUNAME, MVER, BUILD, len(set(client.get_all_members())),
        len(set(client.messages)), len(client.servers),
        len(set(client.get_all_channels())), len(set(client.private_channels)),
        discord.__version__, time.strftime("%A, %B %d, %Y"),
        time.strftime("%I:%M:%S %p")))
        #Watch Nero spam this command until the bot crashes

    async def cmd_rubyrose(self):
        return Response("Here is a picture of Ruby Rose: " + random.choice(rubyshit))

    async def cmd_joinserver(self, author):
        await self.send_message(author, "Here is the link to add me to your server: https://discordapp.com/oauth2/authorize?&client_id=209469933346750464&scope=bot")
        return Response(author.name + " I sent the link to add me to your server in a DM")

    async def cmd_id(self, author, user_mentions):
        """
        Usage:
            {command_prefix}id [@user]
        Tells the user their id or the id of another user.
        """
        if not user_mentions:
            return Response("your Discord ID is: `%s`" % author.id, reply=True, delete_after=35)
        else:
            usr = user_mentions[0]
            return Response("%s's Discord ID is: `%s`" % (usr.name, usr.id), reply=True, delete_after=35)

    async def cmd_uptime(self):
        second = time.time() - st
        minute, second = divmod(second, 60)
        hour, minute = divmod(minute, 60)
        day, hour = divmod(hour, 24)
        week, day = divmod(day, 7)
        return Response(
            "I have been up for %d weeks," % (week) + " %d days," % (day) + " %d hours," % (hour) + " %d minutes," % (
            minute) + " and %d seconds." % (second), delete_after=0)

    async def cmd_userinfo(self, channel, username):
        """
        Usage:
            {command_prefix}userinfo @user
        """
        user_id = extract_user_id(username)
        user = discord.utils.find(lambda mem: mem.id == str(user_id), channel.server.members)
        if not user:
            raise exceptions.CommandError("Invalid user specified", expire_in=30)
        roles = ", ".join(map(str, user.roles))
        if roles == "@everyone":
            roles = None
        else:
            roles = roles[len("@everyone, "):].strip()
        await self.send_message(channel, xl.format("~~~~~~~~~{}~~~~~~~~\nUsername: {}\nDiscriminator: {}\nID: {}\nBot: {}\nAvatar URL: {}\nAccount created: {}\nGame: {}\nStatus: {}\nVoice channel: {}\nServer muted: {}\nServer deafened: {}\nRoles: {}").format(self.format_user(user), user.name, user.discriminator, user.id, user.bot, user.avatar_url, user.created_at, str(user.game), str(user.status), str(user.voice_channel), user.mute, user.deaf, roles))

    async def cmd_serverinfo(self, channel, server):
        owner = self.format_user(server.owner)
        afk_channel = None
        if not server.afk_channel:
            afk_channel = "None"
        else:
            afk_channel = server.afk_channel.name
        await self.send_message(channel, xl.format("~~~~~~~~~Server Info~~~~~~~~\nName: {}\nID: {}\nIcon URL: {}\nTotal Members: {}\nCreated: {}\nRegion: {}\nOwner: {}\nOwner ID: {}\nAFK Channel: {}\nAFK timeout: {}\nRoles: {}\nChannels: {}").format(server.name, server.id, server.icon_url, server.member_count, server.created_at, server.region, owner, server.owner_id, afk_channel, server.afk_timeout, len(server.roles), len(server.channels)))

    async def cmd_kick(self, message, username):
        """
        Usage: {command_prefix}kick @user
        Kicks the user prior to using the command.
        """
        user_id = extract_user_id(username)
        member = discord.utils.find(lambda mem: mem.id == str(user_id), message.channel.server.members)
        mod_role_name = read_data_entry(message.server.id, "mod-role")
        botcommander = discord.utils.get(message.author.roles, name=mod_role_name)
        if not botcommander:
            raise exceptions.CommandError("You must have the \""+ mod_role_name + "\" role in order to use that command.", expire_in=30)
        try:
            await self.kick(member)
            neroishot = self.format_user(message.author)
            name = self.format_user(member)
            await self.mod_log(message.server, "`" + neroishot +  "` kicked `" + name + "`")
            return Response(neroishot + " kicked " + name, delete_after=0)
        except discord.Forbidden:
            return Response("I do not have the proper permissions to kick that user.", reply=True)
        except discord.HTTPException:
            return Response("Kicking failed due to HTTPException error.", reply=True)

    async def cmd_rwby(self):
        return Response("You can watch RWBY here fam: http://roosterteeth.com/show/rwby")

    async def cmd_furry(self, server, message, username):
        """
        Usage: {command_prefix}furry @user
        Adds the specified user to the \"Furry\" role, if it does not exist it will create one
        """
        botcommander = discord.utils.get(message.author.roles, name="Bot Commander")
        if not botcommander:
            raise exceptions.CommandError("You must have the \"Bot Commander\" role in order to use that command.", expire_in=30)
        try:
            furryrole = discord.utils.find(lambda role: role.name == "Furry", server.roles)
            if furryrole == None:
                await self.create_role(message.channel.server, name="Furry", color=discord.Colour(16711680), mentionable=True, hoist=True)
                furryrole = discord.utils.find(lambda role: role.name == "Furry", server.roles)
            user_id = extract_user_id(username)
            member = discord.utils.find(lambda mem: mem.id == str(user_id), server.members)
            if not member:
                raise exceptions.CommandError("Invalid user specified", expire_in=30)
            await self.add_roles(member, furryrole)
            await self.send_message(message.channel, "FURRY ALERT! " + member.name.upper() + " IS A FURRY! HIDE THE FUCKING CHILDREN!!!!!111!11")
        except discord.Forbidden:
            raise exceptions.CommandError("I do not have the \"Manage Roles\" permission or \"Furry\" role is higher than my highest role", expire_in=30)

    async def cmd_allahuakbar(self, channel):
        await self.send_message(channel, "http://i.imgur.com/2mmCbQz.gif")

    async def cmd_onlytime(self, message, text):
        meme = message.content[len(self.command_prefix + "onlytime "):].strip()
        return Response(meme + ": https://www.youtube.com/watch?v=7wfYIMyS_dI")

    async def cmd_nicememe(self):
        return Response("http://niceme.me", delete_after=0)

    async def cmd_github(self):
        return Response("https://github.com/CreeperSeth/RubyRoseBot", delete_after=0)

    async def cmd_kys(self, message, name):
        WorthlessPieceOfShit = message.content[len(self.command_prefix + "kys "):].strip()
        return Response(WorthlessPieceOfShit + " you seriously need to go fucking kill yourself you worthless piece of shit!")

    async def cmd_thehood(self, channel):
        await self.send_typing(channel)
        await self.send_file(channel, "imgs/TheHood.gif")
        await self.send_message(channel, "I look good in a hood don't I?")

    async def cmd_saytts(self, channel, message, msg):
        bot = discord.utils.get(channel.server.members, name=self.user.name)
        perms = channel.permissions_for(message.author)
        bot_perms = channel.permissions_for(bot)
        msg = message.content[len(self.command_prefix + "saytts "):].strip()
        if perms.send_tts_messages is False:
            await self.send_message(channel, "You do not have permissions to send tts messages")
            return
        if bot_perms.send_tts_messages is False:
            await self.send_message(channel, "I do not have permissions to send tts messages")
            return
        await self.send_message(channel, msg, tts=True)
        await self._manual_delete_check(message)

    async def cmd_lenny(self):
        return Response("( ͡° ͜ʖ ͡°)")

    async def cmd_8ball(self, message):
        await self.send_message(message.channel, message.author.mention + " " + random.choice(magic_conch_shell))

    async def cmd_whydidievenmakethiscommand(self, channel):
        await self.send_message(channel, "\"In all honestly, why did I take 30 seconds out of my day to write this command?\" - CreeperSeth")

    async def cmd_makemeowner(self, channel, author, server):
        await self.send_message(channel, "Did you actually think that transfers ownership to you? HOW RETARDED ARE YOU!? This has been logged via the bot's logging channel and a PM was sent to the owner of this discord server.")
        await self.send_message(server.owner, "`" + self.format_user(author) + "` tried to make himself owner of your discord server using the command `" + self.command_prefix + "makemeowner` but failed.")
        await self.log(":information_source: `" + self.format_user(author) + "` literally tried to make himself owner of `" + server.name + "`! What a retard!")

    async def cmd_createchannel(self, server, author, message, name):
        botcommander = discord.utils.get(author.roles, name="Bot Commander")
        if not botcommander:
            raise exceptions.CommandError("You must have the \"Bot Commander\" role in order to use that command.", expire_in=30)
        tehname = message.content[len(self.command_prefix + "createchannel "):].strip().lower().replace(" ", "")
        try:
            noticemenero = await self.create_channel(server, tehname, type="text")
            noperm = discord.PermissionOverwrite(read_messages = False)
            neroisacat = discord.PermissionOverwrite(read_messages = True, manage_channels = True, manage_roles = True, manage_messages = True)
            await self.edit_channel_permissions(noticemenero, server.default_role, noperm)
            await self.edit_channel_permissions(noticemenero, message.author, neroisacat)
            await self.send_message(message.channel, "Sucessfully created the text channel " + noticemenero.mention + " You can fully manage this channel, currently only you can see it, you can change this in the channel permissions")
        except discord.HTTPException:
            await self.send_message(message.channel, "Could not create channel, check the name, names can not contain spaces and must be alphanumeric but dashes and underscores are allowed. **If you are sure the name is properly formatted, then I do not have permission to manage channels.**")

    async def cmd_createvoicechannel(self, server, author, message, name):
        botcommander = discord.utils.get(author.roles, name="Bot Commander")
        if not botcommander:
            raise exceptions.CommandError("You must have the \"Bot Commander\" role in order to use that command.", expire_in=30)
        tehname = message.content[len(self.command_prefix + "createvoicechannel "):].strip()
        try:
            noticemenero = await self.create_channel(server, tehname, type="voice")
            noperm = discord.PermissionOverwrite(connect = False)
            neroisacat = discord.PermissionOverwrite(connect = True, manage_channels = True, manage_roles = True, move_members = True, mute_members = True, deafen_members = True)
            await self.edit_channel_permissions(noticemenero, server.default_role, noperm)
            await self.edit_channel_permissions(noticemenero, message.author, neroisacat)
            await self.send_message(message.channel, "Sucessfully created the voice channel `" + noticemenero.name + "` You can fully manage this channel, currently only you can join it, you can change this in the channel permissions")
        except discord.HTTPException:
            await self.send_message(message.channel, "Could not create channel, I do not have permission to manage channels")

    async def cmd_mute(self, message, user):
        """
        Usage: {command_prefix}mute @user
        Adds the user to the \"Muted\" role
        """
        mod_role_name = read_data_entry(message.server.id, "mod-role")
        botcommander = discord.utils.get(message.author.roles, name=mod_role_name)
        if not botcommander:
            raise exceptions.CommandError("You must have the \"'+ mod_role_name + '\" role in order to use that command.", expire_in=30)
        user_id = extract_user_id(user)
        member = discord.utils.find(lambda mem: mem.id == str(user_id), message.channel.server.members)
        if not member:
            await self.send_message(message.channel, "User not found, make sure you are using a @mention")
            return
        mute_role = discord.utils.find(lambda role: role.name == "Muted", message.server.roles)
        if mute_role == None:
            await self.send_message(message.channel, "The `Muted` role was not found")
            return
        try:
            await self.add_roles(member, mute_role)
            await self.mod_log(message.server, "`" + self.format_user(message.author) + "` muted `" + self.format_user(member) + "`")
            await self.send_message(message.channel, "Sucessfully muted `" + self.format_user(member) + "`")
        except discord.errors.Forbidden:
            await self.send_message(message.channel, "I do not have permission to manage roles or the `Muted` role is higher than my highest role")

    async def cmd_unmute(self, message, user):
        """
        Usage: {command_prefix}unmute @user
        Removes the user from the \"Muted\" role
        """
        mod_role_name = read_data_entry(message.server.id, "mod-role")
        botcommander = discord.utils.get(message.author.roles, name=mod_role_name)
        if not botcommander:
            raise exceptions.CommandError("You must have the \"'+ mod_role_name + '\" role in order to use that command.", expire_in=30)
        user_id = extract_user_id(user)
        member = discord.utils.find(lambda mem: mem.id == str(user_id), message.channel.server.members)
        if not member:
            await self.send_message(message.channel, "User not found, make sure you are using a @mention")
            return
        mute_role = discord.utils.find(lambda role: role.name == "Muted", message.server.roles)
        if mute_role == None:
            await self.send_message(message.channel, "The `Muted` role was not found")
            return
        try:
            await self.remove_roles(member, mute_role)
            await self.mod_log(message.server, "`" + self.format_user(message.author) + "` unmuted `" + self.format_user(member) + "`")
            await self.send_message(message.channel, "Sucessfully unmuted `" + self.format_user(member) + "`")
        except discord.errors.Forbidden:
            await self.send_message(message.channel, "I do not have permission to manage roles or the `Muted` role is higher than my highest role")

    async def cmd_cykablyat(self, channel):
        await self.send_file(channel, "imgs/cykablyat.jpg")

    async def cmd_cykablyatsong(self):
        return Response("https://www.youtube.com/watch?v=bo5ZVe1LHxU")

    async def cmd_changelog(self):
        changes = "\n".join(map(str, change_log))
        return Response("Latest update changelog:\nCommand syntaxes can be found at http://ruby.creeperseth.com!\n```diff\n" + changes + "```")

    async def cmd_suggest(self, message, suggestion):
        await self.send_typing(message.channel)
        await self.send_message(message.channel, "Suggestion sent!")
        await self.send_message(discord.User(id="169597963507728384"), "New suggestion recieved from `" + message.author.name + "` Discrim: `" + message.author.discriminator + "` ID: `" + message.author.id + "` Server Name: `" + message.author.server.name + "` Suggestion: `" + message.content[len(self.command_prefix + "suggest "):].strip() + "`")
        await self.send_message(message.author, "You have sent a suggestion to <@169597963507728384>, the developer. Your suggstion that was sent was `" + message.content[len(self.command_prefix + "suggest "):].strip() + "`. You are not able to respond via the bot, <@169597963507728384> should send a message back to you shortly via PM.")
        
    async def cmd_wakemeup(self, channel):
        await self.send_message(channel, "Wake me up...")
        await asyncio.sleep(3)
        await self.send_message(channel, "Can't wake up...")

    async def cmd_fuckherrightinthepussy(self):
        return Response("https://www.youtube.com/watch?v=x7-nzLx4Oa0")

    async def cmd_memes(self):
        return Response(memes)

    async def cmd_showconfig(self, message):
        await self.send_typing(message.channel)
        mod_role_name = read_data_entry(message.server.id, "mod-role")
        nsfw_channel_name = read_data_entry(message.server.id, "nsfw-channel")
        return Response(xl.format("~~~~~~~~~~Server Config~~~~~~~~~~\nMod role name: {}\nNSFW channel name: {}").format(mod_role_name, nsfw_channel_name))

    async def cmd_config(self, message, type, value):
        """
        Usage: {command_prefix}config type value
        Configure the bot config for this server
        If you need help with this, visit the docs at ruby.creeperseth.com
        """
        if message.author is not message.server.owner:
            return Response("Only the server owner can use this command")
        await self.send_typing(message.channel)
        val = message.content[len(self.command_prefix + "config " + type + " "):].strip()
        if type == "mod-role" or type == "nsfw-channel":
            if type == "nsfw-channel":
                val = val.lower().replace(" ", "")
            update_data_entry(message.server.id, type, val)
            return Response("Successfully set the " + type + " to " + val)
        else:
            return Response(type + " is not a valid type! If you need help go to ruby.creeperseth.com")

    async def cmd_avatar(self, channel, user):
        user_id = extract_user_id(user)
        member = discord.utils.find(lambda mem: mem.id == str(user_id), channel.server.members)
        if not member:
            await self.send_message(channel, "User not found, make sure you are using a @mention")
            return
        if not member.avatar_url:
            await self.send_message(channel, member.mention + " doesn't have an avatar! Tell em to get one!")
            return
        await self.send_message(channel, member.mention + "'s current avatar is:\n" + member.avatar_url)

    async def cmd_prune(self, message, channel, amount):
        mod_role_name = read_data_entry(message.server.id, "mod-role")
        botcommander = discord.utils.get(message.author.roles, name=mod_role_name)
        if not botcommander:
            raise exceptions.CommandError("You must have the \"'+ mod_role_name + '\" role in order to use that command.", expire_in=30)
        try:
            harambe = int(amount)
        except:
            raise exceptions.CommandError("Error: " + amount + " is not a valid number!")
        try:
            deleted = await self.purge_from(channel, limit = harambe)
            return Response("Deleted {} messages".format(len(deleted)), delete_after=10, reply=True)
        except discord.Forbidden: 
            raise exceptions.CommandError("I need the \"Manage Messages\" permission in order to prune messages.")
        except discord.HTTPException:
            raise exceptions.CommandError("Unexpected error while attempting to prune messages.")

    async def cmd_unban(self, message, username):
        mod_role_name = read_data_entry(message.server.id, "mod-role")
        botcommander = discord.utils.get(message.author.roles, name=mod_role_name)
        if not botcommander:
            raise exceptions.CommandError("You must have the \"'+ mod_role_name + '\" role in order to use that command.", expire_in=30)
        bans = await self.get_bans(message.server)
        usr = message.content[len(self.command_prefix + "unban "):].strip()
        try:
            member = discord.utils.get(bans, name=usr)
            await self.unban(message.server, member)
            kek = self.format_user(message.author)
            name = self.format_user(member)
            await self.mod_log(message.server, "`" + kek + "` unbanned `" + name + "`")
            return Response(kek + " unbanned " + name, delete_after=0)
        except:
            await self.send_message(message.channel, "User is not banned fam")

    async def cmd_banlist(self, message):
        mod_role_name = read_data_entry(message.server.id, "mod-role")
        botcommander = discord.utils.get(message.author.roles, name=mod_role_name)
        if not botcommander:
            raise exceptions.CommandError("You must have the \""+ mod_role_name + "\" role in order to use that command.", expire_in=30)
        bans = await self.get_bans(message.server)
        banlist = ", ".join(map(str, bans))
        if banlist == "":
            banlist = "None"
        await self.send_message(message.channel, "Server ban list: ```" + banlist + "```")

    async def cmd_listservers(self, author):
        await self.send_message(author, "Servers that I am currently in\n```- " + "\n- ".join(map(str, self.servers)) + "```")

    async def cmd_getserverinfo(self, message, servername):
        sn = message.content[len(self.command_prefix + "getserverinfo "):].strip()
        serv = discord.utils.get(self.servers, name=sn)
        if serv is None:
            return Response("Couldn't find server named " + sn)
        return Response("```Name: {}\nID: {}\nOwner: {}\nMember count: {}```".format(serv.name, serv.id, self.format_user(serv.owner), len(serv.members)))

    async def cmd_setnick(self, message, nickname):
        nick = message.content[len(self.command_prefix + "setnick "):].strip()
        try:
            await self.change_nickname(message.server.me, nick)
            return Response("Changed my nickname to `" + nick + "`", delete_after=10)
        except discord.Forbidden:
            return Response("Could not change nickname because I don't have permission to", delete_after=10)
        except discord.HTTPException:
            return Response("Could not change nickname because of an unknown error", delete_after=10)

    async def cmd_removenick(self, server):
        try:
             await self.change_nickname(server.me, None)
             return Response("Removed my nickname", delete_after=10)
        except discord.Forbidden:
            return Response("Could not remove nickname because I don't have permission to", delete_after=10)
        except discord.HTTPException:
            return Response("Could not remove nickname because of an unknown error", delete_after=10)

    async def cmd_plzmsgme(self, message, text):
        msg = message.content[len(self.command_prefix + "plzmsgme "):].strip()
        await self.send_message(message.author, msg)
        await self.send_message(message.channel, "mkay fam")

    async def cmd_about(self):
        return Response("Here is some character information about me!\n```Name: Ruby Rose\nAge: 15\nRace: Human\nWeapon: Crescent Rose\nOutfit Colors: Red, Black\nAccessories: Rose Symbol, Ammunition Clips, Pouch, Cloak, Hood\nHandedness: Left\nComplexion: Pale White\nHeight: 5'2\" (1.57 meters)\nHair Color: Black and Red\nEye Color: Silver\nAura Color: Red\nSemblance: Speed\nOccupation: Student```")

    async def cmd_yiffinhell(self, channel):
        await self.send_file(channel, "imgs/yiffinhell.png")

    async def cmd_pressf(self, author):
        return Response(author.name + " has paid their respects! Respects paid: " + str(random.randint(1, 1000)))

    async def cmd_halloween(self, message):
        await self.send_message(message.channel, "Halloween is getting closer " + message.author.mention + "! :eyes: To see how many days until halloween run the command `" + self.command_prefix + "daystillhalloween`")
        await self.send_file(message.channel, "imgs/halloween.png")

    async def cmd_daystillhalloween(self):
        return Response("Days until halloween: `" + str((halloween - date.today()).days) + " days`")

    async def cmd_alex(self, channel):
        await self.send_message(channel, "https://www.youtube.com/watch?v=GX5xQPhC6UY")

    async def cmd_wtf(self, channel):
        await self.send_typing(channel)
        await self.send_file(channel, "imgs/quotes/" + str(random.randint(1, 18)) + ".png")

    async def cmd_changestatus(self, message, status):
        """
        Usage: {command_prefix}changestatus status name
        Change the bot's status
        status: Valid status types are: online, idle, do_not_disurb, and dnd
        The name is OPTIONAL
        """
        if lock_status is True:
            await self.send_message("The status is currently locked")
        statustype = None
        game = None
        if status == "invisible" or status == "offline":
            await self.send_message(message.channel, "You can not use the status type `" + status + "`")
            return
        try:
            statustype = discord.Status(status)
        except ValueError:
            await self.send_message(message.channel, "`" + status + "` is not a valid status type, valid status types are `online`, `idle`, `do_not_disurb`, and `dnd`")
            return
        name = message.content[len(self.command_prefix + "changestatus " + status + " "):].strip()
        if name != "":
            game = discord.Game(name=name)
        await self.change_presence(game=game, status=statustype)
        if game != None:
            await self.send_message(message.channel, "Changed game name to `" + game.name + "` with a(n) `" + str(status).replace("dnd", "do_not_disturb") + "` status type")
        else:
            await self.send_message(message.channel, "Changed status type to `" + str(status).replace("dnd", "do_not_disturb") + "`")

    async def cmd_stream(self, message, name):
        if lock_status is True:
            await self.send_message("The status is currently locked")
        name = message.content[len(self.command_prefix + "stream "):].strip()
        await self.change_presence(game=discord.Game(name=name, type=1, url="https://www.twitch.tv/creeperseth"))
        await self.send_message("Now streaming **" + name + "**")

    async def cmd_getemojis(self, message):
        emotes = []
        emojis = message.server.emojis
        if emojis == None:
            await self.send_message(message.channel, "The server does not have any emojis!")
        for emoji in emojis:
            emotes.append("`:" + emoji.name + ":` = " + str(emoji))
        await self.send_message(message.channel, "\n".join(map(str, emotes)))

    async def cmd_ping(self, channel):
        pingtime = time.time()
        pingms = await self.send_message(channel, "Pinging...")
        ping = time.time() - pingtime
        await self.edit_message(pingms, "The ping time is `%.01f secs`" % (ping))

    async def cmd_isitdown(self, channel, url):
        await self.send_typing(channel)
        try:
            starttime = time.time()
            r = requests.get(url, timeout=3)
            ping = time.time() - starttime
            await self.send_message(channel, "`" + url + "` is online. Ping time is `%.01f secs`" % (ping))
        except requests.exceptions.MissingSchema:
            await self.send_message(channel, "`" + url + "` is not a valid url. Make sure you are using `http://` or `https://`")
        except:
            await self.send_message(channel, "`" + url + "` is offline.")

    async def cmd_calc(self, message, problem):
        """
        Usage: {command_prefix}calc problem
        Solves a math problem so you don't have to!
        + = add, - = subtract, * = multiply, and / = divide
        """
        prob = re.sub("[^0-9+-/* ]", "", message.content[len(self.command_prefix + "calc "):].strip())
        try:
            answer = str(eval(prob))
            await self.send_message(message.channel, "`" + prob + "` = `" + answer + "`")
        except:
            await self.send_message(message.channel, "I couldn't solve that problem it's too hard")

    async def cmd_thisishalloween(self, channel):
        await self.send_message(channel, "https://www.youtube.com/watch?v=DOtEdhKOMgQ")

    async def cmd_randomasscat(self, channel):
        await self.send_typing(channel)
        cat.getCat(directory="imgs", filename="cat", format="gif")
        await self.send_file(channel, "imgs/cat.gif")
        # Watch Nero spam this command until the bot crashes

    async def on_message(self, message):
        if discord.utils.get(message.author.roles, name="Grimm"):
            return
        await self.wait_until_ready()

        if message.channel.is_private:
            await self.send_message(message.author, "I'm sorry, but I can't respond to private messages")
            return

        if respond is False:
            if message.author.id != owner_id:
                return

        message_content = message.content.strip()
        if not message_content.startswith(self.config.command_prefix):
            if not message_content.find("<@" + self.user.id + ">" or "<@!" + self.user.id + ">"):
                if message.author == self.user:
                    return
                await self.send_message(message.channel, message.author.mention + " " + random.choice(triggered))
            return

        if message.author == self.user:
            self.safe_print("Ignoring command from myself (%s)" % message.content)
            return

        if self.config.bound_channels and message.channel.id not in self.config.bound_channels and not message.channel.is_private:
            return

        command, *args = message_content.split()
        command = command[len(self.config.command_prefix):].lower().strip()

        handler = getattr(self, "cmd_%s" % command, None)
        if not handler:
            return

        if message.channel.is_private:
            await self.send_message(message.channel, "You cannot use this bot in private messages.")
            return

        if message.author.id in self.blacklist and message.author.id != self.config.owner_id:
            self.safe_print("[User blacklisted] {0.id}/{0.name} ({1})".format(message.author, message_content))
            if self.config.log_interaction:
                await self.log(":no_pedestrians: `{0.name}#{0.discriminator}`: `{1}`".format(message.author, message_content), message.channel)
            return

        elif self.config.white_list_check and int(
                message.author.id) not in self.whitelist and message.author.id != self.config.owner_id:
            self.safe_print("[User not whitelisted] {0.id}/{0.name} ({1})".format(message.author, message_content))
            if self.config.log_interaction:
                await self.log("Whitelisted: `{0.name}#{0.discriminator}`: `{1}`".format(message.author, message_content), message.channel)
            return

        else:
            self.safe_print("[Command] [{0.server.name}] {0.id}/{0.name}#{0.discriminator} ({1})".format(message.author, message_content))

        user_permissions = self.permissions.for_user(message.author)

        argspec = inspect.signature(handler)
        params = argspec.parameters.copy()

        # noinspection PyBroadException
        try:
            if user_permissions.ignore_non_voice and command in user_permissions.ignore_non_voice:
                await self._check_ignore_non_voice(message)

            handler_kwargs = {}
            if params.pop("message", None):
                handler_kwargs["message"] = message

            if params.pop("channel", None):
                handler_kwargs["channel"] = message.channel

            if params.pop("author", None):
                handler_kwargs["author"] = message.author

            if params.pop("server", None):
                handler_kwargs["server"] = message.server

            if params.pop("player", None):
                handler_kwargs["player"] = await self.get_player(message.channel)

            if params.pop("permissions", None):
                handler_kwargs["permissions"] = user_permissions

            if params.pop("user_mentions", None):
                handler_kwargs["user_mentions"] = list(map(message.server.get_member, message.raw_mentions))

            if params.pop("channel_mentions", None):
                handler_kwargs["channel_mentions"] = list(map(message.server.get_channel, message.raw_channel_mentions))

            if params.pop("voice_channel", None):
                handler_kwargs["voice_channel"] = message.server.me.voice_channel

            if params.pop("leftover_args", None):
                handler_kwargs["leftover_args"] = args

            args_expected = []
            for key, param in list(params.items()):
                doc_key = "[%s=%s]" % (key, param.default) if param.default is not inspect.Parameter.empty else key
                args_expected.append(doc_key)

                if not args and param.default is not inspect.Parameter.empty:
                    params.pop(key)
                    continue

                if args:
                    arg_value = args.pop(0)
                    handler_kwargs[key] = arg_value
                    params.pop(key)

            if message.author.id != self.config.owner_id:
                if user_permissions.command_whitelist and command not in user_permissions.command_whitelist:
                    raise exceptions.PermissionsError(
                        "Command isn't enabled for: (%s)." % user_permissions.name,
                        expire_in=20)

                elif user_permissions.command_blacklist and command in user_permissions.command_blacklist:
                    raise exceptions.PermissionsError(
                        "This command is disabled for: (%s)." % user_permissions.name,
                        expire_in=20)

            if params:
                docs = getattr(handler, "__doc__", None)
                if not docs:
                    docs = "Usage: {}{} {}".format(
                        self.command_prefix,
                        command,
                        " ".join(args_expected)
                    )

                docs = "\n".join(l.strip() for l in docs.split("\n"))
                await self.safe_send_message(
                    message.channel,
                    "```\n%s\n```" % docs.format(command_prefix=self.config.command_prefix),
                    expire_in=60
                )
                return

            response = await handler(**handler_kwargs)
            if response and isinstance(response, Response):
                content = response.content
                if response.reply:
                    content = "%s, %s" % (message.author.mention, content)

                sentmsg = await self.safe_send_message(
                    message.channel, content,
                    expire_in=response.delete_after if self.config.delete_messages else 0,
                    also_delete=message if self.config.delete_invoking else None
                )

        except (exceptions.CommandError, exceptions.HelpfulError, exceptions.ExtractionError) as e:
            print("{0.__class__}: {0.message}".format(e))
            await self.safe_send_message(message.channel, "```\n%s\n```" % e.message, expire_in=e.expire_in)

        except exceptions.Signal:
            raise

        except Exception:
            traceback.print_exc()
            if self.config.log_exceptions:
                await self.log(":warning: `%s` encountered an Exception:\n```python\n%s\n```" % (self.format_user(self.user), traceback.format_exc()), message.channel)

    async def on_server_join(self, server):
        if self.config.log_interaction:
            await self.log(":performing_arts: `%s` joined: `%s`" % (self.format_user(self.user), server.name))

    async def on_server_remove(self, server):
        if self.config.log_interaction:
            await self.log(":performing_arts: `%s` left: `%s`" % (self.format_user(self.user), server.name))         

    async def on_server_update(self, before:discord.Server, after:discord.Server):
        if before.name != after.name:
            await self.mod_log(after, "Server name was changed from `" + before.name + "` to `" + after.name + "`")

        if before.region != after.region:
            await self.mod_log(after, "Server region was changed from `" + str(before.region)+ "` to `" + str(after.region) + "`")

        if before.afk_channel != after.afk_channel:
            await self.mod_log(after, "Server afk channel was changed from `" + before.afk_channel.name + "` to `" + after.afk_channel.name + "`")

        if before.afk_timeout != after.afk_timeout:
            await self.mod_log(after, "Server afk timeout was changed from `" + str(before.afk_timeout) + "` seconds to `" + str(after.afk_timeout) + "` seconds")

        if before.icon != after.icon:
            await self.mod_log(after, "Server icon was changed from " + before.icon_url + " to " + after.icon_url)

        if before.owner != after.owner:
            await self.mod_log(after, "Server ownership was transfered from `" + self.format_user(before.owner) + "` to `" + self.format_user(after.owner) + "`")

    async def on_voice_state_update(self, before, after):
        if not all([before, after]):
            return

        if before.server.id not in self.players:
            return

        my_voice_channel = after.server.me.voice_channel  # This should always work, right?

        auto_paused = self.server_specific_data[after.server]["auto_paused"]
        player = await self.get_player(my_voice_channel)

        if after == after.server.me and after.voice_channel:
            player.voice_client.channel = after.voice_channel

        if not self.config.auto_pause:
            return


        num_deaf = sum(1 for m in my_voice_channel.voice_members if (
            m.deaf or m.self_deaf))

        if (len(my_voice_channel.voice_members) - 1) != num_deaf:
            if auto_paused and player.is_paused:
                print("[config:autopause] Unpausing")
                self.server_specific_data[after.server]["auto_paused"] = False
                player.resume()
        else:
            if not auto_paused and player.is_playing:
                print("[config:autopause] Pausing")
                self.server_specific_data[after.server]["auto_paused"] = True
                player.pause()

        if before.voice_channel == after.voice_channel:
            return
  
        if not my_voice_channel:
            return

        if not my_voice_channel:
            return

        if before.voice_channel == my_voice_channel:
            joining = False
        elif after.voice_channel == my_voice_channel:
            joining = True
        else:
            return

        moving = before == before.server.me

        if sum(1 for m in my_voice_channel.voice_members if m != after.server.me):
            if auto_paused and player.is_paused:
                print("[config:autopause] Unpausing")
                self.server_specific_data[after.server]["auto_paused"] = False
                player.resume()
        else:
            if not auto_paused and player.is_playing:
                print("[config:autopause] Pausing")
                self.server_specific_data[after.server]["auto_paused"] = True
                player.pause()


if __name__ == "__main__":
    bot = Ruby()
    bot.run()