import discord
from discord.ext import commands, tasks

import asyncio
import json
import configparser
import os

from itertools import cycle

cfg = configparser.ConfigParser()
cfg.sections()

bot = commands.Bot(command_prefix="bot.")
status = cycle(['LOOK AT MA YOUTUBE', 'I AM KUHL', 'LOOK AT MA TWITCH'])

def ist_it_me(ctx):
    return ctx.author.id == 273731884800933888

# BOT EVENT ON_READY
@bot.event
async def on_ready():
    change_status.start()
    print('ready')
    

# BOT EVENT CATJAM
@bot.event
async def on_message(message):
    cfg.read('config.cfg')
    # RETURN IF MESSAGE WAS SEND BY BOT
    if message.author == bot.user:
        return
    # PUT A CATJAM GIF IN CHAT IF CATJAM IST SET TRUE IN CFG AND MESSAGE CONTAINS WORD FROM CATJAM.JSON
    if(cfg['GIFR']['catjam'] == 'true'):
        with open('catjam.json', 'r') as catjam:
            data = json.load(catjam)
        for word in data:
            if word in message.content:
                await message.channel.send('a') 
                break
        catjam.close()
    #if 'ping' or 'Ping' in message.content:
        #await message.channel.send("Pong!")
"""
# PRINTS TO COLSOLE ON MEMBER REMOVE
@bot.event
async def on_member_remove(member):
    print(f'{member} has left a server')

# SIMPLE PING COMMAND
@bot.command
async def ping(ctx):
    await ctx.sent(f'Pong! {round(bot.latency * 1000)}ms')

# CLEARS AMOUNT NUMBER OF MESSAGES DEFAULT VALUE = 5
@bot.command
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount=5):
    await ctx.channel.purge(limit=amount)

# SIMPLE PRINT COMMAND
@bot.command(help="prints out the message you told him to print", brief="prints out ur stupid shit")
async def print(ctx, *args):
    for arg in args:
        await ctx.send(arg)
"""
@tasks.loop(seconds=10)
async def change_status():
    await bot.change_presence(activity=discord.Streaming(name=next(status), url='https://twitch.tv/spark0fchaos'))
 
@bot.command
@commands.check(ist_it_me)
async def load(ctx, extension):
    bot.load_extension(f'cogs.{extension}')
    await ctx.send(f'successfully loaded {extension}')

@bot.command
@commands.check(ist_it_me)
async def unload(ctx, extension):
    bot.unload_extension(f'cogs.{extension}')
    await ctx.send(f'successfully unloaded {extension}')

@bot.command
@commands.check(ist_it_me)
async def reload(ctx, extension):
    bot.unload_extension(f'cogs.{extension}')
    bot.load_extension(f'cogs.{extension}')
    await ctx.send(f'successfully reloaded {extension}')

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')

# RUNS THE BOT
bot.run("ODAxNzczNDUwNDY0OTg1MTI4.YAljtg.ykgA-Mv3K2XvQqI8xskGYqR8Njg")
