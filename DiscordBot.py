import discord
from discord.ext import commands, tasks

import json
import configparser
import os

from itertools import cycle

cfg = configparser.ConfigParser()
cfg.sections()

status = cycle(['LOOK AT MA YOUTUBE','I AM KUHL', 'LOOK AT MA TWITCH'])

bot = commands.Bot(command_prefix="bot.")

# BOT EVENT ON_READY
@bot.event
async def on_ready():
    print("ready")
    change_status.start()
    

# BOT EVENT CATJAM
@bot.event
async def on_message(self, message):
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
                await message.channel.send('https://tenor.com/view/cat-jam-gif-18110512') 
                break
        catjam.close()
    if 'ping' or 'Ping' in message.content:
        message.channel.send("Pong!")

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

# ALLOW THE USER TO CHANGE A SPECIFIC CONFIG VALUE
@bot.command(aliases=['changeconfig', 'change config'], help="change a config value by using this command like *bot.ccfg GIFR catjam true* GIFR is the config u want to change catjam ist the value of this particualer config and true is the value u want to set it to", brief="change the config settings")
async def ccfg(ctx, arg1, arg2, arg3):
    print(arg1)
    print(arg2)
    print(arg3)
    cfg[arg1][arg2] = arg3
    await ctx.channel.send("Changed value "+ arg2 + "of group" + arg1 + "to" + arg3)

# PRINTS ALL THE CONFIG SETTINGS OF A SPECIFIC SECTION
@bot.command(help="prints the config of the selectet section use this command like *bot.scfg GIFR*")
async def scfg(ctx, arg1):
    for word in cfg[arg1]:
        await ctx.channel.send(word + "=" + cfg[arg1][word])

# COMANND TO SEE ALL SECTIONS OF THE CONFIG.CFG FILE
@bot.command(help="prints all sections of the config file")
async def pcfgsec(ctx, arg):
    await ctx.channel.send(cfg.sections())

# SIMPLE PRINT COMMAND
@bot.command(help="prints out the message you told him to print", brief="prints out ur stupid shit")
async def print(ctx, *args):
    for arg in args:
        await ctx.send(arg)

@tasks.loop(seconds=5)
async def change_status():
    await bot.change_presence(activity=discord.Streaming(name=next(status), url='twitch.tv/spark0fchaos'))

# RUNS THE BOT
bot.run("ODAxNzczNDUwNDY0OTg1MTI4.YAljtg.ykgA-Mv3K2XvQqI8xskGYqR8Njg")
