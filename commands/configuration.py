from discord.ext import commands
from utils.mysql import *
from utils.tools import *
from utils import checks

class Configuration():
    def __init__(self, bot):
        self.bot = bot

    @checks.is_guild_owner()
    @commands.guild_only()
    @commands.command()
    async def config(self, ctx, type:str, *, value:str):
        """Modifies the server's local config"""
        await ctx.channel.trigger_typing()
        if type == "mod-role" or type == "mute-role" or type == "enable-ranking":
            if type == "ranking":
                try:
                    global bool
                    bool = convert_to_bool(value)
                    update_data_entry(ctx.guild.id, "ranking", bool)
                except ValueError:
                    await ctx.send("`{}` is not a valid bool!".format(value))
                    return
            else:
                update_data_entry(ctx.guild.id, type, value)
            if type == "enable-ranking":
                if bool:
                    action = "enabled"
                else:
                    action = "disabled"
                await ctx.send("Successfully {} the ranking system".format(action))
            else:
                await ctx.send("Successfully set the {} to `{}`".format(type, value))
        else:
            await ctx.send("`{}` is not a valid type! Valid types are `mod-role`, `mute-role`, and `enable-ranking`".format(type))

    @commands.command()
    async def showconfig(self, ctx):
        """Shows the server's configuration"""
        await ctx.channel.trigger_typing()
        mod_role_name = read_data_entry(ctx.guild.id, "mod-role")
        mute_role_name = read_data_entry(ctx.guild.id, "mute-role")
        ranking_enabled = read_data_entry(ctx.guild.id, "enable-ranking")
        fields = {"Mod Role":mod_role_name, "Mute Role":mute_role_name, "Ranking":ranking_enabled}
        embed = make_list_embed(fields)
        embed.title = "Server Configuration"
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
            await ctx.send("Successfully set the join message to: {}".format(value.replace("%user%", "@{}".format(ctx.author.name)).replace("%server%", ctx.guild.name)))
        elif type == "leave-message":
            update_data_entry(ctx.guild.id, type, value)
            await ctx.send("Successfully set the leave message to: {}".format(value.replace("%user%", "@{}".format(ctx.author.name)).replace("%server%", ctx.guild.name)))
        elif type == "channel":
            if value == "remove":
                update_data_entry(ctx.guild.id, "join-leave-channel", None)
                await ctx.send("Successfully disabled join-leave messages")
                return
            channel = discord.utils.get(ctx.guild.channels, name=value)
            if channel is None:
                await ctx.send("There is no channel on this server named `{}`".format(value))
                return
            update_data_entry(ctx.guild.id, "join-leave-channel", channel.id)
            await ctx.send("Successfully set the join-leave-channel to: {}".format(channel.mention))
        elif type == "join-role":
            if value == "remove":
                update_data_entry(ctx.guild.id, type, None)
                await ctx.send("Successfully disabled the join-role")
                return
            role = discord.utils.get(ctx.guild.roles, name=value)
            if role is None:
                await ctx.send("There is no role on this server named `{}`".format(value))
                return
            update_data_entry(ctx.guild.id, type, role.id)
            await ctx.send("Successfully set the join-role to: {}".format(role.name))
        else:
            await ctx.send("`{}` is not a valid type! Valid types are `join-message`, `leave-message`, `channel`, and `mute-role`".format(type))

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
        fields = {"Join Message":join_message, "Leave Message":leave_message, "Channel":join_leave_channel, "Join Role":join_role}
        embed = make_list_embed(fields)
        embed.title = "Configuration for join and leave events"
        embed.color = 0xFF0000
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Configuration(bot))
