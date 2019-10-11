import time, asyncio, random, collections

import discord
from discord.ext import commands

import settings
from settings import Help

class HelpCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @settings.check_channel()
    @commands.group(name = "help", aliases = ["h", "cmds"], description = "Shows you a list of the commands. You can add arg1 and arg2 optionally to get help on a specific command/subcommand.")
    async def help_group(self, ctx, cmdn : str = "", scmdn : str = ""):
        if cmdn != "": #if person wants help for specific command
            cmdt = cmdn
            if scmdn != "":#subcommands?
                cmdt += " " + scmdn
            cmd = self.bot.get_command(cmdt)
            if cmd: #if it's a real command
                if cmd.description:

                    cmdt = await Help.create_string_names(ctx, cmd)

                    embed = discord.Embed(title = f"**{ctx.author.name}**, \"{cmdt}\"", description = cmd.description + "\n")
                    await settings.send_msg(self, ctx, "", embed = embed)
                    return
            await settings.send_msg(self, ctx, f"**{ctx.author.name}**, that command does not exist!")

            return

        embed = discord.Embed(title = f"**{ctx.author.name}**, list of commands:")
        for c in self.bot.cogs:
            cu = c[0:-3] #remove the Cog in the name
            cmdlist = ""
            #print(c)
            #print(self.bot.get_cog_commands(c))
            for thing in self.bot.get_cog(c).get_commands(): #for things in each cog

                if isinstance(thing, commands.Group):
                    if thing.description: #if it has a global command
                        cmdlist = await Help.add_to_string(ctx, thing, cmdlist)
                    for cmd in thing.commands: #loop through command in the group
                        cmdlist = await Help.add_to_string(ctx, cmd, cmdlist)
                else: #it's a command
                    cmdlist = await Help.add_to_string(ctx, thing, cmdlist)
            if not cmdlist == "":
                cmdlist += "\u200b"
                embed.add_field(name = cu, value = cmdlist, inline = False)
        await settings.send_msg(self, ctx, "", embed = embed)


def setup(bot):
    bot.add_cog(HelpCog(bot))
