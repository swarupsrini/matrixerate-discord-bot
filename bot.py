import sys, traceback

import discord
from discord.ext import commands

import settings

initial_extensions = [
    "bot-gen",
    "bot-help",
    "bot-errors",

    "bot-roles",
    "bot-money",
]

bot = commands.Bot(command_prefix = "-", case_insensitive = True)
bot.remove_command("help")

if __name__ == "__main__":
    for extension in initial_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            #print(f"Failed to load extension {extension}.", file = sys.stderr)
            traceback.print_exc()

@bot.event
async def on_ready():
    print(bot.user.name)
    print(f"\nLogged in as: {bot.user.name} - {bot.user.id}\ndiscord.py version: {discord.__version__}\n")
    await bot.change_presence(activity = discord.Game(name="with the matrix"))
    print("Successfully logged in and booted...!")

bot.run("NjE3MjQwNTMxNjQ2NDE0ODQ4.XZ6-RA.25BAY_eiS1fNInIwTDaxiC_JIBw", bot=True, reconnect=True)
