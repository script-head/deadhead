import asyncio

from discord.ext import commands
from utils.mysql import *
from utils.channel_logger import Channel_Logger
from utils.tools import *
from utils import checks
from utils.language import Language

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.logger = Channel_Logger(bot)

    @checks.server_mod_or_perms(kick_members=True)
    @commands.guild_only()
    @commands.command()
    async def kick(self, ctx, user:discord.Member):
        """Kicks the specified user from the server"""
        try:
            await ctx.guild.kick(user)
        except discord.errors.Forbidden:
            if user.top_role.position == ctx.me.top_role.position:
                await ctx.send(Language.get("moderation.no_kick_highest_role", ctx))
            elif user.top_role.position > ctx.me.top_role.position:
                await ctx.send(Language.get("moderation.no_kick_higher_role", ctx))
            else:
                await ctx.send(Language.get("moderation.no_kick_perms", ctx))
        await ctx.send(Language.get("moderation.kick_success", ctx).format(user))

    @checks.server_mod_or_perms(ban_members=True)
    @commands.guild_only()
    @commands.command()
    async def ban(self, ctx, user:discord.Member, *, reason:str=None):
        """Bans the specified user from the server"""
        if reason is None:
            reason = Language.get("moderation.no_reason", ctx)
        reason += Language.get("moderation.banned_by", ctx).format(ctx.author)
        try:
            await ctx.guild.ban(user, delete_message_days=0, reason=reason)
        except discord.errors.Forbidden:
            if user.top_role.position == ctx.me.top_role.position:
                await ctx.send(Language.get("moderation.no_ban_highest_role", ctx))
            elif user.top_role.position > ctx.me.top_role.position:
                await ctx.send(Language.get("moderation.no_ban_higher_role", ctx))
            else:
                await ctx.send(Language.get("moderation.no_ban_perms", ctx))
            return
        await ctx.send(Language.get("moderation.ban_success", ctx).format(user))

    @checks.server_mod_or_perms(ban_members=True)
    @commands.guild_only()
    @commands.command()
    async def unban(self, ctx, *, username:str):
        """Unbans the user with the specifed name from the server"""
        try:
            banlist = await ctx.guild.bans()
        except discord.errors.Forbidden:
            await ctx.send(Language.get("moderation.no_ban_perms", ctx))
            return
        user = None
        for ban in banlist:
            if ban.user.name == username:
                user = ban.user
        if user is None:
            await ctx.send(Language.get("moderation.user_not_banned", ctx).format(username))
            return
        await ctx.guild.unban(user)
        await ctx.send(Language.get("moderation.unban_success", ctx).format(user))

    @checks.server_mod_or_perms(ban_members=True)
    @commands.guild_only()
    @commands.command()
    async def banid(self, ctx, id:int, *, reason:str=None):
        """Bans the user with the specified id from the server (Useful if the user isn't on the server yet)"""
        if reason is None:
            reason = Language.get("moderation.no_reason", ctx)
        reason += Language.get("moderation.banned_by", ctx).format(ctx.author)
        try:
            await self.bot.http.ban(id, ctx.guild.id, delete_message_days=0, reason=reason)
        except discord.errors.HTTPException or discord.errors.NotFound:
            await ctx.send(Language.get("moderation.invalid_user_id", ctx).format(id))
            return
        except discord.errors.Forbidden:
            await ctx.send(Language.get("moderation.no_ban_perms", ctx))
            return
        banlist = await ctx.guild.bans()
        for ban in banlist:
            if ban.user.id == id:
                user = ban.user
        await ctx.send(Language.get("moderation.ban_success", ctx).format(user))

    @commands.guild_only()
    @commands.command()
    async def banlist(self, ctx):
        """Displays the server's banlist"""
        try:
            banlist = await ctx.guild.bans()
        except discord.errors.Forbidden:
            await ctx.send(Language.get("moderation.no_ban_perms", ctx))
            return
        bancount = len(banlist)
        display_bans = []
        bans = None
        if bancount == 0:
            bans = Language.get("moderation.no_bans", ctx)
        else:
            for ban in banlist:
                if len(", ".join(display_bans)) < 1800:
                    display_bans.append(str(ban.user))
                else:
                    bans = ", ".join(display_bans) + Language.get("moderation.banlist_and_more", ctx).format(len(banlist) - len(display_bans))
                    break
        if not bans:
            bans = ", ".join(display_bans)
        await ctx.send(Language.get("moderation.banlist", ctx).format(bancount, bans))

    @checks.server_mod_or_perms(manage_roles=True)
    @commands.guild_only()
    @commands.command()
    async def mute(self, ctx, user:discord.Member, *, reason:str=None):
        """Mutes the specified user"""
        if reason is None:
            reason = Language.get("moderation.no_reason", ctx)
        reason += Language.get("moderation.muted_by", ctx).format(ctx.author)
        mute_role_name = read_data_entry(ctx.guild.id, "mute-role")
        mute_role = discord.utils.get(ctx.guild.roles, name=mute_role_name)
        if mute_role is None:
            await ctx.send(Language.get("moderation.role_not_found", ctx).format(mute_role_name))
            return
        try:
            await user.add_roles(mute_role, reason=reason)
            await ctx.send(Language.get("moderation.mute_success", ctx).format(user))
        except discord.errors.Forbidden:
            if mute_role.position == ctx.me.top_role.position:
                await ctx.send(Language.get("moderation.no_mute_highest_role", ctx))
            elif mute_role.position > ctx.me.top_role.position:
                await ctx.send(Language.get("moderation.no_mute_higher_role", ctx))
            else:
                await ctx.send(Language.get("moderation.no_manage_role_perms", ctx))

    @checks.server_mod_or_perms(manage_roles=True)
    @commands.guild_only()
    @commands.command()
    async def unmute(self, ctx, user:discord.Member):
        """Unmutes the specified user"""
        mute_role_name = read_data_entry(ctx.guild.id, "mute-role")
        mute_role = discord.utils.get(ctx.guild.roles, name=mute_role_name)
        if mute_role is None:
            await ctx.send(Language.get("moderation.role_not_found", ctx).format(mute_role_name))
            return
        try:
            await user.remove_roles(user, mute_role, reason=Language.get("moderation.unmuted_by", ctx).format(ctx.author))
            await ctx.send(Language.get("moderation.unmute_success", ctx).format(user))
        except discord.errors.Forbidden:
            if mute_role.position == ctx.me.top_role.position:
                await ctx.send(Language.get("moderation.no_unmute_highest_role", ctx))
            elif mute_role.position > ctx.me.top_role.position:
                await ctx.send(Language.get("moderation.no_unmute_higher_role", ctx))
            else:
                await ctx.send(Language.get("moderation.no_manage_role_perms", ctx))

    @checks.server_mod_or_perms(manage_messages=True)
    @commands.guild_only()
    @commands.command()
    async def prune(self, ctx, amount:int):
        """Prunes the specified amount of messages (you can also prune messages from a specific user too)"""
        try:
            await ctx.message.delete()
        except discord.errors.Forbidden:
            await ctx.send(Language.get("moderation.no_manage_messages_perms", ctx))
            return
        deleted = await ctx.channel.purge(limit=amount)
        deleted_message = await ctx.send(Language.get("moderation.pruned", ctx).format(ctx.author.mention, len(deleted)))
        await asyncio.sleep(10)
        # The try and except pass is so in the event a user prunes again or deletes the prune notification before the bot automatically does it, it will not raise an error
        try:
            await deleted_message.delete()
        except:
            pass

    @checks.server_mod_or_perms(manage_messages=True)
    @commands.command()
    async def pin(self, ctx, id:int):
        """Pins the message with the specified ID to the channel"""
        try:
            message = await ctx.channel.fetch_message(id)
        except discord.errors.NotFound:
            await ctx.send(Language.get("bot.no_message_found", ctx).format(id))
            return
        try:
            await message.pin()
        except discord.errors.Forbidden:
            await ctx.send(Language.get("moderation.no_manage_messages_perms", ctx))

    @checks.server_mod_or_perms(manage_messages=True)
    @commands.command()
    async def unpin(self, ctx, id:int):
        """Unpins the message with the specified ID from the channel"""
        pinned_messages = await ctx.channel.pins()
        message = discord.utils.get(pinned_messages, id=id)
        if message is None:
            await ctx.send(Language.get("moderation.no_pinned_message_found", ctx).format(id))
            return
        try:
            await message.unpin()
            await ctx.send(Language.get("moderation.unpin_success", ctx))
        except discord.errors.Forbidden:
            await ctx.send(Language.get("moderation.no_manage_messages_perms", ctx))

    @checks.server_mod_or_perms(manage_roles=True)
    @commands.guild_only()
    @commands.command()
    async def addrole(self, ctx, user:discord.Member, *, name:str):
        """Adds the specified role to the specified user"""
        role = discord.utils.get(ctx.guild.roles, name=name)
        if role is None:
            await ctx.send(Language.get("moderation.role_not_found", ctx).format(name))
            return
        try:
            await user.add_roles(role, reason=Language.get("moderation.addrole_reason", ctx).format(role.name, ctx.author))
            await ctx.send(Language.get("moderation.addrole_success", ctx).format(name, user))
        except discord.errors.Forbidden:
            if role.position == ctx.me.top_role.position:
                await ctx.send(Language.get("moderation.no_addrole_highest_role", ctx))
            elif role.position > ctx.me.top_role.position:
                await ctx.send(Language.get("moderation.no_addrole_higher_role", ctx))
            else:
                await ctx.send(Language.get("moderation.no_manage_role_perms", ctx))

    @checks.server_mod_or_perms(manage_roles=True)
    @commands.guild_only()
    @commands.command()
    async def removerole(self, ctx, user:discord.Member, *, name:str):
        """Removes the specified role from the specified user"""
        role = discord.utils.get(ctx.guild.roles, name=name)
        if role is None:
            await ctx.send(Language.get("moderation.role_not_found", ctx).format(name))
            return
        try:
            await user.remove_roles(role, reason=Language.get("moderation.removerole_reason", ctx).format(role.name, ctx.author))
            await ctx.send(Language.get("moderation.remove_role_success", ctx).format(name, user))
        except discord.errors.Forbidden:
            if role.position == ctx.me.top_role.position:
                await ctx.send(Language.get("moderation.no_removerole_highest_role", ctx))
            elif role.position > ctx.me.top_role.position:
                await ctx.send(Language.get("moderation.no_removerole_higher_role", ctx))
            else:
                await ctx.send(Language.get("moderation.no_manage_role_perms", ctx))

    @checks.server_mod_or_perms(manage_roles=True)
    @commands.guild_only()
    @commands.command()
    async def createrole(self, ctx, *, name:str):
        """Creates a role with the specified name"""
        try:
            await ctx.guild.create_role(name=name, reason=Language.get("createrole_reason", ctx).format(ctx.author), permissions=ctx.guild.default_role.permissions)
            await ctx.send(Language.get("createrole_success", ctx).format(name))
        except discord.errors.Forbidden:
            await ctx.send(Language.get("moderation.no_manage_role_perms", ctx))

    @checks.server_mod_or_perms(manage_roles=True)
    @commands.guild_only()
    @commands.command()
    async def deleterole(self, ctx, *, name:str):
        """Deletes the role with the specified name"""
        role = discord.utils.get(ctx.guild.roles, name=name)
        if role is None:
            await ctx.send(Language.get("moderation.role_not_found", ctx).format(name))
            return
        try:
            await role.delete(reason=Language.get("moderation.deleterole_reason", ctx).format(ctx.author))
            await ctx.send(Language.get("moderation.deleterole_success", ctx).format(name))
        except discord.errors.Forbidden:
            if role.position == ctx.me.top_role.position:
                await ctx.send(Language.get("moderation.no_deleterole_highest_role", ctx))
            elif role.position > ctx.me.top_role.position:
                await ctx.send(Language.get("moderation.no_deleterole_higher_role", ctx))
            else:
                await ctx.send(Language.get("moderation.no_manage_role_perms", ctx))

    @checks.server_mod_or_perms(manage_roles=True)
    @commands.guild_only()
    @commands.command()
    async def editrole(self, ctx, type:str, value:str, *, name:str):
        """Edits a role with the specified name"""
        role = discord.utils.get(ctx.guild.roles, name=name)
        if role is None:
            await ctx.send(Language.get("moderation.role_not_found", ctx).format(name))
            return
        if type == "color":
            if value != "remove":
                try:
                    color = discord.Color(value=int(value.strip("#"), 16))
                except:
                    await ctx.send(Language.get("bot.invalid_color", ctx).format(value))
                    return
            else:
                color = discord.Color.default()
            try:
                await role.edit(reason=Language.get("moderation.editrole_reason", ctx).format(ctx.author), color=color)
                await ctx.send(Language.get("moderation.editrole_success", ctx).format(name))
            except discord.errors.Forbidden:
                if role.position == ctx.me.top_role.position:
                    await ctx.send(Language.get("moderation.no_editrole_highest_role", ctx))
                elif role.position > ctx.me.top_role.position:
                    await ctx.send(Language.get("moderation.no_editrole_higher_role", ctx))
                else:
                    await ctx.send(Language.get("moderation.no_manage_role_perms", ctx))
        elif type == "permissions":
            try:
                perms = discord.Permissions(permissions=int(value))
            except:
                await ctx.send(Language.get("moderation.invalid_permission_number", ctx).format(value))
                return
            try:
                await role.edit(reason=Language.get("moderation.editrole_reason", ctx).format(ctx.author), permissions=perms)
                await ctx.send(Language.get("moderation.editrole_success", ctx).format(name))
            except discord.errors.Forbidden:
                if role.position == ctx.me.top_role.position:
                    await ctx.send(Language.get("moderation.no_editrole_highest_role", ctx))
                elif role.position > ctx.me.top_role.position:
                    await ctx.send(Language.get("moderation.no_editrole_higher_role", ctx))
                else:
                    await ctx.send(Language.get("moderation.no_manage_role_perms", ctx))
        elif type == "position":
            try:
                pos = int(value)
            except:
                await ctx.send(Language.get("moderation.invalid_number", ctx).format(pos))
                return
            if pos >= ctx.guild.me.top_role.position:
                await ctx.send(Language.get("moderation.pos_too_high", ctx).format(ctx.guild.me.top_role.position))
                return
            try:
                if pos <= 0:
                    pos = 1
                await role.edit(reason=Language.get("moderation.moverole_reason", ctx).format(ctx.author), position=pos)
                await ctx.send(Language.get("moderation.editrole_success", ctx).format(name))
            except discord.errors.Forbidden:
                if role.position == ctx.me.top_role.position:
                    await ctx.send(Language.get("moderation.no_editrole_highest_role", ctx))
                elif role.position > ctx.me.top_role.position:
                    await ctx.send(Language.get("moderation.no_editrole_higher_role", ctx))
                else:
                    await ctx.send(Language.get("moderation.no_manage_role_perms", ctx))
        elif type == "separate":
            try:
                bool = convert_to_bool(value)
            except ValueError:
                await ctx.send(Language.get("moderation.invalid_bool", ctx).format(value))
                return
            try:
                await role.edit(reason=Language.get("moderation.editrole_reason", ctx).format(ctx.author), hoist=bool)
                await ctx.send(Language.get("moderation.editrole_success", ctx).format(name))
            except discord.errors.Forbidden:
                if role.position == ctx.me.top_role.position:
                    await ctx.send(Language.get("moderation.no_editrole_highest_role", ctx))
                elif role.position > ctx.me.top_role.position:
                    await ctx.send(Language.get("moderation.no_editrole_higher_role", ctx))
                else:
                    await ctx.send(Language.get("moderation.no_manage_role_perms", ctx))
        elif type == "mentionable":
            try:
                bool = convert_to_bool(value)
            except ValueError:
                await ctx.send(Language.get("moderation.invalid_bool", ctx).format(value))
                return
            try:
                await role.edit(reason=Language.get("moderation.editrole_reason", ctx).format(ctx.author), mentionable=bool)
                await ctx.send(Language.get("moderation.editrole_success", ctx).format(name))
            except discord.errors.Forbidden:
                if role.position == ctx.me.top_role.position:
                    await ctx.send(Language.get("moderation.no_editrole_highest_role", ctx))
                elif role.position > ctx.me.top_role.position:
                    await ctx.send(Language.get("moderation.no_editrole_higher_role", ctx))
                else:
                    await ctx.send(Language.get("moderation.no_manage_role_perms", ctx))
        else:
            await ctx.send(Language.get("moderation.invalid_editrole_type", ctx))

    @checks.server_mod_or_perms(manage_roles=True)
    @commands.guild_only()
    @commands.command()
    async def renamerole(self, ctx, name:str, newname:str):
        """Renames a role with the specified name, be sure to put double quotes (\") around the name and the new name"""
        role = discord.utils.get(ctx.guild.roles, name=name)
        if role is None:
            await ctx.send(Language.get("moderation.role_not_found", ctx).format(name))
            return
        try:
            await role.edit(reason=Language.get("moderation.renamerole_reason", ctx).format(ctx.author), name=newname)
            await ctx.send(Language.get("moderation.renamerole_success", ctx).format(name, newname))
        except discord.errors.Forbidden:
            if role.position == ctx.me.top_role.position:
                await ctx.send(Language.get("moderation.no_renamerole_highest_role", ctx))
            elif role.position > ctx.me.top_role.position:
                await ctx.send(Language.get("moderation.no_renamerole_higher_role", ctx))
            else:
                await ctx.send(Language.get("moderation.no_manage_role_perms", ctx))

    @checks.server_mod_or_perms(ban_members=True)
    @commands.guild_only()
    @commands.command()
    async def massban(self, ctx, *, ids:str):
        """Mass bans users by ids (separate ids with spaces)"""
        await ctx.channel.trigger_typing()
        ids = ids.split(" ")
        failed_ids = []
        success = 0
        for id in ids:
            try:
                await self.bot.http.ban(int(id), ctx.guild.id, delete_message_days=0)
                success += 1
            except:
                failed_ids.append("`{}`".format(id))
        if len(failed_ids) != 0:
            await ctx.send(Language.get("moderation.massban_failed_ids", ctx).format(", ".join(ids)))
        await ctx.send(Language.get("moderation.massban_success", ctx).format(success, len(ids)))

    @checks.server_mod_or_perms(manage_messages=True)
    @commands.guild_only()
    @commands.command()
    async def removereactions(self, ctx, id:int):
        """Clear reactions from a message"""
        try:
            message = await ctx.channel.fetch_message(id)
        except discord.errors.NotFound:
            await ctx.send(Language.get("bot.no_message_found", ctx).format(id))
            return
        try:
            await message.clear_reactions()
            await ctx.send(Language.get("moderation.removereactions_success", ctx))
        except discord.errors.Forbidden:
            await ctx.send(Language.get("moderation.no_manage_messages_perms", ctx))

def setup(bot):
    bot.add_cog(Moderation(bot))
