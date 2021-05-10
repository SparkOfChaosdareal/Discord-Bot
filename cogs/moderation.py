import discord
from discord.ext import commands

import json
import configparser

cfg = configparser.ConfigParser()
cfg.sections()

class moderation(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # COMMANDS
    # CLEARS AMOUNT NUMBER OF MESSAGES DEFAULT VALUE = 5
    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount=5):
        await ctx.channel.purge(limit=amount)

def setup(bot):
    bot.add_cog(moderation(bot))
