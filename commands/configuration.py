from discord.ext import commands
from utils.mysql import *
from utils.tools import *
from utils import checks
from utils.language import Language, lang_list

class Configuration(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @checks.server_admin_or_perms(manage_guild=True)
    @commands.guild_only()
    @commands.command()
    async def config(self, ctx, type:str, *, value:str):
        """Modifies the server's local config"""
        await ctx.channel.trigger_typing()
        if type == "mod-role" or type == "admin-role" or type == "mute-role" or type == "join-role":
            role = by_name_or_id(ctx.guild.roles, value)
            if role is None:
                await ctx.send("Could not find the role `" + value + "`")
                return
            update_data_entry(ctx.guild.id, type, role.id)
            await ctx.send(Language.get("configuration.set_success", ctx).format(type, role.name))
        else:
            await ctx.send(Language.get("configuration.invalid_set_type", ctx).format(type))

    @commands.guild_only()
    @commands.command()
    async def showconfig(self, ctx):
        """Shows the server's configuration"""
        await ctx.channel.trigger_typing()

        mod_role = id_to_name(ctx.guild.roles, read_data_entry(ctx.guild.id, "mod-role"))
        admin_role = id_to_name(ctx.guild.roles, read_data_entry(ctx.guild.id, "admin-role"))
        mute_role = id_to_name(ctx.guild.roles, read_data_entry(ctx.guild.id, "mute-role"))
        join_role = id_to_name(ctx.guild.roles, read_data_entry(ctx.guild.id, "join-role"))

        fields = {Language.get("configuration.mod_role", ctx):mod_role, "Admin Role":admin_role, Language.get("configuration.mute_role", ctx):mute_role, Language.get("configuration.join_role", ctx):join_role}
        embed = make_list_embed(fields)
        embed.title = Language.get("configuration.server_configuration", ctx)
        embed.color = 0xFF0000
        await ctx.send(embed=embed)

    @commands.guild_only()
    @checks.server_admin_or_perms(manage_guild=True)
    @commands.command()
    async def setlanguage(self, ctx, language:str):
        """Sets the bot's language for the server"""
        await ctx.send(Language.set_language(ctx.guild, language))

    @commands.guild_only()
    @commands.command()
    async def languages(self, ctx):
        """Lists the current bot languages"""
        await ctx.send("Current bot languages: " + ", ".join(lang_list))

def setup(bot):
    bot.add_cog(Configuration(bot))
