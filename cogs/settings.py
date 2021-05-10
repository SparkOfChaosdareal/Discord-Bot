import discord
from discord.ext import commands

import json
import configparser

cfg = configparser.ConfigParser()
cfg.sections()

class Settings(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
    """
    # EVENT
    @commands.Cog.listener()
    async def 
    """   
    # ALLOW THE USER TO CHANGE A SPECIFIC CONFIG VALUE
    @commands.command(aliases=['changeconfig', 'change config'], help="change a config value by using this command like *bot.ccfg GIFR catjam true* GIFR is the config u want to change catjam ist the value of this particualer config and true is the value u want to set it to", brief="change the config settings")
    async def ccfg(self, ctx, arg1, arg2, arg3):
        print(arg1)
        print(arg2)
        print(arg3)
        cfg[arg1][arg2] = arg3
        await ctx.channel.send("Changed value " + arg2 + "of group" + arg1 + "to" + arg3)

    # PRINTS ALL THE CONFIG SETTINGS OF A SPECIFIC SECTION
    @commands.command(help="prints the config of the selectet section use this command like *bot.scfg GIFR*")
    async def scfg(self, ctx, arg1):
        for word in cfg[arg1]:
            await ctx.channel.send(word + "=" + cfg[arg1][word])

    # COMANND TO SEE ALL SECTIONS OF THE CONFIG.CFG FILE
    @commands.command(help="prints all sections of the config file")
    async def pcfgsec(self, ctx):
        await ctx.channel.send(cfg.sections(1))
    
        
    
def setup(bot):
    bot.add_cog(Settings(bot))
