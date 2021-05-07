import discord
from discord.ext import commands

import json
import configparser

cfg = configparser.ConfigParser()
cfg.sections()


class infoCommands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # COMMANDS
    @commands.command(help='test')
    async def ping(self, ctx):
        await ctx.send(f'Pong! {round(self.bot.latency * 1000)}ms')


def setup(bot):
    bot.add_cog(infoCommands(bot))
