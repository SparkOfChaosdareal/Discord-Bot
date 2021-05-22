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
    @commands.command(aliases=['changeconfig', 'change config', 'ccfg'], help="change cfg like *bot.ccfg GIFR catjam true* GIFR is the config u want to change catjam ist the value of this particualer config and true is the value u want to set it to", brief="change the config settings")
    async def cfgChange(self, ctx, Section, arg, Value):
        cfg.read('config.cfg')
        # with open('No.json', 'r', encoding="utf8") as No:
        #     no = json.load(No)
        # with open('Yes.json', 'r', encoding="utf8") as Yes:
        #     yes = json.load(Yes)
        # if arg3 in no:
        #     cfg[arg1][arg2] = 'false'
        # if arg3 in yes:
        Value2 = str(Value)
        cfg.set(Section, arg, Value2)
        with open('config.cfg', 'w') as configfile:
            cfg.write(configfile)
        await ctx.channel.send("Changed value " + arg + " of group " + Section + " to " + Value)

    # PRINTS ALL THE CONFIG SETTINGS OF A SPECIFIC SECTION
    @commands.command(aliases=['gcfg'],help="shows config group like *bot.scfg GIFR*")
    async def cfgGroup(self, ctx, arg1):
        cfg.read('config.cfg')
        for word in cfg[arg1]:
            await ctx.channel.send(word + " = " + cfg[arg1][word])

    # COMANND TO SEE ALL SECTIONS OF THE CONFIG.CFG FILE
    @commands.command(aliases=['scfg'],help="prints cfg sections")
    async def cfgSections(self, ctx):
        cfg.read('config.cfg')
        print (cfg.sections())
        await ctx.channel.send(cfg.sections())
 
def setup(bot):
    bot.add_cog(Settings(bot))
