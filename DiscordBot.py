import discord
from discord.ext import commands, tasks

import asyncio
import json
import configparser
import os

from itertools import cycle

from typing_extensions import TypeAlias

# CREATES A CONFIG PAERSER
cfg = configparser.ConfigParser()
cfg.sections()

# CREATES THE BOT AND SET HIS STATUS
bot = commands.Bot(command_prefix="bot.")
status = cycle(['Im on da tube', 'I AM KUHL', 'twutch'])

# TESTS FOR USER WHO SENT THE MESSAGE
def ist_it_me(ctx):
    return ctx.author.id == 273731884800933888  # SparkOfChaos#8361

# BOT EVENT ON_READY
@bot.event
async def on_ready():
    change_status.start()
    print('ready')

# CHANGES BOT STATUS EVERY 10 SECS
@tasks.loop(seconds=10)
async def change_status():
    await bot.change_presence(activity=discord.Streaming(name=next(status), url='https://twitch.tv/spark0fchaos'))

# COMMANDS FOR LOADING AND UNLOADING COGS
@bot.command()
@commands.check(ist_it_me)
async def load(ctx, extension):
    bot.load_extension(f'cogs.{extension}')
    await ctx.send(f'successfully loaded {extension}')

@bot.command()
@commands.check(ist_it_me)
async def unload(ctx, extension):
    bot.unload_extension(f'cogs.{extension}')
    await ctx.send(f'successfully unloaded {extension}')

@bot.command()
@commands.check(ist_it_me)
async def reload(ctx, extension):
    bot.unload_extension(f'cogs.{extension}')
    bot.load_extension(f'cogs.{extension}')
    await ctx.send(f'successfully reloaded {extension}')

# LOADS COGS ON BOT STARTUP
for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')

# RUNS THE BOT
bot.run("ODM1NDk1ODg2NzY2NzM1Mzcw.YIQSLg.S20ieFv3RFN_TfP3lXS4t_ar5VE")
