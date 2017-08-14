import random

from discord.ext import commands

from utils.economy import *
from utils import checks
from utils.config import Config
from datetime import datetime, timedelta

config = Config()

class Economy():
    def __init__(self, bot):
        self.bot = bot

    #TODO: ADD MORE FUCKING SHIT TO BUY

    @commands.command()
    async def ecostats(self, ctx, user:discord.Member=None):
        """Gets economy stats for you or the specified user"""
        await ctx.channel.trigger_typing()
        if user is None:
            user = ctx.author
        if user.bot:
            await ctx.send("Bots can not use the economy system!")
            return
        eco_data = get_user_economy_data(user)
        fields = {"Balance":format_currency(eco_data["balance"])}
        for key, value in eco_data["data"].items():
            try:
                is_valid = eco_data_defaults[key]
            except KeyError:
                continue
            if key == "lastdailyroses":
                continue
            fields[key.capitalize()] = value
        embed = make_list_embed(fields)
        embed.title = "Economy Stats ({})".format(user)
        embed.color = 0xFF0000
        await ctx.send(embed=embed)

    @commands.command()
    async def pay(self, ctx, user:discord.Member, amount:int):
        """Pays the specified user the specified number of roses"""
        await ctx.channel.trigger_typing()
        if user == ctx.author:
            await ctx.send("You can't pay yourself!")
            return
        if amount < 0:
            await ctx.send("You can not pay users a negative amount of roses!")
            return
        if not can_afford(ctx.author, amount):
            await ctx.send("You do not have enough roses to pay that much!")
            return
        remove_roses(ctx.author, amount)
        add_roses(user, amount)
        await ctx.send("Gave {} {}".format(user.name, format_currency(amount)))

    @commands.command(hidden=True)
    @checks.is_dev()
    async def setbalance(self, ctx, user:discord.Member, amount:int):
        """Sets the specified user's balance"""
        await ctx.channel.trigger_typing()
        if user.bot:
            await ctx.send("Bots can not use the economy system!")
            return
        if amount < 0:
            amount = 0
        set_balance(user, amount)
        await ctx.send("Set {}'s balance to {}".format(user.name, format_currency(amount)))

    @commands.command()
    async def slotmachine(self, ctx):
        """Try your luck at the good ol' slot machine. Costs 2 roses to play. You get 5 roses per straight row"""
        await ctx.channel.trigger_typing()
        if not can_afford(ctx.author, 2):
            await ctx.send(needs_amount(2))
            return
        remove_roses(ctx.author, 2)
        emotes = [":eyes:", ":thinking:", ":rose:"]
        rows = []
        for i in range(3):
            rows.append([random.choice(emotes), random.choice(emotes), random.choice(emotes)])
        wins = 0
        slots = []
        for row in rows:
            slots.append("{} {} {}".format(row[0], row[1], row[2]))
            if row[0] == row[1] and row[0] == row[2]:
                wins += 1
        if wins != 0:
            roses = (5 * wins)
            add_roses(ctx.author, roses)
            slots.append("\nYou've won {}!".format(format_currency(roses)))
        else:
            slots.append("\nYou didn't win anything! Good luck next time!")
        await ctx.send("\n".join(slots))

    @commands.command()
    async def dailyroses(self, ctx):
        """Get your daily roses. You can only run this once every 24 hours."""
        await ctx.channel.trigger_typing()
        now = datetime.now()
        last = get_eco_data_entry(ctx.author, "lastdailyroses")
        if last is not None:
            last = datetime.fromtimestamp(last)
            time_remaining = (last - now).seconds
            if (last - now).total_seconds() > 0:
                second = time_remaining
                minute, second = divmod(second, 60)
                hour, minute = divmod(minute, 60)
                await ctx.send("You have {} hours, {} minutes, and {} seconds remaining until you can use this command again.".format(hour, minute, second))
                return
            wait_time = now + timedelta(hours=24)
            update_eco_data_entry(ctx.author, "lastdailyroses", wait_time.timestamp())
            add_roses(ctx.author, daily_rose_amount)
            await ctx.send("You've been given your daily {} roses!".format(format_currency(daily_rose_amount)))
        else:
            wait_time = now + timedelta(hours=24)
            update_eco_data_entry(ctx.author, "lastdailyroses", wait_time.timestamp())
            add_roses(ctx.author, daily_rose_amount)
            await ctx.send("You've been given your daily {} roses!".format(format_currency(daily_rose_amount)))

    @commands.command(hidden=True)
    @checks.is_dev()
    async def resetdailycooldown(self, ctx, user:discord.Member=None):
        """Resets the daily cooldown for yourself or the specified user"""
        await ctx.channel.trigger_typing()
        if user is None:
            user = ctx.author
        update_eco_data_entry(user, "lastdailyroses", None)
        await ctx.send("Reset the daily cooldown for `{}`".format(user))

    @commands.command()
    async def balance(self, ctx, user:discord.Member=None):
        """Displays your current balance"""
        await ctx.channel.trigger_typing()
        if user is None:
            user = ctx.author
        await ctx.send("{}'s balance is {}".format(user.name, format_currency(get_user_economy_data(user)["balance"])))

    @commands.command()
    async def econotice(self, ctx):
        """A short notice on the new economy system"""
        await ctx.send("".join(open("assets/EcoNotice.txt", mode="r").readlines()))

def setup(bot):
    bot.add_cog(Economy(bot))
