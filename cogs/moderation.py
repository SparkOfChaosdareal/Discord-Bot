import discord
from discord.ext import commands

import json
import configparser

cfg = configparser.ConfigParser()
cfg.sections()

def is_admin(ctx):
    return ctx.author.guild_permissions.administrator

class moderation(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # CLEARS AMOUNT NUMBER OF MESSAGES DEFAULT VALUE = 5
    @commands.command(help='Clears specified amount of Messages | Default is 5')
    @commands.has_permissions(manage_messages=True)
    @commands.check(is_admin)
    async def clear(self, ctx, amount=5):
        await ctx.channel.purge(limit=amount)

def setup(bot):
    bot.add_cog(moderation(bot))
