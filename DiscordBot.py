import discord
from discord.ext import commands

import json
import configparser

cfg = configparser.ConfigParser()
cfg.sections()

bot = commands.Bot(command_prefix="bot.")

# BOT EVENT ON_READY
@bot.event
async def on_ready(self):
    print("ready")

# BOT EVENT CATJAM
@bot.event
async def on_message(self, message):
    cfg.read('config.cfg')
    if message.author == bot.user:
        return
    if(cfg['GIF_REACTS']['catjam'] == 'true'):
        with open('catjam.json', 'r') as catjam:
            data = json.load(catjam)
        for word in data:
            if word in message.content:
                await message.channel.send('https://tenor.com/view/cat-jam-gif-18110512') 
                break
        catjam.close()

# ALLOW THE USER TO CHANGE A SPECIFIC CONFIG VALUE
@bot.command(help="change a config value by using this command like *bot.ccfg GIFR catjam true* GIFR is the config u want to change catjam ist the value of this particualer config and true is the value u want to set it to", breif="change the config settings")
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


# RUNS THE BOT
bot.run("ODAxNzczNDUwNDY0OTg1MTI4.YAljtg.ykgA-Mv3K2XvQqI8xskGYqR8Njg")
