import sys, traceback

import discord
from discord.ext import commands

import settings

class ErrorsCog:
    def __init__(self, bot):
        self.bot = bot

    async def on_command_error(self, ctx, error):
        ignored = (settings.ignored_exceptions)

        #if isinstance(error, ignored):
        #    print("error ignored: " + error)
        #    return

        print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)


def setup(bot):
    bot.add_cog(ErrorsCog(bot))
