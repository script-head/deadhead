import asyncio
import aiohttp
import time
import sys
import subprocess
import os
import json

from datetime import datetime

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
log.setupRotator(config.log_dateformat, config.log_timeformat)
if config.debug:
    log.enableDebugging() # pls no flame
bot = commands.Bot(command_prefix=config.command_prefix, description="A multi-purpose Ruby Rose from RWBY themed discord bot", pm_help=True)
channel_logger = Channel_Logger(bot)
aiosession = aiohttp.ClientSession(loop=bot.loop)
lock_status = config.lock_status

extensions = ["commands.fun", "commands.information", "commands.moderation", "commands.configuration", "commands.rwby", "commands.nsfw", "commands.music", "commands.reactions", "commands.economy", "commands.ranking"]

# Thy changelog
change_log = [
    "Side note: Read r!econotice because I still need suggestions for the eco system.",
    "Commands:",
    "+ editmessage",
    "+ rank",
    "+ rankuproles",
    "+ addrankuprole",
    "+ removerankuprole",
    "+ topranked",
    "+ reverse",
    "+ react",
    "+ intellect",
    "Other things:",
    "Added the ranking system",
    "Reworked the terminal command so it performs better",
    "Added a missing invalid type message to the joinleave command",
    "Re-worked my check functions to be less confusing",
    "- Removed the mod-log channel feature as audit logs are a better alternative. If you wish for users to see audit logs just give them the `View Audit Log` permission.",
    "",
    "Added a ranking system, it is disabled by default and can be enabled with the config command. You can gain xp from sending messages after a 2 minute interval from recieving xp from a previous message. You can add and remove roles to be added after achieving a certain level with the addrankuprole and the removerankuprole commands."
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
            game = discord.Game(name=game, url="http://twitch.tv/CreeperSeth", type=1)
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
            bot.cogs["Music"].clear_cache()
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
        r = requests.post("https://bots.discord.pw/api/bots/{}/stats".format(bot.user.id), json={"server_count":len(bot.servers)}, headers={"Authorization":config._dbots_token})
        if r.status_code == "200":
            log.info("Discord Bots Server count updated.")
        elif r.status_code == "401":
            log.error("An error occurred while trying to update the server count!")
    if config._carbonitex_key:
        log.info("Updating Carbonitex Statistics...")
        payload = {"key":config._carbonitex_key, "servercount":len(bot.servers), "botname":bot.user.name, "logoid":bot.user.avatar_url}
        owner = discord.utils.get(list(bot.get_all_members()), id=config.owner_id)
        if owner is not None:
            payload["ownername"] = owner.name
        r = requests.post("https://www.carbonitex.net/discord/data/botdata.php", json=payload)
        if r.text == "1 - Success":
            log.info("Carbonitex stats updated")
        else:
            log.error("Failed to update the carbonitex stats, double check the key in the config!")

@bot.event
async def on_command_error(error, ctx):
    if isinstance(error, commands.CommandNotFound):
        return
    if isinstance(error, commands.DisabledCommand):
        await bot.send_message(ctx.message.channel, "This command has been disabled")
        return
    if isinstance(error, checks.dev_only):
        await bot.send_message(ctx.message.channel, "This command can only be ran by the bot developers")
        return
    if isinstance(error, checks.owner_only):
        await bot.send_message(ctx.message.channel, "This command can only be ran by the bot owner")
        return
    if isinstance(error, checks.not_nsfw_channel):
        await bot.send_message(ctx.message.channel, "This command can only be ran in NSFW enabled channels. It must either be named `nsfw` or the name must start with `nsfw-`")
        return
    if isinstance(error, checks.not_server_owner):
        await bot.send_message(ctx.message.channel, "Only the server owner (`{}`) can use this command".format(ctx.message.server.owner))
        return
    if isinstance(error, checks.no_permission):
        await bot.send_message(ctx.message.channel, "You do not have permission to use this command".format(ctx.message.server.owner))
        return
    if ctx.message.channel.is_private:
        await bot.send_message(ctx.message.channel, "An error occured while trying to run this command, this is most likely because it was ran in a private message channel. Please try running this command on a server.")
        return

    # In case the bot failed to send a message to the channel, the try except pass statement is to prevent another error
    try:
        await bot.send_message(ctx.message.channel, error)
    except:
        pass
    log.error("An error occured while executing the {} command: {}".format(ctx.command.qualified_name, error))

@bot.event
async def on_command(command, ctx):
    if ctx.message.channel.is_private:
        server = "Private Message"
    else:
        server = "{}/{}".format(ctx.message.server.id, ctx.message.server.name)
    log_line = "[Command] [{}] [{}/{}]: {}".format(server, ctx.message.author.id, ctx.message.author, ctx.message.content)
    print(log_line)
    log_file = open("logs/latest.log", "a+")
    log_file.write("{} {}\n".format(datetime.now().strftime("{} {}".format(config.log_dateformat, config.log_timeformat)), log_line))
    log_file.close()

@bot.event
async def on_message(message):
    if message.author.bot:
        return
    if isinstance(message.author, discord.Member):
        if discord.utils.get(message.author.roles, name="Grimm"):
            return
    if getblacklistentry(message.author.id) is not None:
        return
    if not message.channel.is_private:
        if read_data_entry(message.server.id, "enable-ranking"):
            if ranking.level_up(message.author, message.server):
                level = ranking.get_rank_data(message.author, message.server)["level"]
                role_rank_ups = ranking.get_rankup_role_dict(message.server)
                try:
                    role = discord.utils.get(message.server.roles, id=role_rank_ups[level])
                    await bot.add_roles(message.author, role)
                except:
                    pass
                await bot.send_message(message.channel, "{} you've leveled up to level **{}**!".format(message.author.mention, level))
    await bot.process_commands(message)

@bot.event
async def on_member_join(member:discord.Member):
    join_message = read_data_entry(member.server.id, "join-message")
    if join_message is not None:
        join_message = join_message.replace("!USER!", member.mention).replace("!SERVER!", member.server.name)
    join_leave_channel_id = read_data_entry(member.server.id, "join-leave-channel")
    if join_leave_channel_id is not None:
        join_leave_channel = discord.utils.get(member.server.channels, id=join_leave_channel_id)
        if join_leave_channel is None:
            update_data_entry(member.server.id, "join-leave-channel", None)
    else:
        join_leave_channel = None
    join_role_id = read_data_entry(member.server.id, "join-role")
    if join_role_id is not None:
        join_role = discord.utils.get(member.server.roles, id=join_role_id)
        if join_role is None:
            update_data_entry(member.server.id, "join-role", None)
    else:
        join_role = None
    if join_leave_channel is not None and join_message is not None:
        try:
            await bot.send_message(join_leave_channel, join_message)
        except:
            pass
    if join_role is not None:
        try:
            await bot.add_roles(member, join_role)
        except:
            None

@bot.event
async def on_member_remove(member:discord.Member):
    leave_message = read_data_entry(member.server.id, "leave-message")
    if leave_message is not None:
        leave_message = leave_message.replace("!USER!", member.mention).replace("!SERVER!", member.server.name)
    join_leave_channel_id = read_data_entry(member.server.id, "join-leave-channel")
    if join_leave_channel_id is not None:
        join_leave_channel = discord.utils.get(member.server.channels, id=join_leave_channel_id)
        if join_leave_channel is None:
            update_data_entry(member.server.id, "join-leave-channel", None)
    else:
        join_leave_channel = None
    if join_leave_channel is not None and leave_message is not None:
        try:
            await bot.send_message(join_leave_channel, leave_message)
        except:
            pass

@bot.command(hidden=True, pass_context=True)
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
        await bot.say(py.format(rebug))
    except Exception as damnit:
        await bot.say(py.format("{}: {}".format(type(damnit).__name__, damnit)))

@bot.command(hidden=True)
@checks.is_owner()
async def rename(*, name:str):
    """Renames the bot"""
    await bot.edit_profile(username=name)
    await bot.say("si")

@bot.command(hidden=True, pass_context=True)
@checks.is_dev()
async def shutdown(ctx):
    """Shuts down the bot"""
    await bot.say("Shutting down...")
    log.warning("{} has shut down the bot!".format(ctx.message.author))
    await _shutdown_bot()

@bot.command(hidden=True, pass_context=True)
@checks.is_dev()
async def restart(ctx):
    """Restarts the bot"""
    await bot.say("Restarting...")
    log.warning("{} has restarted the bot!".format(ctx.message.author))
    await _restart_bot()

@bot.command(hidden=True, pass_context=True)
@checks.is_owner()
async def setavatar(ctx, *, url:str=None):
    """Changes the bot's avatar"""
    if ctx.message.attachments:
        url = ctx.message.attachments[0]["url"]
    elif url is None:
        await bot.say("Please specify an avatar url if you did not attach a file")
        return
    try:
        with aiohttp.Timeout(10):
            async with aiosession.get(url.strip("<>")) as image:
                await bot.edit_profile(avatar=await image.read())
    except Exception as e:
        await bot.say("Unable to change avatar: {}".format(e))
    await bot.say(":eyes:")

@bot.command(pass_context=True)
async def notifydev(ctx, *, message:str):
    """Sends a message to the developers"""
    if ctx.message.channel.is_private:
        server = "`No server! Sent via Private Message!`"
    else:
        server = "`{}` / `{}`".format(ctx.message.server.id, ctx.message.server.name)
    msg = make_message_embed(ctx.message.author, 0xFF0000, message, formatUser=True)
    await bot.send_message(discord.User(id=config.owner_id), "You have received a new message! The user's ID is `{}` Server: {}".format(ctx.message.author.id, server), embed=msg)
    for id in config.dev_ids:
        await bot.send_message(discord.User(id=id), "You have received a new message! The user's ID is `{}` Server: {}".format(ctx.message.author.id, server), embed=msg)
    await bot.send_message(ctx.message.author, "You have sent the developers a message! The message you sent was: `{}`".format(message))
    await bot.say("Message sent!")

@bot.command(pass_context=True)
async def suggest(ctx, *, suggestion:str):
    """Sends a suggestion to the developers"""
    if ctx.message.channel.is_private:
        server = "`No server! Sent via Private Message!`"
    else:
        server = "`{}` / `{}`".format(ctx.message.server.id, ctx.message.server.name)
    msg = make_message_embed(ctx.message.author, 0xFF0000, suggestion, formatUser=True)
    await bot.send_message(discord.User(id=config.owner_id), "You have received a new suggestion! The user's ID is `{}` Server: {}".format(ctx.message.author.id, server), embed=msg)
    for id in config.dev_ids:
        await bot.send_message(discord.User(id=id), "You have received a new suggestion! The user's ID is `{}` Server: {}".format(ctx.message.author.id, server), embed=msg)
    await bot.send_message(ctx.message.author, "You have sent the developers a suggestion! The suggestion you sent was: `{}`".format(suggestion))
    await bot.say("Suggestion sent!")

@bot.command(hidden=True, pass_context=True)
@checks.is_dev()
async def blacklist(ctx, id:str, *, reason:str):
    """Blacklists a user"""
    await bot.send_typing(ctx.message.channel)
    user = discord.utils.get(list(bot.get_all_members()), id=id)
    if user is None:
        await bot.say("Could not find a user with an id of `{}`".format(id))
        return
    if getblacklistentry(id) != None:
        await bot.say("`{}` is already blacklisted".format(user))
        return
    blacklistuser(id, user.name, user.discriminator, reason)
    await bot.say("Blacklisted `{}` Reason: `{}`".format(user, reason))
    try:
        await bot.send_message(user, "You have been blacklisted from the bot by `{}` Reason: `{}`".format(ctx.message.author, reason))
    except:
        log.debug("Couldn't send a message to a user with an ID of \"{}\"".format(id))
    await channel_logger.log_to_channel(":warning: `{}` blacklisted `{}`/`{}` Reason: `{}`".format(ctx.message.author, id, user, reason))

@bot.command(hidden=True, pass_context=True)
@checks.is_dev()
async def unblacklist(ctx, id:str):
    """Unblacklists a user"""
    entry = getblacklistentry(id)
    if entry is None:
        await bot.say("No blacklisted user can be found with an id of `{}`".format(id))
        return
    try:
        unblacklistuser(id)
    except:
        await bot.say("No blacklisted user can be found with an id of `{}`".format(id)) # Don't ask pls
        return
    await bot.say("Successfully unblacklisted `{}#{}`".format(entry.get("name"), entry.get("discrim")))
    try:
        await bot.send_message(discord.User(id=id), "You have been unblacklisted from the bot by `{}`".format(ctx.message.author))
    except:
        log.debug("Couldn't send a message to a user with an ID of \"{}\"".format(id))
    await channel_logger.log_to_channel(":warning: `{}` unblacklisted `{}`/`{}#{}`".format(ctx.message.author, id, entry.get("name"), entry.get("discrim")))

@bot.command()
async def showblacklist():
    """Shows the list of users that are blacklisted from the bot"""
    blacklist = getblacklist()
    count = len(blacklist)
    if blacklist == []:
        blacklist = "There are no blacklisted users"
    else:
        blacklist = "\n".join(blacklist)
    await bot.say(xl.format("Total blacklisted users: {}\n\n{}".format(count, blacklist)))

@bot.command(hidden=True)
@checks.is_owner()
async def lockstatus():
    """Toggles the lock on the status"""
    global lock_status
    if lock_status:
        lock_status = False
        await bot.say("The status has been unlocked")
    else:
        lock_status = True
        await bot.say("The status has been locked")

@bot.command(pass_context=True)
async def stream(ctx, *, name:str):
    """Sets the streaming status with the specified name"""
    if lock_status:
        if not ctx.message.author.id == config.owner_id and not ctx.message.author.id in config.dev_ids:
            await bot.say("The status is currently locked")
            return
    await bot.change_presence(game=discord.Game(name=name, type=1, url="https://www.twitch.tv/creeperseth"))
    await bot.say("Now streaming `{}`".format(name))
    await channel_logger.log_to_channel(":information_source: `{}`/`{}` has changed the streaming status to `{}`".format(ctx.message.author.id, ctx.message.author, name))

@bot.command(pass_context=True)
async def changestatus(ctx, status:str, *, name:str=None):
    """Changes the bot's status with the specified status type and name"""
    if lock_status:
        if not ctx.message.author.id == config.owner_id and not ctx.message.author.id in config.dev_ids:
            await bot.say("The status is currently locked")
            return
    game = None
    if status == "invisible" or status == "offline":
        await bot.say("You can not use the status type `{}`".format(status))
        return
    try:
        statustype = discord.Status(status)
    except ValueError:
        await bot.say("`{}` is not a valid status type, valid status types are `online`, `idle`, `do_not_disurb`, and `dnd`".format(status))
        return
    if name != "":
        game = discord.Game(name=name)
    await bot.change_presence(game=game, status=statustype)
    if name is not None:
        await bot.say("Changed game name to `{}` with a(n) `{}` status type".format(name, status))
        await channel_logger.log_to_channel(":information_source: `{}`/`{}` has changed the game name to `{}` with a(n) `{}` status type".format(ctx.message.author.id, ctx.message.author, name, status))
    else:
        await bot.say("Changed status type to `{}`".format(status))
        await channel_logger.log_to_channel(":information_source: `{}`/`{}` has changed the status type to `{}`".format(ctx.message.author.id, ctx.message.author, name))

@bot.command(hidden=True, pass_context=True)
@checks.is_dev()
async def terminal(ctx, *, command:str):
    """Runs terminal commands and shows the output via a message. Oooh spoopy!"""
    try:
        await bot.send_typing(ctx.message.channel)
        await bot.say(xl.format(subprocess.Popen(command.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0].decode("ascii")))
    except:
        await bot.say("Error, couldn't send command")

@bot.command(hidden=True, pass_context=True)
@checks.is_dev()
async def uploadfile(ctx, *, path:str):
    """Uploads any file on the system. What is this hackery?"""
    await bot.send_typing(ctx.message.channel)
    try:
        await bot.send_file(ctx.message.channel, path)
    except FileNotFoundError:
        await bot.say("That file does not exist!")

@bot.command()
async def changelog():
    """The latest changelog"""
    await bot.say("For command usages and a list of commands go to https://ruby.creeperseth.com or do `{0}help` (`{0}help command` for a command usage)\n{1}".format(bot.command_prefix, diff.format("\n".join(map(str, change_log)))))

@bot.command()
async def version():
    """Get the bot's current version"""
    await bot.say("Bot version: {}\nAuthor(s): {}\nCode name: {}\nBuild date: {}".format(BUILD_VERSION, BUILD_AUTHORS, BUILD_CODENAME, BUILD_DATE))

@bot.command(hidden=True, pass_context=True)
@checks.is_dev()
async def dm(ctx, id:str, *, message:str):
    """DMs a user"""
    msg = make_message_embed(ctx.message.author, 0xFF0000, message, formatUser=True)
    try:
        sent_message = await bot.send_message(discord.User(id=id), "You have received a message from one of the bot developers!", embed=msg)
        user = sent_message.channel.user
    except:
        await bot.say("Could not send a message to the user.")
        return
    await bot.send_message(discord.User(id=config.owner_id), "`{}` has replied to a recent DM with `{}` (ID: `{}`)".format(ctx.message.author, user, id), embed=make_message_embed(ctx.message.author, 0xFF0000, message))
    for dev_id in config.dev_ids:
        await bot.send_message(discord.User(id=dev_id), "`{}` has replied to a recent DM with `{}` (ID: `{}`)".format(ctx.message.author, user, id), embed=make_message_embed(ctx.message.author, 0xFF0000, message))

@bot.command()
async def uptime():
    """Displays how long the bot has been online for"""
    second = time.time() - start_time
    minute, second = divmod(second, 60)
    hour, minute = divmod(minute, 60)
    day, hour = divmod(hour, 24)
    week, day = divmod(day, 7)
    await bot.say("I've been online for %d weeks, %d days, %d hours, %d minutes, %d seconds" % (week, day, hour, minute, second))

@bot.command(hidden=True)
@checks.is_dev()
async def reload(*, extension:str):
    """Reloads an extension"""
    extension = "commands.{}".format(extension)
    if extension in extension:
        await bot.say("Reloading {}...".format(extension))
        bot.unload_extension(extension)
        bot.load_extension(extension)
        await bot.say("Successfully reloaded the {} extension!".format(extension))
    else:
        await bot.say("Extension doesn't exist")

@bot.command(pass_context=True)
async def joinserver(ctx):
    """Sends the bot's OAuth2 link"""
    await bot.send_message(ctx.message.author, "Here is the link to add me to your server: http://invite.ruby.creeperseth.com")

@bot.command(pass_context=True)
async def invite(ctx):
    """Sends an invite link to the bot's server"""
    await bot.send_message(ctx.message.author, "Here is the link to my server: discord.gg/m5BEde5\n\n(if the invite link is expired, report it using {}notifydev)".format(bot.command_prefix))

@bot.command()
async def ping():
    """Pings the bot"""
    pingtime = time.time()
    pingms = await bot.say("Pinging...")
    ping = time.time() - pingtime
    await bot.edit_message(pingms, "The ping time is `%.01f seconds`" % ping)

@bot.command()
async def website():
    """Gives the link to the bot docs"""
    await bot.say("My official website can be found here: https://ruby.creeperseth.com")

@bot.command()
async def github():
    """Gives the link to the github repo"""
    await bot.say("My official github repo can be found here: https://github.com/CreeperSeth/RubyRoseBot")

@bot.command()
async def stats():
    """Gets the bot's stats"""
    voice_clients = []
    for server in bot.servers:
        if server.me.voice_channel:
            voice_clients.append(server.me.voice_channel)
    fields = {"Users":len(list(bot.get_all_members())), "Servers":len(bot.servers), "Channels":len(list(bot.get_all_channels())), "Private Channels":len((bot.private_channels)), "Voice Clients":len(voice_clients), "Discord.py Version":discord.__version__, "Bot Version":BUILD_VERSION, "Built by":BUILD_AUTHORS}
    embed = make_list_embed(fields)
    embed.title = str(bot.user)
    embed.color = 0xFF0000
    embed.set_thumbnail(url=bot.user.avatar_url)
    bot_owner = discord.utils.get(list(bot.get_all_members()), id=config.owner_id)
    if bot_owner is not None:
        embed.set_footer(text=bot_owner, icon_url=get_avatar(bot_owner))
    await bot.say(embed=embed)

@bot.command(pass_context=True)
@checks.is_dev()
async def editmessage(ctx, id:str, *, newmsg:str):
    """Edits a message sent by the bot"""
    try:
        msg = await bot.get_message(ctx.message.channel, id)
    except discord.errors.NotFound:
        await bot.say("Couldn't find a message with an ID of `{}` in this channel".format(id))
        return
    if msg.author != ctx.message.server.me:
        await bot.say("That message was not sent by me")
        return
    await bot.edit_message(msg, newmsg)
    await bot.say("edit af")

@bot.command()
async def top10servers():
    """Gets the top 10 most populated servers the bot is on"""
    servers = []
    for server in sorted(bot.servers, key=lambda e: e.member_count, reverse=True)[:10]:
        members = 0
        bots = 0
        total = len(server.members)
        for member in server.members:
            if member.bot:
                bots += 1
            else:
                members += 1
        servers.append("{}: {} members, {} bots ({} total)".format(server.name, members, bots, total))
    await bot.say("```{}```".format("\n\n".join(servers)))

@bot.command(pass_context=True, hidden=True, enable=False)
async def vote(ctx, vote:str):
    """Vote command"""
    # Left this code here for future purposes so in the event I run another poll I don't need to recode a vote command
    with open("data/votes.json", "r") as jsonFile:
        votes = json.load(jsonFile)
    voted = False
    try:
        votes[ctx.message.author.id]
        voted = True
    except KeyError:
        pass
    if voted:
        await bot.say("You already voted!")
        return
    vote = vote.lower()
    if vote == "yes" or vote == "no":
        votes[ctx.message.author.id] = vote
        await bot.say("Successfully voted!")
    else:
        await bot.say("Valid vote options are `yes` and `no`")
        return
    with open("data/ranksysvotes.json", "w") as jsonFile:
        json.dump(votes, jsonFile)

@bot.command(hidden=True, enable=False)
async def ranksysvoteresults():
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
    await bot.say("Results for the rank system poll:\nYes: {}\nNo: {}".format(yes, no))


print("Connecting...")
bot.run(config._token)
