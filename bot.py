import asyncio
import os
import aiohttp
import time

start_time = time.time()

# Initialize the logger first so the colors and shit are setup
from utils.logger import log
log.init() # Yes I could just use __init__ but I'm dumb

from utils.bootstrap import Bootstrap
Bootstrap.run_checks()

from utils import checks

from discord.ext import commands
from utils.config import Config
from utils.tools import *
from utils.channel_logger import Channel_Logger
from utils.mysql import *
from utils.buildinfo import *
from utils.opus_loader import load_opus_lib

config = Config()
if config.debug:
    log.enableDebugging() # pls no flame
loop = asyncio.get_event_loop()
bot = commands.Bot(command_prefix=config.command_prefix, description="A multi-purpose Ruby Rose from RWBY themed discord bot", pm_help=True, loop=loop)
channel_logger = Channel_Logger(bot)
aiosession = aiohttp.ClientSession(loop=loop)
lock_status = config.lock_status

extensions = ["commands.fun", "commands.information", "commands.moderation", "commands.configuration", "commands.rwby", "commands.nsfw", "commands.music"]

# Thy changelog
change_log = [
    "Commands:",
    "None!",
    "Other things:",
    "Fixed the skip command",
    "Fixed the invite command",
    "Fixed the bug where the volume resets when the song changes",
    "Fixed the NSFW commands returning a \"JSONDecodeError\""
]

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
    log.info("\nReconnected to discord!")

@bot.event
async def on_ready():
    print("Logged in as:\n{}/{}#{}\n----------".format(bot.user.id, bot.user.name, bot.user.discriminator))
    print("Bot version: {}\nAuthor(s): {}\nCode name: {}\nBuild date: {}".format(BUILD_VERSION, BUILD_AUTHORS, BUILD_CODENAME, BUILD_DATE))
    log.debug("Debugging enabled!")
    await set_default_status()
    for extension in extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            log.error("Failed to load extension {}\n{}: {}".format(extension, type(e).__name__, e))
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
    load_opus_lib()

@bot.event
async def on_command_error(error, ctx):
    if isinstance(error, commands.CommandNotFound):
        return
    if ctx.message.channel.is_private:
        await bot.send_message(ctx.message.channel, "An error occured while trying to run this command, this is most likely because it was ran in this private message channel. Please try running this command on a server.")
        return

    # In case the bot failed to send a message to the channel, the try except pass statement is to prevent another error
    try:
        await bot.send_message(ctx.message.channel, error)
    except:
        pass
    log.error("An error occured while executing the command named {}: {}".format(ctx.command.qualified_name, error))

@bot.event
async def on_command(command, ctx):
    if ctx.message.channel.is_private:
        server = "Private Message"
    else:
        server = "{}/{}".format(ctx.message.server.id, ctx.message.server.name)
    print("[Command] [{}] [{}/{}]: {}".format(server, ctx.message.author.id, format_user(ctx.message.author), ctx.message.content))

@bot.event
async def on_message(message):
    if discord.Member is type(message.author):
        if discord.utils.get(message.author.roles, name="Grimm"):
            return

    if getblacklistentry(message.author.id) is not None:
        return

    await bot.process_commands(message)

@bot.event
async def on_server_update(before:discord.Server, after:discord.Server):
    if before.name != after.name:
        await channel_logger.mod_log(after, "Server name was changed from `{}` to `{}`".format(before.name, after.name))
    if before.region != after.region:
        await channel_logger.mod_log(after, "Server region was changed from `{}` to `{}`".format(before.region, after.region))
    if before.afk_channel != after.afk_channel:
        await channel_logger.Channel_logg.mod_log(after, "Server afk channel was changed from `{}` to `{}`".format(before.afk_channel.name, after.afk_channel.name))
    if before.afk_timeout != after.afk_timeout:
        await channel_logger.mod_log(after, "Server afk timeout was changed from `{}` seconds to `{}` seconds".format(before.afk_timeout, after.afk_timeout))
    if before.icon != after.icon:
        await channel_logger.mod_log(after, "Server icon was changed from {} to {}".format(before.icon_url, after.icon_url))
    if before.mfa_level != after.mfa_level:
        if after.mfa_level == 0:
            mfa = "enabled"
        else:
            mfa = "disabled"
        await channel_logger.mod_log(after, "Server two-factor authentication requirement has been `{}`".format(mfa))
    if before.verification_level != after.verification_level:
        await channel_logger.mod_log(after, "Server verification level was changed from `{}` to `{}`".format(before.verification_level, after.verification_level))
    if before.owner != after.owner:
        await channel_logger.mod_log(after, "Server ownership was transferred from `{}` to `{}`".format(format_user(before.owner), format_user(after.owner)))

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

@bot.command(hidden=True, pass_context=True)
@checks.is_dev()
async def shutdown(ctx):
    """Logs out and shuts down the bot"""
    await bot.say("Shutting down...")
    log.warning("{} has shut down the bot!".format(format_user(ctx.message.author)))
    await bot.cogs["Music"].disconnect_all_voice_clients()
    await bot.logout()

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
            async with aiosession.get(url) as image:
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
    msg = make_message_embed(ctx.message.author, 0xCC0000, message, formatUser=True)
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
    msg = make_message_embed(ctx.message.author, 0xCC0000, suggestion, formatUser=True)
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
        await bot.say("`{}` is already blacklisted".format(format_user(user)))
        return
    blacklistuser(id, user.name, user.discriminator, reason)
    await bot.say("Blacklisted `{}` Reason: `{}`".format(format_user(user), reason))
    try:
        await bot.send_message(user, "You have been blacklisted from the bot by `{}` Reason: `{}`".format(format_user(ctx.message.author), reason))
    except:
        log.debug("Couldn't send a message to a user with an ID of \"{}\"".format(id))
    await channel_logger.log_to_channel(":warning: `{}` blacklisted `{}`/`{}` Reason: `{}`".format(format_user(ctx.message.author), id, format_user(user), reason))

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
        await bot.send_message(discord.User(id=id), "You have been unblacklisted from the bot by `{}`".format(format_user(ctx.message.author)))
    except:
        log.debug("Couldn't send a message to a user with an ID of \"{}\"".format(id))
    await channel_logger.log_to_channel(":warning: `{}` unblacklisted `{}`/`{}#{}`".format(format_user(ctx.message.author), id, entry.get("name"), entry.get("discrim")))

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
        await bot.say("The status is currently locked.")
        return
    await bot.change_presence(game=discord.Game(name=name, type=1, url="https://www.twitch.tv/creeperseth"))
    await bot.say("Now streaming `{}`".format(name))
    await channel_logger.log_to_channel(":information_source: `{}`/`{}` changed the streaming status to `{}`".format(ctx.message.author.id, format_user(ctx.message.author), name))

@bot.command(pass_context=True)
async def changestatus(ctx, status:str, *, name:str=None):
    """Changes the bot's status with the specified status type and name"""
    if lock_status:
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
        await channel_logger.log_to_channel(":information_source: `{}`/`{}` Changed game name to `{}` with a(n) `{}` status type".format(ctx.message.author.id, format_user(ctx.message.author), name, status))
    else:
        await bot.say("Changed status type to `{}`".format(status))
        await channel_logger.log_to_channel(":information_source: `{}`/`{}` has changed the status type to `{}`".format(ctx.message.author.id, format_user(ctx.message.author), status))

@bot.command(hidden=True, pass_context=True)
@checks.is_dev()
async def terminal(ctx, *, command:str):
    """Runs terminal commands and shows the output via a message. Oooh spoopy!"""
    try:
        await bot.send_typing(ctx.message.channel)
        await bot.say(xl.format(os.popen(command).read()))
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
    await bot.say("For command usages and a list of commands go to http://ruby.creeperseth.com or do `{0}help` (`{0}help command` for a command usage)\n{1}".format(bot.command_prefix, diff.format("\n".join(map(str, change_log)))))

@bot.command()
async def version():
    """Get the bot's current version"""
    await bot.say("Bot version: {}\nAuthor(s): {}\nCode name: {}\nBuild date: {}".format(BUILD_VERSION, BUILD_AUTHORS, BUILD_CODENAME, BUILD_DATE))

@bot.command(hidden=True, pass_context=True)
@checks.is_dev()
async def dm(ctx, id:str, *, message:str):
    """DMs a user"""
    msg = make_message_embed(ctx.message.author, 0xCC0000, message, formatUser=True)
    try:
        await bot.send_message(discord.User(id=id), "You have received a message from one of the bot developers!", embed=msg)
        await bot.say("Message sent!")
    except:
        await bot.say("Could not send a message to the user.")

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
    await bot.send_message(ctx.message.author, "Here is the link to my server: https://discord.gg/enDDbMC (if the invite link is expired, report it using {}notifydev)".format(bot.command_prefix))

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
    await bot.say("My official website can be found here: http://ruby.creeperseth.com")

@bot.command()
async def github():
    """Gives the link to the github repo"""
    await bot.say("My official github repo can be found here: https://github.com/CreeperSeth/RubyRoseBot")

@bot.command()
async def stats():
    """Gets the bot's stats"""
    voice_clients = []
    for server in list(bot.get_all_servers):
        if server.me.voice_channel:
            voice_clients.append(server.me.voice_channel)
    await bot.say("```xl\n ~~~~~~Ruby Stats~~~~~\nUsers: {}\nServers: {}\nChannels: {}\nActive Voice Clients: {}\nPrivate Channels: {}\ndiscord.py Version: {}\n~~~~~~~~~~~~~~~~~~~~~~~~~~\n```".format(len(list(bot.get_all_members())), len(bot.servers), len(list(bot.get_all_channels())), len(voice_clients), len(list(bot.private_channels)), discord.__version__))

try:
    loop.run_until_complete(bot.login(config._token))
    loop.run_until_complete(bot.connect())
except:
    loop.run_until_complete(os.system("bot.py"))
finally:
    aiosession.close()
    loop.close()
