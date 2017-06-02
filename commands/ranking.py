import traceback

from discord.ext import commands
from utils.ranking import *
from utils.tools import *

class Ranking():
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def rank(self, ctx, user:discord.Member=None):
        """Gets your ranking card for you or the specified user"""
        await self.bot.send_typing(ctx.message.channel)
        if not read_data_entry(ctx.message.server.id, "enable-ranking"):
            await self.bot.say("The ranking system is disabled on this server.")
            return
        if user is None:
            user = ctx.message.author
        if user.bot:
            await self.bot.say("Bots can not use the ranking system!")
            return
        data = get_rank_data(user, ctx.message.server)
        fields = {"Level":data["level"], "XP":"{}/{}".format(data["xp"], data["xpneeded"])}
        embed = make_list_embed(fields)
        embed.title = "Ranking card for {}".format(user)
        embed.color = 0xFF0000
        await self.bot.say(embed=embed)

    @commands.command(pass_context=True)
    async def rankuproles(self, ctx):
        """Gets the list of roles you can get when you reach a certain level"""
        await self.bot.send_typing(ctx.message.channel)
        if not read_data_entry(ctx.message.server.id, "enable-ranking"):
            await self.bot.say("The ranking system is disabled on this server.")
            return
        data = get_rankup_roles(ctx.message.server)
        if len(data) == 0:
            await self.bot.say("This server has no rank up roles.")
            return
        await self.bot.say(xl.format("\n".join(data)))

    @commands.command(pass_context=True)
    async def addrankuprole(self, ctx, level:int, *, role:discord.Role):
        """Adds a role to be added when a user reaches a certain level"""
        await self.bot.send_typing(ctx.message.channel)
        if not read_data_entry(ctx.message.server.id, "enable-ranking"):
            await self.bot.say("The ranking system is disabled on this server.")
            return
        if not ctx.message.author.server_permissions.manage_roles:
            await self.bot.say("You need the `Manage Roles` permission in order to use this command.")
            return
        data = get_rankup_role_dict(ctx.message.server)
        data[level] = role.id
        set_rankup_roles(ctx.message.server, data)
        await self.bot.say("Successfully set the `{}` role to be added when a user reaches level **{}**".format(role.name, level))

    @commands.command(pass_context=True)
    async def removerankuprole(self, ctx, level:int):
        """Removes a role from being added when a user reaches a certain level"""
        await self.bot.send_typing(ctx.message.channel)
        if not read_data_entry(ctx.message.server.id, "enable-ranking"):
            await self.bot.say("The ranking system is disabled on this server.")
            return
        if not ctx.message.author.server_permissions.manage_roles:
            await self.bot.say("You need the `Manage Roles` permission in order to use this command.")
            return
        data = get_rankup_role_dict(ctx.message.server)
        del data[level]
        set_rankup_roles(ctx.message.server, data)
        await self.bot.say("Successfully removed the role that was to be set when a user reaches level **{}**".format(level))

    @commands.command(pass_context=True)
    async def topranked(self, ctx):
        """Gets the top 10 highest ranked users on the server"""
        await self.bot.send_typing(ctx.message.channel)
        if not read_data_entry(ctx.message.server.id, "enable-ranking"):
            await self.bot.say("The ranking system is disabled on this server.")
            return
        members = get_user_ranks(ctx.message.server)
        ranks = []
        pos = 1
        for member in sorted(members, key=lambda e: ((e["level"] * 1000) + e["xp"]), reverse=True)[:10]:
            user = discord.utils.get(ctx.message.server.members, id=member["userid"])
            total_xp = member["xp"] + (member["level"] * 1000)
            ranks.append("{}. {}: Level {} ({} total XP)".format(pos, user.name, member["level"], total_xp))
            pos += 1
        await self.bot.say("```{}```".format("\n\n".join(ranks)))

def setup(bot):
    bot.add_cog(Ranking(bot))
