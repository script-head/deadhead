import asyncio
import aiohttp
import time
import sys
import subprocess
import os
import json
import pyping

start_time = time.time()

# Initialize the logger first so the colors and shit are setup
from utils.logger import log
log.init()

from utils.bootstrap import Bootstrap
Bootstrap.run_checks()

from utils import checks
from utils import ranking

from discord.ext import commands
from utils.config import Config
from utils.tools import *
from utils.channel_logger import Channel_Logger
from utils.mysql import *
from utils.buildinfo import *

config = Config()
log.setupRotator(config.log_date_format, config.log_time_format)
if config.debug:
    log.enableDebugging() # pls no flame
bot = commands.Bot(command_prefix=config.command_prefix, description="A multi-purpose Ruby Rose from RWBY themed discord bot", pm_help=None)
channel_logger = Channel_Logger(bot)
aiosession = aiohttp.ClientSession(loop=bot.loop)
lock_status = config.lock_status

extensions = ["commands.fun", 
              "commands.information", 
              "commands.moderation", 
              "commands.configuration", 
              "commands.rwby", 
              "commands.nsfw", 
              "commands.music", 
              "commands.reactions", 
              "commands.economy", 
              "commands.ranking"]

# Thy changelog
change_log = [
    "Side note: Read r!econotice because I still need suggestions for the eco system.",
    "Commands:",
    "None",
    "Other things:",
    "Fixed the r!stats command from breaking whenever voice clients were active",
    "Fixed the r!notifydev and r!suggest commands",
    "Fixed the dev ids from returning as strings",
    "Fixed all the \"fun\" commands that were broken from the ctx.channel argument in the trigger_typing method",
    "Fixed the join and leave messages",
    "Fixed the join roles",
    "Fixed r!invite, r!joinserver, and r!dm"
]

async def _restart_bot():
    try:
      aiosession.close()
      await bot.cogs["Music"].disconnect_all_voice_clients()
    except:
       pass
    await bot.logout()
    subprocess.call([sys.executable, "bot.py"])

async def _shutdown_bot():
    try:
      aiosession.close()
      await bot.cogs["Music"].disconnect_all_voice_clients()
    except:
       pass
    await bot.logout()

async def set_default_status():
    if not config.enable_default_status:
        return
    type = config.default_status_type
    game = config.default_status_name
    try:
        type = discord.Status(type)
    except:
        type = discord.Status.online
    if game is not None:
        if config.default_status_type == "stream":
            if config.default_status_name is None:
                log.critical("If the status type is set to \"stream\" then the default status game must be specified")
                os._exit(1)
            game = discord.Game(name=game, url="http://twitch.tv/ZeroEpoch1969", type=1)
        else:
            game = discord.Game(name=game)
        await bot.change_presence(status=type, game=game)
    else:
        await bot.change_presence(status=type)

@bot.event
async def on_resumed():
    log.info("Reconnected to discord!")

@bot.event
async def on_ready():
    print("Connected!\n")
    print("Logged in as:\n{}/{}#{}\n----------".format(bot.user.id, bot.user.name, bot.user.discriminator))
    print("Bot version: {}\nAuthor(s): {}\nCode name: {}\nBuild date: {}".format(BUILD_VERSION, BUILD_AUTHORS, BUILD_CODENAME, BUILD_DATE))
    log.debug("Debugging enabled!")
    await set_default_status()
    for extension in extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            log.error("Failed to load extension {}\n{}: {}".format(extension, type(e).__name__, e))
    if os.path.isdir("data/music"):
        try:
            bot.cogs["Music"].clear_data()
            log.info("The music cache has been cleared!")
        except:
            log.warning("Failed to clear the music cache!")
    if config.enableMal:
        try:
            bot.load_extension("commands.myanimelist")
            log.info("The MyAnimeList module has been enabled!")
        except Exception as e:
            log.error("Failed to load the MyAnimeList module\n{}: {}".format(type(e).__name__, e))
    if config.enableOsu:
        log.info("The osu! module has been enabled in the config!")
    if config._dbots_token:
        log.info("Updating DBots Statistics...")
        r = requests.post("https://bots.discord.pw/api/bots/{}/stats".format(bot.user.id), json={
            "server_count":len(bot.guilds)}, headers={"Authorization":config._dbots_token})
        if r.status_code == "200":
            log.info("Discord Bots guild count updated.")
        elif r.status_code == "401":
            log.error("An error occurred while trying to update the guild count!")
    if config._carbonitex_key:
        log.info("Updating Carbonitex Statistics...")
        payload = {"key":config._carbonitex_key, "guildcount":len(bot.guilds), "botname":bot.user.name, "logoid":bot.user.avatar_url}
        owner = discord.utils.get(list(bot.get_all_members()), id=config.owner_id)
        if owner is not None:
            payload["ownername"] = owner.name
        r = requests.post("https://www.carbonitex.net/discord/data/botdata.php", json=payload)
        if r.text == "1 - Success":
            log.info("Carbonitex stats updated")
        else:
            log.error("Failed to update the carbonitex stats, double check the key in the config!")

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return
    if isinstance(error, commands.DisabledCommand):
        await ctx.send("This command has been disabled")
        return
    if isinstance(error, checks.dev_only):
        await ctx.send("This command can only be ran by the bot developers")
        return
    if isinstance(error, checks.owner_only):
        await ctx.send("This command can only be ran by the bot owner")
        return
    if isinstance(error, checks.not_nsfw_channel):
        await ctx.send("This command can only be ran in NSFW enabled channels.")
        return
    if isinstance(error, checks.not_guild_owner):
        await ctx.send(ctx.channel, "Only the server owner (`{}`) can use this command".format(ctx.guild.owner))
        return
    if isinstance(error, checks.no_permission):
        await ctx.send("You do not have permission to use this command".format(ctx.guild.owner))
        return
    if isinstance(error, commands.NoPrivateMessage):
        await ctx.send("This command can only be ran on servers".format(ctx.guild.owner))
        return
    if isinstance(ctx.channel, discord.DMChannel):
        await ctx.send("An error occured while trying to run this command, this is most likely because it was ran in a private message channel. Please try running this command on a guild.")
        return

    #In case the bot failed to send a message to the channel, the try except pass statement is to prevent another error
    try:
        await ctx.send("An error occured while processing this command: `{}`".format(error))
    except:
        pass
    log.error("An error occured while executing the {} command: {}".format(ctx.command.qualified_name, error))

@bot.before_invoke
async def on_command_preprocess(ctx):
    if isinstance(ctx.channel, discord.DMChannel):
        guild = "Private Message"
    else:
        guild = "{}/{}".format(ctx.guild.id, ctx.guild.name)
    log.info("[Command] [{}] [{}/{}]: {}".format(guild, ctx.author.id, ctx.author, ctx.message.content))

@bot.event
async def on_message(message):
    if message.author.bot:
        return
    if isinstance(message.author, discord.Member):
        if discord.utils.get(message.author.roles, name="Grimm"):
            return
    if getblacklistentry(message.author.id) is not None:
        return
    if isinstance(message.channel, discord.TextChannel):
        if read_data_entry(message.guild.id, "enable-ranking"):
            if ranking.level_up(message.author, message.guild):
                level = ranking.get_rank_data(message.author, message.guild)["level"]
                role_rank_ups = ranking.get_rankup_role_dict(message.guild)
                try:
                    role = discord.utils.get(message.guild.roles, id=role_rank_ups[level])
                    await bot.add_roles(message.author, role)
                except:
                    pass
                await message.channel.send("{} you've leveled up to level **{}**!".format(message.author.mention, level))
    await bot.process_commands(message)

@bot.event
async def on_member_join(member:discord.Member):
    join_message = read_data_entry(member.guild.id, "join-message")
    if join_message is not None:
        join_message = join_message.replace("%user%", member.mention).replace("%server%", member.guild.name)
    join_leave_channel_id = read_data_entry(member.guild.id, "join-leave-channel")
    if join_leave_channel_id is not None:
        join_leave_channel = discord.utils.get(member.guild.channels, id=join_leave_channel_id)
        if join_leave_channel is None:
            update_data_entry(member.guild.id, "join-leave-channel", None)
    else:
        join_leave_channel = None
    join_role_id = read_data_entry(member.guild.id, "join-role")
    if join_role_id is not None:
        join_role = discord.utils.get(member.guild.roles, id=join_role_id)
        if join_role is None:
            update_data_entry(member.guild.id, "join-role", None)
    else:
        join_role = None
    if join_leave_channel is not None and join_message is not None:
        try:
            await join_leave_channel.send(join_message)
        except:
            pass
    if join_role is not None:
        try:
            await member.add_roles(join_role)
        except:
            None

@bot.event
async def on_member_remove(member:discord.Member):
    leave_message = read_data_entry(member.guild.id, "leave-message")
    if leave_message is not None:
        leave_message = leave_message.replace("%user%", member.mention).replace("%guild%", member.guild.name)
    join_leave_channel_id = read_data_entry(member.guild.id, "join-leave-channel")
    if join_leave_channel_id is not None:
        join_leave_channel = discord.utils.get(member.guild.channels, id=join_leave_channel_id)
        if join_leave_channel is None:
            update_data_entry(member.guild.id, "join-leave-channel", None)
    else:
        join_leave_channel = None
    if join_leave_channel is not None and leave_message is not None:
        try:
            await join_leave_channel.send(leave_message)
        except:
            pass

@bot.command(hidden=True)
@checks.is_dev()
async def debug(ctx, *, shit:str):
    """This is the part where I make 20,000 typos before I get it right"""
    # "what the fuck is with your variable naming" - EJH2
    # seth seriously what the fuck - Robin
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

@bot.command(hidden=True)
@checks.is_owner()
async def rename(ctx, *, name:str):
    """Renames the bot"""
    await bot.edit_profile(username=name)
    await ctx.send("si")

@bot.command(hidden=True)
@checks.is_dev()
async def shutdown(ctx):
    """Shuts down the bot"""
    await ctx.send("Shutting down...")
    log.warning("{} has shut down the bot!".format(ctx.author))
    await _shutdown_bot()

@bot.command(hidden=True)
@checks.is_dev()
async def restart(ctx):
    """Restarts the bot"""
    await ctx.send("Restarting...")
    log.warning("{} has restarted the bot!".format(ctx.author))
    await _restart_bot()

@bot.command(hidden=True)
@checks.is_owner()
async def setavatar(ctx, *, url:str=None):
    """Changes the bot's avatar"""
    if ctx.message.attachments:
        url = ctx.message.attachments[0]["url"]
    elif url is None:
        await ctx.send("Please specify an avatar url if you did not attach a file")
        return
    try:
        with aiohttp.Timeout(10):
            async with aiosession.get(url.strip("<>")) as image:
                await bot.edit_profile(avatar=await image.read())
    except Exception as e:
        await ctx.send("Unable to change avatar: {}".format(e))
    await ctx.send(":eyes:")

@bot.command()
async def notifydev(ctx, *, message:str):
    """Sends a message to the developers"""
    if isinstance(ctx.channel, discord.DMChannel):
        guild = "`No server! Sent via Private Message!`"
    else:
        guild = "`{}` / `{}`".format(ctx.guild.id, ctx.guild.name)
    msg = make_message_embed(ctx.author, 0xFF0000, message, formatUser=True)
    owner = bot.get_user(config.owner_id)
    if owner:
        await owner.send("You have received a new message! The user's ID is `{}` Server: {}".format(ctx.author.id, guild), embed=msg)
    for id in config.dev_ids:
        dev = bot.get_user(id)
        if dev:
            await dev.send("You have received a new message! The user's ID is `{}` Server: {}".format(ctx.author.id, guild), embed=msg)
    await ctx.author.send("You have sent the developers a message! The message you sent was: `{}`".format(message))

@bot.command()
async def suggest(ctx, *, suggestion:str):
    """Sends a suggestion to the developers"""
    if isinstance(ctx.channel, discord.DMChannel):
        guild = "`No server! Sent via Private Message!`"
    else:
        guild = "`{}` / `{}`".format(ctx.guild.id, ctx.guild.name)
    msg = make_message_embed(ctx.author, 0xFF0000, suggestion, formatUser=True)
    owner = bot.get_user(config.owner_id)
    if owner:
        await owner.send("You have received a new suggestion! The user's ID is `{}` Server: {}".format(ctx.author.id, guild), embed=msg)
    for id in config.dev_ids:
        dev = bot.get_user(id)
        if dev:
            await dev.send("You have received a new suggestion! The user's ID is `{}` Server: {}".format(ctx.author.id, guild), embed=msg)
    await ctx.author.send("You have sent the developers a suggestion! The suggestion you sent was: `{}`".format(suggestion))

@bot.command(hidden=True)
@checks.is_dev()
async def blacklist(ctx, id:int, *, reason:str):
    """Blacklists a user"""
    await ctx.channel.trigger_typing()
    user = discord.utils.get(list(bot.get_all_members()), id=id)
    if user is None:
        await ctx.send("Could not find a user with an id of `{}`".format(id))
        return
    if getblacklistentry(id) != None:
        await ctx.send("`{}` is already blacklisted".format(user))
        return
    blacklistuser(id, user.name, user.discriminator, reason)
    await ctx.send("Blacklisted `{}` Reason: `{}`".format(user, reason))
    try:
        await user.send("You have been blacklisted from the bot by `{}` Reason: `{}`".format(ctx.author, reason))
    except:
        log.debug("Couldn't send a message to a user with an ID of \"{}\"".format(id))
    await channel_logger.log_to_channel(":warning: `{}` blacklisted `{}`/`{}` Reason: `{}`".format(ctx.author, id, user, reason))

@bot.command(hidden=True)
@checks.is_dev()
async def unblacklist(ctx, id:int):
    """Unblacklists a user"""
    entry = getblacklistentry(id)
    if entry is None:
        await ctx.send("No blacklisted user can be found with an id of `{}`".format(id))
        return
    try:
        unblacklistuser(id)
    except:
        await ctx.send("No blacklisted user can be found with an id of `{}`".format(id)) # Don't ask pls
        return
    await ctx.send("Successfully unblacklisted `{}#{}`".format(entry.get("name"), entry.get("discrim")))
    try:
        await discord.User(id=id).send("You have been unblacklisted from the bot by `{}`".format(ctx.author))
    except:
        log.debug("Couldn't send a message to a user with an ID of \"{}\"".format(id))
    await channel_logger.log_to_channel(":warning: `{}` unblacklisted `{}`/`{}#{}`".format(ctx.author, id, entry.get("name"), entry.get(
        "discrim")))

@bot.command()
async def showblacklist(ctx):
    """Shows the list of users that are blacklisted from the bot"""
    blacklist = getblacklist()
    count = len(blacklist)
    if blacklist == []:
        blacklist = "There are no blacklisted users"
    else:
        blacklist = "\n".join(blacklist)
    await ctx.send(xl.format("Total blacklisted users: {}\n\n{}".format(count, blacklist)))

@bot.command(hidden=True)
@checks.is_owner()
async def lockstatus(ctx):
    """Toggles the lock on the status"""
    global lock_status
    if lock_status:
        lock_status = False
        await ctx.send("The status has been unlocked")
    else:
        lock_status = True
        await ctx.send("The status has been locked")

@bot.command()
async def stream(ctx, *, name:str):
    """Sets the streaming status with the specified name"""
    if lock_status:
        if not ctx.author.id == config.owner_id and not ctx.author.id in config.dev_ids:
            await ctx.send("The status is currently locked")
            return
    await bot.change_presence(game=discord.Game(name=name, type=1, url="https://www.twitch.tv/creeperseth"))
    await ctx.send("Now streaming `{}`".format(name))
    await channel_logger.log_to_channel(":information_source: `{}`/`{}` has changed the streaming status to `{}`".format(
        ctx.author.id, ctx.author, name))

@bot.command()
async def changestatus(ctx, status:str, *, name:str=None):
    """Changes the bot's status with the specified status type and name"""
    if lock_status:
        if not ctx.author.id == config.owner_id and not ctx.author.id in config.dev_ids:
            await ctx.send("The status is currently locked")
            return
    game = None
    if status == "invisible" or status == "offline":
        await ctx.send("You can not use the status type `{}`".format(status))
        return
    try:
        statustype = discord.Status(status)
    except ValueError:
        await ctx.send("`{}` is not a valid status type, valid status types are `online`, `idle`, `do_not_disurb`, and `dnd`".format(
            status))
        return
    if name != "":
        game = discord.Game(name=name)
    await bot.change_presence(game=game, status=statustype)
    if name is not None:
        await ctx.send("Changed game name to `{}` with a(n) `{}` status type".format(name, status))
        await channel_logger.log_to_channel(":information_source: `{}`/`{}` has changed the game name to `{}` with a(n) `{}` status type".format(ctx.author.id, ctx.author, name, status))
    else:
        await ctx.send("Changed status type to `{}`".format(status))
        await channel_logger.log_to_channel(":information_source: `{}`/`{}` has changed the status type to `{}`".format(
            ctx.author.id, ctx.author, name))

@bot.command(hidden=True)
@checks.is_dev()
async def terminal(ctx, *, command:str):
    """Runs terminal commands and shows the output via a message. Oooh spoopy!"""
    try:
        await ctx.channel.trigger_typing()
        await ctx.send(xl.format(subprocess.Popen(command.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate(
        )[0].decode("ascii")))
    except:
        await ctx.send("Error, couldn't send command")

@bot.command(hidden=True)
@checks.is_dev()
async def uploadfile(ctx, *, path:str):
    """Uploads any file on the system. What is this hackery?"""
    await ctx.channel.trigger_typing()
    try:
        await bot.send_file(ctx.channel, path)
    except FileNotFoundError:
        await ctx.send("That file does not exist!")

@bot.command()
async def changelog(ctx):
    """The latest changelog"""
    await ctx.send("For command usages and a list of commands go to https://ruby.creeperseth.com or do `{0}help` (`{0}help command` for a command usage)\n{1}".format(bot.command_prefix, diff.format("\n".join(map(str, change_log)))))

@bot.command()
async def version(ctx):
    """Get the bot's current version"""
    await ctx.send("Bot version: {}\nAuthor(s): {}\nCode name: {}\nBuild date: {}".format(
        BUILD_VERSION, BUILD_AUTHORS, BUILD_CODENAME, BUILD_DATE))

@bot.command(hidden=True)
@checks.is_dev()
async def dm(ctx, id:int, *, message:str):
    """DMs a user"""
    msg = make_message_embed(ctx.author, 0xFF0000, message, formatUser=True)
    user = bot.get_user(id)
    if not user:
        await ctx.send("Could not find any user with an ID of `{}`".format(id))
    owner = bot.get_user(config.owner_id)
    if owner:
        await owner.send("`{}` has replied to a recent DM with `{}` (ID: `{}`)".format(ctx.author, user, id), embed=msg)
    for id in config.dev_ids:
        dev = bot.get_user(id)
        if dev:
            await dev.send("`{}` has replied to a recent DM with `{}` (ID: `{}`)".format(ctx.author, user, id), embed=msg)
    await user.send("You have received a message from one of the bot developers!", embed=msg)

@bot.command()
async def uptime(ctx):
    """Displays how long the bot has been online for"""
    second = time.time() - start_time
    minute, second = divmod(second, 60)
    hour, minute = divmod(minute, 60)
    day, hour = divmod(hour, 24)
    week, day = divmod(day, 7)
    await ctx.send("I've been online for %d weeks, %d days, %d hours, %d minutes, %d seconds" % (week, day, hour, minute, second))

@bot.command(hidden=True)
@checks.is_dev()
async def reload(ctx, *, extension:str):
    """Reloads an extension"""
    extension = "commands.{}".format(extension)
    if extension in extension:
        await ctx.send("Reloading {}...".format(extension))
        bot.unload_extension(extension)
        bot.load_extension(extension)
        await ctx.send("Successfully reloaded the {} extension!".format(extension))
    else:
        await ctx.send("Extension doesn't exist")

@bot.command()
async def joinserver(ctx):
    """Sends the bot's OAuth2 link"""
    await ctx.author.send("Here is the link to add me to your server: https://invite.ruby.creeperseth.com")

@bot.command()
async def invite(ctx):
    """Sends an invite link to the bot's server"""
    await ctx.author.send("Here is the link to my server: <https://discord.gg/RJTFyBd>\n\n(if the invite link is expired, report it using {}notifydev)".format(bot.command_prefix))

@bot.command()
async def ping(ctx):
    """Pings the bot"""
    #pingtime = time.monotonic()
    #pingms = await ctx.send("Pinging...")
    #ping = time.monotonic() - pingtime
    #await pingms.edit(content="The ping time is `{%.ms`" % ping)
    pingms = await ctx.send("Pinging...")
    # await bot.edit_message(pingms, topkek + " // ***{} ms***".format(str(ping)[3:][:3]))
    await pingms.edit(content="{} // **{} ms**".format(pingms.content, pyping.ping("creeperseth.com").avg_rtt))

@bot.command()
async def website(ctx):
    """Gives the link to the bot docs"""
    await ctx.send("My official website can be found here: https://ruby.creeperseth.com")

@bot.command()
async def github(ctx):
    """Gives the link to the github repo"""
    await ctx.send("My official github repo can be found here: https://github.com/ZeroEpoch1969/RubyRoseBot")

@bot.command()
async def stats(ctx):
    """Gets the bot's stats"""
    voice_clients = []
    for guild in bot.guilds:
        if guild.me.voice:
            voice_clients.append(guild.me.voice.channel)
    fields = {"Users":len(list(bot.get_all_members())), "Servers":len(bot.guilds), "Channels":len(list(
        bot.get_all_channels())), "Voice Clients":len(voice_clients), "Discord.py Version":discord.__version__, "Bot Version":
              BUILD_VERSION, "Built by":BUILD_AUTHORS}
    embed = make_list_embed(fields)
    embed.title = str(bot.user)
    embed.color = 0xFF0000
    embed.set_thumbnail(url=bot.user.avatar_url)
    bot_owner = discord.utils.get(list(bot.get_all_members()), id=config.owner_id)
    if bot_owner is not None:
        embed.set_footer(text=bot_owner, icon_url=get_avatar(bot_owner))
    await ctx.send(embed=embed)

@bot.command()
@checks.is_dev()
async def editmessage(ctx, id:int, *, newmsg:str):
    """Edits a message sent by the bot"""
    try:
        msg = await ctx.channel.get_message(id)
    except discord.errors.NotFound:
        await ctx.send("Couldn't find a message with an ID of `{}` in this channel".format(id))
        return
    if msg.author != ctx.guild.me:
        await ctx.send("That message was not sent by me")
        return
    await msg.edit(content=newmsg)
    await ctx.send("edit af")

@bot.command()
async def top10servers(ctx):
    """Gets the top 10 most populated servers the bot is on"""
    guilds = []
    for guild in sorted(bot.guilds, key=lambda e: e.member_count, reverse=True)[:10]:
        members = 0
        bots = 0
        total = len(guild.members)
        for member in guild.members:
            if member.bot:
                bots += 1
            else:
                members += 1
        guilds.append("{}: {} members, {} bots ({} total)".format(guild.name, members, bots, total))
    await ctx.send("```{}```".format("\n\n".join(guilds)))

@bot.command(hidden=True, enable=False)
async def vote(ctx, vote:str):
    """Vote command"""
    # Left this code here for future purposes so in the event I run another poll I don't need to recode a vote command
    with open("data/votes.json", "r") as jsonFile:
        votes = json.load(jsonFile)
    voted = False
    try:
        votes[ctx.author.id]
        voted = True
    except KeyError:
        pass
    if voted:
        await ctx.send("You already voted!")
        return
    vote = vote.lower()
    if vote == "yes" or vote == "no":
        votes[ctx.author.id] = vote
        await ctx.send("Successfully voted!")
    else:
        await ctx.send("Valid vote options are `yes` and `no`")
        return
    with open("data/ranksysvotes.json", "w") as jsonFile:
        json.dump(votes, jsonFile)

@bot.command(hidden=True, enable=False)
async def ranksysvoteresults(ctx):
    """Vote results command"""
    # Left this code here for future purposes so in the event I run another poll I don't need to recode a vote results command
    with open("data/votes.json", "r") as jsonFile:
        votes = json.load(jsonFile)
    yes = 0
    no = 0
    for vote in votes.values():
        if vote == "yes":
            yes += 1
        elif vote == "no":
            no += 1
    await ctx.send("Results for the rank system poll:\nYes: {}\nNo: {}".format(yes, no))

@bot.command()
async def test(ctx):
    await ctx.send("owo")


print("Connecting...")
bot.run(config._token)
