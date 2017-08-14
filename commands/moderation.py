import asyncio

from discord.ext import commands
from utils.mysql import *
from utils.channel_logger import Channel_Logger
from utils.tools import *
from utils import checks

class Moderation():
    def __init__(self, bot):
        self.bot = bot
        self.logger = Channel_Logger(bot)

    @checks.server_mod_or_perms(kick_members=True)
    @commands.command()
    async def kick(self, ctx, user:discord.Member):
        """Kicks the specified user from the server"""
        try:
            await ctx.guild.kick(user)
        except discord.errors.Forbidden:
            if user.top_role.position == ctx.me.top_role.position:
                await ctx.send("I cannot kick that user because their highest role is the same highest role as mine")
            elif user.top_role.position > ctx.me.top_role.position:
                await ctx.send("I cannot kick that user because their highest role is higher than mine")
            else:
                await ctx.send("I do not have the `Kick Members` permission")
        await ctx.send("Successfully kicked `{}`".format(user))

    @checks.server_mod_or_perms(ban_members=True)
    @commands.command()
    async def ban(self, ctx, user:discord.Member, *, reason:str=None):
        """Bans the specified user from the server"""
        if reason is None:
            reason = "No reason was specified"
        reason += "**\n\n**Banned by {}".format(ctx.author)
        try:
            await ctx.guild.ban(user, delete_message_days=0, reason=reason)
        except discord.errors.Forbidden:
            if user.top_role.position == ctx.me.top_role.position:
                await ctx.send("I cannot ban that user because their highest role is the same highest role as mine")
            elif user.top_role.position > ctx.me.top_role.position:
                await ctx.send("I cannot ban that user because their highest role is higher than mine")
            else:
                await ctx.send("I do not have the `Ban Members` permission")
            return
        await ctx.send("Successfully banned `{}`".format(user))

    @checks.server_mod_or_perms(ban_members=True)
    @commands.command()
    async def unban(self, ctx, *, username:str):
        """Unbans the user with the specifed name from the server"""
        try:
            banlist = await ctx.guild.bans()
        except discord.errors.Forbidden:
            await ctx.send("I do not have the `Ban Members` permission")
            return
        user = None
        for ban in banlist:
            if ban.user.name == username:
                user = ban.user
        if user is None:
            await ctx.send("No banned user was found with the username of `{}`".format(username))
            return
        await ctx.guild.unban(user)
        await ctx.send("Successfully unbanned `{}`".format(user))

    @checks.server_mod_or_perms(ban_members=True)
    @commands.command()
    async def banid(self, ctx, id:int, *, reason:str=None):
        """Bans the user with the specified id from the server (Useful if the user isn't on the server yet)"""
        if reason is None:
            reason = "No reason was specified"
        reason += "**\n\n**Banned by {}".format(ctx.author)
        try:
            await self.bot.http.ban(id, ctx.guild.id, delete_message_days=0, reason=reason)
        except discord.errors.HTTPException or discord.errors.NotFound:
            await ctx.send("No discord user has the id of `{}`".format(id))
            return
        except discord.errors.Forbidden:
            await ctx.send("I do not have the `Ban Members` permission")
            return
        banlist = await ctx.guild.bans()
        for ban in banlist:
            if ban.user.id == id:
                user = ban.user
        await ctx.send("Successfully banned `{}`".format(user))

    @commands.command()
    async def banlist(self, ctx):
        """Displays the server's banlist"""
        try:
            banlist = await ctx.guild.bans()
        except discord.errors.Forbidden:
            await ctx.send("I do not have the `Ban Members` permission")
            return
        bancount = len(banlist)
        display_bans = []
        bans = None
        if bancount == 0:
            bans = "No users are banned from this server"
        else:
            for ban in banlist:
                if len(", ".join(display_bans)) < 1800:
                    display_bans.append(str(ban.user))
                else:
                    bans = ", ".join(display_bans) + "\n... and {} more".format(len(banlist) - len(display_bans))
                    break
        if not bans:
            bans = ", ".join(display_bans)
        await ctx.send("Total bans: `{}`\n```{}```".format(bancount, bans))

    @checks.server_mod_or_perms(manage_roles=True)
    @commands.command()
    async def mute(self, ctx, user:discord.Member, *, reason:str=None):
        """Mutes the specified user"""
        if reason is None:
            reason = "No reason was specified"
        reason += "**\n\n**Muted by {}".format(ctx.author)
        mute_role_name = read_data_entry(ctx.guild.id, "mute-role")
        mute_role = discord.utils.get(ctx.guild.roles, name=mute_role_name)
        if mute_role is None:
            await ctx.send("I could not find any role named `{}`".format(mute_role_name))
            return
        try:
            await user.add_roles(mute_role, reason=reason)
            await ctx.send("Successfully muted `{}`".format(user))
        except discord.errors.Forbidden:
            if mute_role.position == ctx.me.top_role.position:
                await ctx.send("I cannot add the mute role to users as it's my highest role, y u mute me like dis")
            elif mute_role.position > ctx.me.top_role.position:
                await ctx.send("I cannot mute users as the mute role is higher than my highest role")
            else:
                await ctx.send("I do not have the `Manage Roles` permission")

    @checks.server_mod_or_perms(manage_roles=True)
    @commands.command()
    async def unmute(self, ctx, user:discord.Member):
        """Unmutes the specified user"""
        mute_role_name = read_data_entry(ctx.guild.id, "mute-role")
        mute_role = discord.utils.get(ctx.guild.roles, name=mute_role_name)
        if mute_role is None:
            await ctx.send("I could not find any role named `{}`".format(mute_role_name))
            return
        try:
            await user.remove_roles(user, mute_role, reason="Unmuted by {}".format(ctx.author))
            await ctx.send("Successfully unmuted `{}`".format(user))
        except discord.errors.Forbidden:
            if mute_role.position == ctx.me.top_role.position:
                await ctx.send("I cannot remove the mute role users as it's my highest role, y u mute me like dis")
            elif mute_role.position > ctx.me.top_role.position:
                await ctx.send("I cannot unmute users as the mute role is higher than my highest role")
            else:
                await ctx.send("I do not have the `Manage Roles` permission")

    @checks.server_mod_or_perms(manage_messages=True)
    @commands.command()
    async def prune(self, ctx, amount:int):
        """Prunes the specified amount of messages (you can also prune messages from a specific user too)"""
        try:
            await ctx.message.delete()
        except discord.errors.Forbidden:
            await ctx.send("I do not have the `Manage Messages` permission")
            return
        deleted = await ctx.channel.purge(limit=amount)
        deleted_message = await ctx.send("{} Deleted {} messages".format(ctx.author.mention, len(deleted)))
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
            message = await ctx.channel.get_message(id)
        except discord.errors.NotFound:
            await ctx.send("No message could be found in this channel with an ID of `{}`".format(id))
            return
        try:
            await message.pin()
        except discord.errors.Forbidden:
            await ctx.send("I do not have the `Manage Messages` permission")

    @checks.server_mod_or_perms(manage_messages=True)
    @commands.command()
    async def unpin(self, ctx, id:int):
        """Unpins the message with the specified ID from the channel"""
        pinned_messages = await ctx.channel.pins()
        message = discord.utils.get(pinned_messages, id=id)
        if message is None:
            await ctx.send("No pinned message could be found in this channel with an ID of `{}`".format(id))
            return
        try:
            await message.unpin()
            await ctx.send("Successfully unpinned the message!")
        except discord.errors.Forbidden:
            await ctx.send("I do not have the `Manage Messages` permission")

    @checks.server_mod_or_perms(manage_roles=True)
    @commands.command()
    async def addrole(self, ctx, user:discord.Member, *, name:str):
        """Adds the specified role to the specified user"""
        role = discord.utils.get(ctx.guild.roles, name=name)
        if role is None:
            await ctx.send("No role with the name of `{}` was found on this server".format(name))
            return
        try:
            await user.add_roles(role, reason="The role \"test\" was added by {}".format(role.name, ctx.author))
            await ctx.send("Successfully added the `{}` role to `{}`".format(name, user))
        except discord.errors.Forbidden:
            if role.position == ctx.me.top_role.position:
                await ctx.send("I cannot add my highest role to users")
            elif role.position > ctx.me.top_role.position:
                await ctx.send("I cannot add that role to users as it is higher than my highest role")
            else:
                await ctx.send("I do not have the `Manage Roles` permission")

    @checks.server_mod_or_perms(manage_roles=True)
    @commands.command()
    async def removerole(self, ctx, user:discord.Member, *, name:str):
        """Removes the specified role from the specified user"""
        role = discord.utils.get(ctx.guild.roles, name=name)
        if role is None:
            await ctx.send("No role with the name of `{}` was found on this server".format(name))
            return
        try:
            await user.remove_roles(role, reason="The role \"{}\" was removed by {}".format(role.name, ctx.author))
            await ctx.send("Successfully removed the `{}` role from `{}`".format(name, user))
        except discord.errors.Forbidden:
            if role.position == ctx.me.top_role.position:
                await ctx.send("I cannot remove my highest role from users")
            elif role.position > ctx.me.top_role.position:
                await ctx.send("I cannot remove that role from users as it is higher than my highest role")
            else:
                await ctx.send("I do not have the `Manage Roles` permission")

    @checks.server_mod_or_perms(manage_roles=True)
    @commands.command()
    async def createrole(self, ctx, *, name:str):
        """Creates a role with the specified name"""
        try:
            await ctx.guild.create_role(name=name, reason="Created by {}".format(ctx.author), permissions=ctx.guild.default_role.permissions)
            await ctx.send("Successfully created a role named `{}`".format(name))
        except discord.errors.Forbidden:
            await ctx.send("I do not have the `Manage Roles` permission")

    @checks.server_mod_or_perms(manage_roles=True)
    @commands.command()
    async def deleterole(self, ctx, *, name:str):
        """Deletes the role with the specified name"""
        role = discord.utils.get(ctx.guild.roles, name=name)
        if role is None:
            await ctx.send("No role was found on this server with the name of `{}`".format(name))
            return
        try:
            await role.delete(reason="Deleted by {}".format(ctx.author))
            await ctx.send("Successfully deleted the role named `{}`".format(name))
        except discord.errors.Forbidden:
            if role.position == ctx.me.top_role.position:
                await ctx.send("I cannot delete my highest role")
            elif role.position > ctx.me.top_role.position:
                await ctx.send("I cannot delete that role because it is higher than my highest role")
            else:
                await ctx.send("I do not have the `Manage Roles` permission")

    @checks.server_mod_or_perms(manage_roles=True)
    @commands.command()
    async def editrole(self, ctx, type:str, value:str, *, name:str):
        """Edits a role with the specified name"""
        role = discord.utils.get(ctx.guild.roles, name=name)
        if role is None:
            await ctx.send("No role was found on this server with the name of `{}`".format(name))
            return
        if type == "color":
            if value != "remove":
                try:
                    color = discord.Color(value=int(value.strip("#"), 16))
                except:
                    await ctx.send("`{}` is not a valid color. Make sure you are using a hex color! (Ex: #FF0000)".format(value))
                    return
            else:
                color = discord.Color.default()
            try:
                await role.edit(reason="Edited by {}".format(ctx.author), color=color)
                await ctx.send("Successfully edited the role named `{}`".format(name))
            except discord.errors.Forbidden:
                if role.position == ctx.me.top_role.position:
                    await ctx.send("I cannot edit my highest role")
                elif role.position > ctx.me.top_role.position:
                    await ctx.send("I cannot edit that role because it is higher than my highest role")
                else:
                    await ctx.send("I do not have the `Manage Roles` permission")
            except discord.errors.NotFound:
                # Don't ask, for some reason if the role is higher than the bot's highest role it returns a NotFound 404 error
                await ctx.send("That role is higher than my highest role")
        elif type == "permissions":
            try:
                perms = discord.Permissions(permissions=int(value))
            except:
                await ctx.send("`{}` is not a valid permission number! If you need help finding the permission number, then go to <http://creeperseth.com/discordpermcalc> for a permission calculator!".format(value))
                return
            try:
                await role.edit(reason="Edited by {}".format(ctx.author), permissions=perms)
                await ctx.send("Successfully edited the role named `{}`".format(name))
            except discord.errors.Forbidden:
                await ctx.send("I either do not have the `Manage Roles` permission")
            except discord.errors.NotFound:
                await ctx.send("That role is higher than my highest role")
        elif type == "position":
            try:
                pos = int(value)
            except:
                await self.bot.send_message(ctx.channel, "`" + value + "` is not a valid number")
                return
            if pos >= ctx.guild.me.top_role.position:
                await ctx.send("That number is not lower than my highest role's position. My highest role's permission is `{}`".format(ctx.guild.me.top_role.position))
                return
            try:
                if pos <= 0:
                    pos = 1
                await role.edit(reason="Moved by {}".format(ctx.author), position=pos)
                await ctx.send("Successfully edited the role named `{}`".format(name))
            except discord.errors.Forbidden:
                await ctx.send("I do not have the `Manage Roles` permission")
            except discord.errors.NotFound:
                await ctx.send("That role is higher than my highest role")
        elif type == "separate":
            try:
                bool = convert_to_bool(value)
            except ValueError:
                await ctx.send("`{}` is not a valid boolean".format(value))
                return
            try:
                await role.edit(reason="Edited by {}".format(ctx.author), hoist=bool)
                await ctx.send("Successfully edited the role named `{}`".format(name))
            except discord.errors.Forbidden:
                await ctx.send("I do not have the `Manage Roles` permission or that role is not lower than my highest role.")
        elif type == "mentionable":
            try:
                bool = convert_to_bool(value)
            except ValueError:
                await ctx.send("`{}` is not a valid boolean".format(value))
                return
            try:
                await role.edit(reason="Edited by {}".format(ctx.author), mentionable=bool)
                await ctx.send("Successfully edited the role named `{}`".format(name))
            except discord.errors.Forbidden:
                await ctx.send("I do not have the `Manage Roles` permission")
            except discord.errors.NotFound:
                await ctx.send("That role is higher than my highest role")
        else:
            await ctx.send("Invalid type specified, valid types are `color`, `permissions`, `position`, `separate`, and `mentionable`")

    @checks.server_mod_or_perms(manage_roles=True)
    @commands.command()
    async def renamerole(self, ctx, name:str, newname:str):
        """Renames a role with the specified name, be sure to put double quotes (\") around the name and the new name"""
        role = discord.utils.get(ctx.guild.roles, name=name)
        if role is None:
            await ctx.send("No role was found on this server with the name of `{}`".format(name))
            return
        try:
            await role.edit(reason="Renamed by {}".format(ctx.author), name=newname)
            await ctx.send("Successfully renamed the `{}` role to `{}`".format(name, newname))
        except discord.errors.Forbidden:
            if role.position == ctx.me.top_role.position:
                await ctx.send("I cannot rename my highest role")
            elif role.position > ctx.me.top_role.position:
                await ctx.send("I cannot rename that role because it is higher than my highest role")
            else:
                await ctx.send("I do not have the `Manage Roles` permission")

    @checks.server_mod_or_perms(ban_members=True)
    @commands.command()
    async def massban(self, ctx, *, ids:str):
        """Mass bans users by ids (separate ids with spaces)"""
        await ctx.channel.trigger_typing()
        ids = ids.split(" ")
        failed_ids = []
        success = 0
        for id in ids:
            try:
                await self.bot.http.ban(id, ctx.guild.id, delete_message_days=0)
                success += 1
            except:
                failed_ids.append("`{}`".format(id))
        if len(failed_ids) != 0:
            await ctx.send("Failed to ban the following id(s): {}".format(", ".join(ids)))
        await ctx.send("Successfully banned {}/{} users".format(success, len(ids)))

    @checks.server_mod_or_perms(manage_messages=True)
    @commands.command()
    async def removereactions(self, ctx, id:int):
        """Clear reactions from a message"""
        try:
            message = await ctx.channel.get_message(id)
        except discord.errors.NotFound:
            await ctx.send("I could not find a message with an ID of `{}` in this channel".format(id))
            return
        try:
            await message.clear_reactions()
            await ctx.send("Successfully cleared all the reactions from that message")
        except discord.errors.Forbidden:
            await ctx.send("I do not have the `Manage Messages` permission")

def setup(bot):
    bot.add_cog(Moderation(bot))
