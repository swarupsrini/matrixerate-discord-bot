import asyncio, pickle

import discord
from discord.ext import commands

#General
channel = None

ignored_exceptions = (commands.CheckFailure, commands.CommandNotFound)

async def send_msg(self, ctx, msg, *args, **kwargs):
    if kwargs:
        embed = kwargs["embed"]
    sentmsg = None
    if channel:
        sentmsg = await channel.send(msg) if msg != "" else await channel.send(embed = embed)
    else:
        sentmsg = await ctx.send(msg) if msg != "" else await ctx.send(embed = embed)
    return sentmsg

def check_channel():
    async def fn(ctx):
        if not channel or ctx.channel == channel:
            return True
    return commands.check(fn)

async def cmd_can_run(ctx, cmd):
    try: #see if user has permissions to use command
        await cmd.can_run(ctx)
    except:
        print(f"{ctx.author.name} can't run {cmd.name}, attempting to skip")
        return
    return True

#Helper
class Help:
    #adds in all the aliases of thing to one string and returns it
    async def create_string_names(ctx, thing):
        b = await cmd_can_run(ctx, thing)
        if not b:
            return ""
        name = thing.name
        for alias in thing.aliases:
            name += f"/{alias}"
        for i in range(len(thing.clean_params)):
            name += f" <arg{i+1}>"
        #print(name)
        cmdlist = f"{name}"
        return cmdlist

    #appends the new thing's aliases and description to the string and returns
    async def add_to_string(ctx, thing, cmdlist):
        b = await cmd_can_run(ctx, thing)
        if not b:
            return cmdlist
        cmdlist += "\n"
        name = thing.name
        for alias in thing.aliases:
            name += f"/{alias}"
        for i in range(len(thing.clean_params)):
            name += f" <arg{i+1}>"
        #print(name)
        desc = thing.description
        cmdlist += f"**{name}:** {desc}\n"
        return cmdlist

#Roling
class Roles:
    roles = {}
    filename = "settings/roles_data.txt"

    def save_roles():
        with open(Roles.filename, "r+b") as data_handle:
            #print(Roles.roles)
            pickle.dump(Roles.roles, data_handle, protocol = pickle.HIGHEST_PROTOCOL)

    def load_roles(ctx):
        with open(Roles.filename, "r+b") as data_handle:
            Roles.roles = pickle.load(data_handle)
            #print(Roles.roles)

#Money Game
class Money:
    currency = "Bucks"
    filename = "settings/money_data.txt"

    def get_data(id):
        with open(Money.filename, "r+b") as data_handle:
            data = pickle.load(data_handle)
            return data[id]

    def save_data(id, value):
        with open(Money.filename, "r+b") as data_handle:
            #print("saving: " , {id : value})
            pickle.dump({id : value}, data_handle, protocol = pickle.HIGHEST_PROTOCOL)

    def output_data():
        with open(Money.filename, "r+b") as data_handle:
            data = pickle.load(data_handle)
            #print("output:", data)
