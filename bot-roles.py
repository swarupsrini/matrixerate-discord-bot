import time, asyncio, random, collections

import discord
from discord.ext import commands

import settings
from settings import Roles

class RolesCog:
    def __init__(self, bot):
        self.bot = bot


    @settings.check_channel()
    @commands.group(name = "roles", aliases = ["r"], invoke_without_command = False)
    async def role_group(self, ctx):
        pass

    @role_group.command(aliases = ["r"], description = "Gives/removes a role from the available roles. arg1 specifies the role to give/remove.")
    async def role(self, ctx, rname : str = ""):
        roleop = discord.utils.get(ctx.guild.roles, name = rname)
        if roleop and rname in Roles.roles[ctx.guild.id]:
            if not roleop in ctx.author.roles:
                msg = await settings.send_msg(self, ctx, f"**{ctx.author.name}**, searching the available roles, please wait...")
                for r in Roles.roles[ctx.guild.id]:
                    r = discord.utils.get(ctx.guild.roles, name = r)
                    await ctx.author.remove_roles(r, reason = "Requested replacement.")
                await ctx.author.add_roles(roleop, reason = "Requested by user.")
                await msg.edit(content = f"**{ctx.author.name}**, you have been given the {roleop.name} role.")
            else:
                await ctx.author.remove_roles(roleop, reason = "Requested by user.")
                await settings.send_msg(self, ctx, f"**{ctx.author.name}**, you have removed the {roleop.name} role.")

    @role_group.command(aliases = ["l"], description = "Displayes available roles to role.")
    async def list(self, ctx):
        rolestr = ""
        #print(Roles.roles)
        #print(Roles.roles[ctx.guild.id])
        for a in Roles.roles[ctx.guild.id]:
            #print(a)
            rolestr += (a + "\n")
        embed = discord.Embed(title = f"**{ctx.author.name}**, list of roles:", description = f"```\n{rolestr}```")
        await settings.send_msg(self, ctx, "", embed = embed)
        #await settings.send_msg(self, ctx, f"**{ctx.author.name}**, list of roles:\n```\n{rolestr}```")

    @role_group.command(aliases = ["lo"], description = "Loads in the roles from the saved storage.")
    @commands.has_permissions(administrator = True)
    async def load(self, ctx):
        Roles.load_roles(ctx)

    @role_group.command(aliases = ["re"], description = "Resets the available roles to none.")
    @commands.has_permissions(administrator = True)
    async def reset(self, ctx):
        Roles.roles[ctx.guild.id] = []
        Roles.save_roles()

    @role_group.command(aliases = ["e"], description = "Edits the available roles. arg1 can be \"add\" or \"remove\" and arg2 is the role to add/remove. ")
    @commands.has_permissions(administrator = True)
    async def edit(self, ctx, edittype : str = "" , rname : str = ""):
        roleop = discord.utils.get(ctx.guild.roles, name = rname)
        if not roleop:
            await settings.send_msg(self, ctx, f"**{ctx.author.name}**, {rname} is not a valid role!")
            return
        if edittype == "add":
            if not rname in Roles.roles[ctx.guild.id]:
                Roles.roles[ctx.guild.id].append(rname)
                await settings.send_msg(self, ctx, f"**{ctx.author.name}**, added {rname} to the available roles.")
        elif edittype == "remove":
            if rname in Roles.roles[ctx.guild.id]:
                Roles.roles[ctx.guild.id].remove(rname)
                await settings.send_msg(self, ctx, f"**{ctx.author.name}**, removed {rname} from the available roles.")
        Roles.save_roles()


def setup(bot):
    bot.add_cog(RolesCog(bot))
