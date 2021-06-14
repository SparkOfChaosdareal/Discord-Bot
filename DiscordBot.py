import discord
from discord.ext import commands, tasks

import asyncio
import json
import configparser
import os
import sqlite3

from itertools import cycle

from typing_extensions import TypeAlias

# CREATES A CONFIG PAERSER
cfg = configparser.ConfigParser()
cfg.sections()

# DATABESE SETUP
con = sqlite3.connect('DataBase.db')
c = con.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS Servers (Server_ID INTEGER PRIMAR KEY, Server_Name text)''')
c.execute('''CREATE TABLE IF NOT EXISTS Users (User_ID INTEGER PRIMAR KEY, User_Name text)''')
c.execute('''CREATE TABLE IF NOT EXISTS Is_On_Server (User_ID integer, Server_ID integer)''')
c.execute('''CREATE TABLE IF NOT EXISTS SFX (Sound_ID INTEGER PRIMARY KEY AUTOINCREMENT, Belongs_To_Server integer, Sound_Name text, Is_Public integer , Sound_Path text)''')

# CREATES THE BOT AND SET HIS STATUS
bot = commands.Bot(command_prefix=commands.when_mentioned_or("bot."))
status = cycle(['Im on da tube', 'I AM KUHL', 'twutch'])

def is_admin(ctx):
    return ctx.author.guild_permissions.administrator

# BOT EVENT ON_READY
@bot.event
async def on_ready():
    change_status.start()
    print('ready')

@bot.event
async def on_guild_join(guild: discord.Guild):
    c.execute(f"INSERT INTO Servers (Server_ID, Server_Name) VALUES ('{guild.id}', '{guild.name}')")

# CHANGES BOT STATUS EVERY 10 SECS
@tasks.loop(seconds=10)
async def change_status():
    await bot.change_presence(activity=discord.Streaming(name=next(status), url='https://twitch.tv/spark0fchaos'))

# COMMANDS FOR LOADING AND UNLOADING COGS
@bot.command()
@commands.check(is_admin)
async def load(ctx, extension):
    bot.load_extension(f'cogs.{extension}')
    await ctx.send(f'successfully loaded {extension}')

@bot.command()
@commands.check(is_admin)
async def unload(ctx, extension):
    bot.unload_extension(f'cogs.{extension}')
    await ctx.send(f'successfully unloaded {extension}')

@bot.command(aliases=['r'])
@commands.check(is_admin)
async def reload(ctx, extension):
    bot.unload_extension(f'cogs.{extension}')
    bot.load_extension(f'cogs.{extension}')
    await ctx.send(f'successfully reloaded {extension}')

# LOADS COGS ON BOT STARTUP
for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')

# RUNS THE BOT
bot.run("<BOT TOKEN>")
