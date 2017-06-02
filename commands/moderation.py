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
    @commands.command(pass_context=True)
    async def kick(self, ctx, user:discord.Member, *, reason:str=None):
        """Kicks the specified user from the server"""
        if reason is None:
            reason = "No reason was specified"
        try:
            await self.bot.kick(user)
        except discord.errors.Forbidden:
            await self.bot.say("I either do not the `Kick Members` permission or my highest role is not higher than that users highest role.")
            return

    @checks.server_mod_or_perms(ban_members=True)
    @commands.command(pass_context=True)
    async def ban(self, ctx, user:discord.Member, *, reason:str=None):
        """Bans the specified user from the server"""
        if reason is None:
            reason = "No reason was specified"
        try:
            await self.bot.ban(user, delete_message_days=0)
        except discord.errors.Forbidden:
            await self.bot.say("I either do not have the `Ban Members` permission or my highest role is not higher than that users highest role.")
            return
        await self.bot.say("Successfully banned `{}`".format(user))

    @checks.server_mod_or_perms(ban_members=True)
    @commands.command(pass_context=True)
    async def unban(self, ctx, *, username:str):
        """Unbans the user with the specifed name from the server"""
        try:
            banlist = await self.bot.get_bans(ctx.message.server)
        except discord.errors.Forbidden:
            await self.bot.say("I do not have the `Ban Members` permission")
            return
        user = discord.utils.get(banlist, name=username)
        if user is None:
            await self.bot.say("No banned user was found with the username of `{}`".format(username))
            return
        await self.bot.unban(ctx.message.server, user)
        await self.bot.say("Successfully unbanned `{}`".format(user))

    @checks.server_mod_or_perms(ban_members=True)
    @commands.command(pass_context=True)
    async def banid(self, ctx, id:str, *, reason:str=None):
        """Bans the user with the specified id from the server (Useful if the user isn't on the server yet)"""
        if reason is None:
            reason = "No reason was specified"
        try:
            await self.bot.http.ban(id, ctx.message.server.id)
        except discord.errors.HTTPException or discord.errors.NotFound:
            await self.bot.say("No discord user has the id of `{}`".format(id))
            return
        except discord.errors.Forbidden:
            await self.bot.say("I do not have the `Ban Members` permission")
            return
        banlist = await self.bot.get_bans(ctx.message.server)
        user = discord.utils.get(banlist, id=id)
        await self.bot.say("Successfully banned `{}`".format(user))

    @commands.command(pass_context=True)
    async def banlist(self, ctx):
        """Displays the server's banlist"""
        try:
            banlist = await self.bot.get_bans(ctx.message.server)
        except discord.errors.Forbidden:
            await self.bot.say("I do not have the `Ban Members` permission")
            return
        banlist = list(map(str, banlist))
        bancount = len(banlist)
        display_bans = []
        bans = ""
        if bancount == 0:
            bans = "No users are banned from this server"
        else:
            for user in banlist:
                if len(", ".join(display_bans)) < 1800:
                    display_bans.append(user)
                else:
                    bans = ", ".join(display_bans) + "\n... and {} more".format(len(banlist) - len(display_bans))
                    break
        if not bans:
            bans = ", ".join(display_bans)
        await self.bot.say("Total bans: `{}`\n```{}```".format(bancount, bans))

    @checks.server_mod_or_perms()
    @commands.command(pass_context=True)
    async def mute(self, ctx, user:discord.Member, *, reason:str=None):
        """Mutes the specified user"""
        if reason is None:
            reason = "No reason was specified"
        mute_role_name = read_data_entry(ctx.message.server.id, "mute-role")
        mute_role = discord.utils.get(ctx.message.server.roles, name=mute_role_name)
        if mute_role is None:
            await self.bot.say("I could not find any role named `{}`".format(mute_role_name))
            return
        try:
            await self.bot.add_roles(user, mute_role)
            await self.bot.say("Successfully muted `{}`".format(user))
        except discord.errors.Forbidden:
            await self.bot.say("I either do not have the `Manage Roles` permission or my highest role is not higher than the `{}` role".format(mute_role_name))

    @checks.server_mod_or_perms()
    @commands.command(pass_context=True)
    async def unmute(self, ctx, user:discord.Member):
        """Unmutes the specified user"""
        mute_role_name = read_data_entry(ctx.message.server.id, "mute-role")
        mute_role = discord.utils.get(ctx.message.server.roles, name=mute_role_name)
        if mute_role is None:
            await self.bot.say("I could not find any role named `{}`".format(mute_role_name))
            return
        try:
            await self.bot.remove_roles(user, mute_role)
            await self.bot.say("Successfully unmuted `{}`".format(user))
        except discord.errors.Forbidden:
            await self.bot.say("I either do not have the `Manage Roles` permission or my highest role is not higher than the `{}` role".format(mute_role_name))

    @checks.server_mod_or_perms(manage_messages=True)
    @commands.command(pass_context=True)
    async def prune(self, ctx, amount:int, *, user:discord.Member=None):
        """Prunes the specified amount of messages (you can also prune messages from a specific user too)"""
        try:
            await self.bot.delete_message(ctx.message)
        except discord.errors.Forbidden:
            await self.bot.say("I do not have the `Manage Messages` permission")
            return
        if user:
            def is_user(message):
                return message.author == user
            deleted = await self.bot.purge_from(ctx.message.channel, limit=amount, check=is_user)
        else:
            deleted = await self.bot.purge_from(ctx.message.channel, limit=amount)
        deleted_message = await self.bot.say("{} Deleted {} messages".format(ctx.message.author.mention, len(deleted)))
        await asyncio.sleep(10)
        # The try and except pass is so in the event a user prunes again or deletes the prune notification before the bot automatically does it, it will not raise an error
        try:
            await self.bot.delete_message(deleted_message)
        except:
            pass

    @checks.server_mod_or_perms(manage_messages=True)
    @commands.command(pass_context=True)
    async def pin(self, ctx, id:str):
        """Pins the message with the specified ID to the channel"""
        try:
            message = await self.bot.get_message(ctx.message.channel, id)
        except discord.errors.NotFound:
            await self.bot.say("No message could be found in this channel with an ID of `{}`".format(id))
            return
        try:
            await self.bot.pin_message(message)
        except discord.errors.Forbidden:
            await self.bot.say("I do not have the `Manage Messages` permission")

    @checks.server_mod_or_perms(manage_messages=True)
    @commands.command(pass_context=True)
    async def unpin(self, ctx, id:str):
        """Unpins the message with the specified ID from the channel"""
        pinned_messages = await self.bot.pins_from(ctx.message.channel)
        message = discord.utils.get(pinned_messages, id=id)
        if message is None:
            await self.bot.say("No pinned message could be found in this channel with an ID of `{}`".format(id))
            return
        try:
            await self.bot.unpin_message(message)
            await self.bot.say("Successfully unpinned the message!")
        except discord.errors.Forbidden:
            await self.bot.say("I do not have the `Manage Messages` permission")

    @checks.server_mod_or_perms(manage_roles=True)
    @commands.command(pass_context=True)
    async def addrole(self, ctx, user:discord.Member, *,  name:str):
        """Adds the specified role to the specified user"""
        role = discord.utils.get(ctx.message.server.roles, name=name)
        if role is None:
            await self.bot.say("No role with the name of `{}` was found on this server".format(name))
            return
        try:
            await self.bot.add_roles(user, role)
            await self.bot.say("Successfully added the `{}` role to `{}`".format(name, user))
        except discord.errors.Forbidden:
            await self.bot.say("I either do not have the `Manage Roles` permission or my highest role isn't higher than the `{}` role".format(name))

    @checks.server_mod_or_perms(manage_roles=True)
    @commands.command(pass_context=True)
    async def removerole(self, ctx, user:discord.Member, *, name:str):
        """Removes the specified role from the specified user"""
        role = discord.utils.get(ctx.message.server.roles, name=name)
        if role is None:
            await self.bot.say("No role with the name of `{}` was found on this server".format(name))
            return
        try:
            await self.bot.remove_roles(user, role)
            await self.bot.say("Successfully removed the `{}` role from `{}`".format(name, user))
        except discord.errors.Forbidden:
            await self.bot.say("I either do not have the `Manage Roles` permission or my highest role isn't higher than the `{}` role".format(name))

    @checks.server_mod_or_perms(manage_roles=True)
    @commands.command(pass_context=True)
    async def createrole(self, ctx, *, name:str):
        """Creates a role with the specified name"""
        try:
            await self.bot.create_role(ctx.message.server, name=name)
            await self.bot.say("Successfully created a role named `{}`".format(name))
        except discord.errors.Forbidden:
            await self.bot.say("I do not have the `Manage Roles` permission")

    @checks.server_mod_or_perms(manage_roles=True)
    @commands.command(pass_context=True)
    async def deleterole(self, ctx, *, name:str):
        """Deletes the role with the specified name"""
        role = discord.utils.get(ctx.message.server.roles, name=name)
        if role is None:
            await self.bot.say("No role was found on this server with the name of `{}`".format(name))
            return
        try:
            await self.bot.delete_role(ctx.message.server, role)
            await self.bot.say("Successfully deleted the role named `{}`".format(name))
        except discord.errors.Forbidden:
            await self.bot.say("I do not have the `Manage Roles` permission")

    @checks.server_mod_or_perms(manage_roles=True)
    @commands.command(pass_context=True)
    async def editrole(self, ctx, type:str, value:str, *, name:str):
        """Edits a role with the specified name"""
        role = discord.utils.get(ctx.message.server.roles, name=name)
        if role is None:
            await self.bot.say("No role was found on this server with the name of `{}`".format(name))
            return
        if type == "color":
            if value != "remove":
                try:
                    color = discord.Color(value=int(value.strip("#"), 16))
                except:
                    await self.bot.say("`{}` is not a valid color. Make sure you are using a hex color! (Ex: #FF0000)".format(value))
                    return
            else:
                color = discord.Color.default()
            try:
                await self.bot.edit_role(ctx.message.server, role, color=color)
                await self.bot.say("Successfully edited the role named `{}`".format(name))
            except discord.errors.Forbidden:
                await self.bot.say("I either do not have the `Manage Roles` permission")
            except discord.errors.NotFound:
                # Don't ask, for some reason if the role is higher than the bot's highest role it returns a NotFound 404 error
                await self.bot.say("That role is higher than my highest role")
        elif type == "permissions":
            try:
                perms = discord.Permissions(permissions=int(value))
            except:
                await self.bot.say("`{}` is not a valid permission number! If you need help finding the permission number, then go to <http://creeperseth.com/discordpermcalc> for a permission calculator!".format(value))
                return
            try:
                await self.bot.edit_role(ctx.message.server, role, permissions=perms)
                await self.bot.say("Successfully edited the role named `{}`".format(name))
            except discord.errors.Forbidden:
                await self.bot.say("I either do not have the `Manage Roles` permission")
            except discord.errors.NotFound:
                await self.bot.say("That role is higher than my highest role")
        elif type == "position":
            try:
                pos = int(value)
            except:
                await self.bot.send_message(ctx.message.channel, "`" + value + "` is not a valid number")
                return
            if pos >= ctx.message.server.me.top_role.position:
                await self.bot.say("That number is not lower than my highest role's position. My highest role's permission is `{}`".format(ctx.message.server.me.top_role.position))
                return
            try:
                if pos <= 0:
                    pos = 1
                await self.bot.move_role(ctx.message.server, role, pos)
                await self.bot.say("Successfully edited the role named `{}`".format(name))
            except discord.errors.Forbidden:
                await self.bot.say("I do not have the `Manage Roles` permission")
            except discord.errors.NotFound:
                await self.bot.say("That role is higher than my highest role")
        elif type == "separate":
            try:
                bool = convert_to_bool(value)
            except ValueError:
                await self.bot.say("`{}` is not a valid boolean".format(value))
                return
            try:
                await self.bot.edit_role(ctx.message.server, role, hoist=bool)
                await self.bot.say("Successfully edited the role named `{}`".format(name))
            except discord.errors.Forbidden:
                await self.bot.say("I do not have the `Manage Roles` permission or that role is not lower than my highest role.")
        elif type == "mentionable":
            try:
                bool = convert_to_bool(value)
            except ValueError:
                await self.bot.say("`{}` is not a valid boolean".format(value))
                return
            try:
                await self.bot.edit_role(ctx.message.server, role, mentionable=bool)
                await self.bot.say("Successfully edited the role named `{}`".format(name))
            except discord.errors.Forbidden:
                await self.bot.say("I do not have the `Manage Roles` permission")
            except discord.errors.NotFound:
                await self.bot.say("That role is higher than my highest role")
        else:
            await self.bot.say("Invalid type specified, valid types are `color`, `permissions`, `position`, `separate`, and `mentionable`")

    @checks.server_mod_or_perms(manage_roles=True)
    @commands.command(pass_context=True)
    async def renamerole(self, ctx, name:str, newname:str):
        """Renames a role with the specified name, be sure to put double quotes (\") around the name and the new name"""
        role = discord.utils.get(ctx.message.server.roles, name=name)
        if role is None:
            await self.bot.say("No role was found on this server with the name of `{}`".format(name))
            return
        try:
            await self.bot.edit_role(ctx.message.server, role, name=newname)
            await self.bot.say("Successfully renamed the `{}` role to `{}`".format(name, newname))
        except discord.errors.Forbidden:
            await self.bot.say("I do not have the `Manage Roles` permission")
        except discord.errors.NotFound:
            await self.bot.say("That role is higher than my highest role")

    @checks.server_mod_or_perms(ban_members=True)
    @commands.command(pass_context=True)
    async def massban(self, ctx, *, ids:str):
        """Mass bans users by ids (separate ids with spaces)"""
        await self.bot.send_typing(ctx.message.channel)
        ids = ids.split(" ")
        failed_ids = []
        success = 0
        for id in ids:
            try:
                await self.bot.http.ban(id, ctx.message.server.id)
                success += 1
            except:
                failed_ids.append("`{}`".format(id))
        if len(failed_ids) != 0:
            await self.bot.say("Failed to ban the following id(s): {}".format(", ".join(ids)))
        await self.bot.say("Successfully banned {}/{} users".format(success, len(ids)))

def setup(bot):
    bot.add_cog(Moderation(bot))
