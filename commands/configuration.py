from discord.ext import commands
from utils.mysql import *
from utils.tools import *
from utils import checks
from utils.language import Language

class Configuration(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @checks.is_guild_owner()
    @commands.guild_only()
    @commands.command()
    async def config(self, ctx, type:str, *, value:str):
        """Modifies the server's local config"""
        await ctx.channel.trigger_typing()
        if type == "mod-role" or type == "mute-role":
            update_data_entry(ctx.guild.id, type, value)
            await ctx.send(Language.get("configuration.set_success", ctx).format(type, value))
        else:
            await ctx.send(Language.get("configuration.invalid_set_type", ctx).format(type))

    @commands.command()
    async def showconfig(self, ctx):
        """Shows the server's configuration"""
        await ctx.channel.trigger_typing()
        mod_role_name = read_data_entry(ctx.guild.id, "mod-role")
        mute_role_name = read_data_entry(ctx.guild.id, "mute-role")
        fields = {Language.get("configuration.mod_role", ctx):mod_role_name, Language.get("configuration.mute_role", ctx):mute_role_name}
        embed = make_list_embed(fields)
        embed.title = Language.get("configuration.server_configuration", ctx)
        embed.color = 0xFF0000
        await ctx.send(embed=embed)

    @checks.is_guild_owner()
    @commands.guild_only()
    @commands.command()
    async def joinleave(self, ctx, type:str, *, value:str):
        """Configures on user join and leave settings"""
        await ctx.channel.trigger_typing()
        if type == "join-message":
            update_data_entry(ctx.guild.id, type, value)
            await ctx.send(Language.get("configuration.join_message_set_success", ctx).format(value.replace("%user%", "@{}".format(ctx.author.name)).replace("%server%", ctx.guild.name)))
        elif type == "leave-message":
            update_data_entry(ctx.guild.id, type, value)
            await ctx.send(Language.get("configuration.leave_message_set_success", ctx).format(value.replace("%user%", "@{}".format(ctx.author.name)).replace("%server%", ctx.guild.name)))
        elif type == "channel":
            if value == "remove":
                update_data_entry(ctx.guild.id, "join-leave-channel", None)
                await ctx.send(Language.get("configuration.join-leave_disabled", ctx))
                return
            channel = discord.utils.get(ctx.guild.channels, name=value)
            if channel is None:
                await ctx.send(Language.get("configuration.channel_not_found", ctx).format(value))
                return
            update_data_entry(ctx.guild.id, "join-leave-channel", channel.id)
            await ctx.send(Language.get("configuration.join-leave_channel_set_success", ctx).format(channel.mention))
        elif type == "join-role":
            if value == "remove":
                update_data_entry(ctx.guild.id, type, None)
                await ctx.send(Language.get("configuration.join-leave_role_disabled", ctx))
                return
            role = discord.utils.get(ctx.guild.roles, name=value)
            if role is None:
                await ctx.send(Language.get("configuration.role_not_found", ctx).format(value))
                return
            update_data_entry(ctx.guild.id, type, role.id)
            await ctx.send(Language.get("configuration.join-role_set_success", ctx).format(role.name))
        else:
            await ctx.send(Language.get("configuration.join_settings_invalid_type", ctx).format(type))

    @commands.guild_only()
    @commands.command()
    async def showjoinleaveconfig(self, ctx):
        """Shows the on user join and leave config"""
        await ctx.channel.trigger_typing()
        join_message = read_data_entry(ctx.guild.id, "join-message")
        if join_message is not None:
            join_message = join_message.replace("%user%", "@{}".format(ctx.author.name)).replace("%server%", ctx.guild.name)
        leave_message = read_data_entry(ctx.guild.id, "leave-message")
        if leave_message is not None:
            leave_message = leave_message.replace("%user%", "@{}".format(ctx.author.name)).replace("%server%", ctx.guild.name)
        join_leave_channel_id = read_data_entry(ctx.guild.id, "join-leave-channel")
        if join_leave_channel_id is not None:
            join_leave_channel = discord.utils.get(ctx.guild.channels, id=join_leave_channel_id).mention
            if join_leave_channel is None:
                update_data_entry(ctx.guild.id, "join-leave-channel", None)
        else:
            join_leave_channel = None
        join_role_id = read_data_entry(ctx.guild.id, "join-role")
        if join_role_id is not None:
            join_role = discord.utils.get(ctx.guild.roles, id=join_role_id).name
            if join_role is None:
                update_data_entry(ctx.guild.id, "join-role", None)
        else:
            join_role = None
        fields = {Language.get("configuration.join_message", ctx):join_message, Language.get("configuration.leave_message", ctx):leave_message, Language.get("configuration.channel", ctx):join_leave_channel, Language.get("configuration.join_role", ctx):join_role}
        embed = make_list_embed(fields)
        embed.title = Language.get("configuration.showjoinleaveconfig_title", ctx)
        embed.color = 0xFF0000
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Configuration(bot))
