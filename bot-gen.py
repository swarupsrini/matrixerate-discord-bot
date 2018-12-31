import time, asyncio, random, collections

import discord
from discord.ext import commands

import settings

class GeneralCog:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(description = "Tells you the bot's current ping.")
    @settings.check_channel()
    async def ping(self, ctx):
        await settings.send_msg(self, ctx, f"**{ctx.author.name}**, Pong! {round(self.bot.latency, 5)} seconds")

    @commands.command(aliases = ["cc"], description = "Changes the bot's input/output channel. If arg1 is \"None\", all channels are set for input/output.")
    @commands.has_permissions(administrator = True)
    async def changechannel(self, ctx, none : str = ""):
        if none.lower() == "None":
            settings.channel == None
            await ctx.channel.send(f"**{ctx.author.name}**, changed the command channel to None")
        else:
            settings.channel = ctx.channel
            await settings.channel.send(f"**{ctx.author.name}**, changed the command channel to {settings.channel.name}")

def setup(bot):
    bot.add_cog(GeneralCog(bot))
