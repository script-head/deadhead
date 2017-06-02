from discord.ext import commands
from utils.mysql import *
from utils.tools import *
from utils import checks

class Configuration():
    def __init__(self, bot):
        self.bot = bot

    @checks.is_server_owner()
    @commands.command(pass_context=True)
    async def config(self, ctx, type:str, *, value:str):
        """Modifies the server's local config"""
        await self.bot.send_typing(ctx.message.channel)
        if type == "mod-role" or type == "mute-role" or type == "enable-ranking":
            if type == "ranking":
                try:
                    global bool
                    bool = convert_to_bool(value)
                    update_data_entry(ctx.message.server.id, "ranking", bool)
                except ValueError:
                    await self.bot.say("`{}` is not a valid bool!".format(value))
                    return
            else:
                update_data_entry(ctx.message.server.id, type, value)
            if type == "enable-ranking":
                if bool:
                    action = "enabled"
                else:
                    action = "disabled"
                await self.bot.say("Successfully {} the ranking system".format(action))
            else:
                await self.bot.say("Successfully set the {} to `{}`".format(type, value))
        else:
            await self.bot.say("`{}` is not a valid type! Valid types are `mod-role`, `mute-role`, and `enable-ranking`".format(type))

    @commands.command(pass_context=True)
    async def showconfig(self, ctx):
        """Shows the server's configuration"""
        await self.bot.send_typing(ctx.message.channel)
        mod_role_name = read_data_entry(ctx.message.server.id, "mod-role")
        mute_role_name = read_data_entry(ctx.message.server.id, "mute-role")
        ranking_enabled = read_data_entry(ctx.message.server.id, "enable-ranking")
        fields = {"Mod Role":mod_role_name, "Mute Role":mute_role_name, "Ranking":ranking_enabled}
        embed = make_list_embed(fields)
        embed.title = "Server Configuration"
        embed.color = 0xFF0000
        await self.bot.say(embed=embed)

    @checks.is_server_owner()
    @commands.command(pass_context=True)
    async def joinleave(self, ctx, type:str, *, value:str):
        """Configures on user join and leave settings"""
        await self.bot.send_typing(ctx.message.channel)
        if type == "join-message":
            update_data_entry(ctx.message.server.id, type, value)
            await self.bot.say("Successfully set the join message to: {}".format(value.replace("!USER!", "@{}".format(ctx.message.author.name)).replace("!SERVER!", ctx.message.server.name)))
        elif type == "leave-message":
            update_data_entry(ctx.message.server.id, type, value)
            await self.bot.say("Successfully set the leave message to: {}".format(value.replace("!USER!", "@{}".format(ctx.message.author.name)).replace("!SERVER!", ctx.message.server.name)))
        elif type == "channel":
            if value == "remove":
                update_data_entry(ctx.message.server.id, "join-leave-channel", None)
                await self.bot.say("Successfully disabled join-leave messages")
                return
            channel = discord.utils.get(ctx.message.server.channels, name=value)
            if channel is None:
                await self.bot.say("There is no channel on this server named `{}`".format(value))
                return
            update_data_entry(ctx.message.server.id, "join-leave-channel", channel.id)
            await self.bot.say("Successfully set the join-leave-channel to: {}".format(channel.mention))
        elif type == "join-role":
            if value == "remove":
                update_data_entry(ctx.message.server.id, type, None)
                await self.bot.say("Successfully disabled the join-role")
                return
            role = discord.utils.get(ctx.message.server.roles, name=value)
            if role is None:
                await self.bot.say("There is no role on this server named `{}`".format(value))
                return
            update_data_entry(ctx.message.server.id, type, role.id)
            await self.bot.say("Successfully set the join-role to: {}".format(role.name))
        else:
            await self.bot.say("`{}` is not a valid type! Valid types are `join-message`, `leave-message`, `channel`, and `mute-role`".format(type))

    @commands.command(pass_context=True)
    async def showjoinleaveconfig(self, ctx):
        """Shows the on user join and leave config"""
        join_message = read_data_entry(ctx.message.server.id, "join-message")
        if join_message is not None:
            join_message = join_message.replace("!USER!", "@{}".format(ctx.message.author.name)).replace("!SERVER!", ctx.message.server.name)
        leave_message = read_data_entry(ctx.message.server.id, "leave-message")
        if leave_message is not None:
            leave_message = leave_message.replace("!USER!", "@{}".format(ctx.message.author.name)).replace("!SERVER!", ctx.message.server.name)
        join_leave_channel_id = read_data_entry(ctx.message.server.id, "join-leave-channel")
        if join_leave_channel_id is not None:
            join_leave_channel = discord.utils.get(ctx.message.server.channels, id=join_leave_channel_id).mention
            if join_leave_channel is None:
                update_data_entry(ctx.message.server.id, "join-leave-channel", None)
        else:
            join_leave_channel = None
        join_role_id = read_data_entry(ctx.message.server.id, "join-role")
        if join_role_id is not None:
            join_role = discord.utils.get(ctx.message.server.roles, id=join_role_id).name
            if join_role is None:
                update_data_entry(ctx.message.server.id, "join-role", None)
        else:
            join_role = None
        fields = {"Join Message":join_message, "Leave Message":leave_message, "Channel":join_leave_channel, "Join Role":join_role}
        embed = make_list_embed(fields)
        embed.title = "Configuration for join and leave events"
        embed.color = 0xFF0000
        await self.bot.say(embed=embed)


def setup(bot):
    bot.add_cog(Configuration(bot))
