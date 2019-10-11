import time, asyncio, random, collections

import discord
from discord.ext import commands

import settings
from settings import Money

class MoneyCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @settings.check_channel()
    @commands.group(name = "money", aliases = ["m"], invoke_without_command = False)
    async def money_group(self, ctx):
        pass

    @money_group.command(aliases = ["bal", "b"], description = "Displays the amount of money you have.")
    async def balance(self, ctx):
        id = ctx.author.id
        val = Money.get_data(id)
        await settings.send_msg(self, ctx, f"**{ctx.author.name}**, you have a balance of **{val}** {Money.currency}!")

    @money_group.command()
    async def give(self, ctx):
        Money.save_data(ctx.author.id, 100)

    @money_group.command(aliases = ["g"], description = "Gamble an amount of money that randomly gives/reduces money. arg1 is the amount you may lose/gain.")
    async def gamble(self, ctx, amt : str = ""):
        id = ctx.author.id
        if not amt.isdigit():
            await settings.send_msg(self, ctx, f"**{ctx.author.name}**, that is not a valid amount!")
            return
        amt = int(amt)
        amtbank = Money.get_data(id)
        #print(amt)
        #print(amtbank)
        if amt > amtbank:
            await settings.send_msg(self, ctx, f"**{ctx.author.name}**, you cannot gamble more than you have!")
            return
        newamt = random.randint(-amt, amt)
        gainrec = "gained" if newamt > 0 else "lost"
        Money.save_data(id, amtbank + newamt)
        await settings.send_msg(self, ctx, f"**{ctx.author.name}**, you {gainrec} {abs(newamt)} {Money.currency}!")

def setup(bot):
    bot.add_cog(MoneyCog(bot))
