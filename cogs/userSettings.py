import discord
from discord.ext import commands

import json
import configparser

cfg = configparser.ConfigParser()
cfg.sections()


class userSettings(commands.Cog):

    def __init__(self, bot):
        self.bot = bot



def setup(bot):
    bot.add_cog(userSettings(bot))
