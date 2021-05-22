import discord
from discord.ext import commands

import json
import configparser

import mysql.connector  # https://www.w3schools.com/python/python_mysql_getstarted.asp

cfg = configparser.ConfigParser()
cfg.sections()

class SFX(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def upload(self, ctx, SoundName):
        print('a')

    

def setup(bot):
    bot.add_cog(SFX(bot))
