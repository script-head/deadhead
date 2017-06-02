from discord.ext import commands
from utils.config import Config
from utils.mysql import *
config = Config()

class dev_only(commands.CommandError):
    pass

class owner_only(commands.CommandError):
    pass

class not_nsfw_channel(commands.CommandError):
    pass

class not_server_owner(commands.CommandError):
    pass

class no_permission(commands.CommandError):
    pass

def is_owner():
    def predicate(ctx):
        if ctx.message.author.id == config.owner_id:
            return True
        else:
            raise owner_only
    return commands.check(predicate)

def is_dev():
    def predicate(ctx):
        if ctx.message.author.id in config.dev_ids or ctx.message.author.id == config.owner_id:
            return True
        else:
            raise dev_only
    return commands.check(predicate)

def is_nsfw_channel():
    def predicate(ctx):
        if ctx.message.channel.name == "nsfw" or ctx.message.channel.name.startswith("nsfw-"):
            return True
        else:
            raise not_nsfw_channel
    return commands.check(predicate)

def is_server_owner():
    def predicate(ctx):
        if ctx.message.author.id == ctx.message.server.owner_id:
            return True
        else:
            raise not_server_owner
    return commands.check(predicate)

def server_mod_or_perms(**permissions):
    def predicate(ctx):
        mod_role_name = read_data_entry(ctx.message.server.id, "mod-role")
        mod = discord.utils.get(ctx.message.author.roles, name=mod_role_name)
        if mod or permissions and all(getattr(ctx.message.channel.permissions_for(ctx.message.author), name, None) == value for name, value in permissions.items()):
            return True
        else:
            raise no_permission
    return commands.check(predicate)

def has_permissions(**permissions):
    def predicate(ctx):
        if all(getattr(ctx.message.channel.permissions_for(ctx.message.author), name, None) == value for name, value in permissions.items()):
            return True
        else:
            raise no_permission
    return commands.check(predicate)

