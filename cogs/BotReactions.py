import discord
from discord.ext import commands

import json
import configparser

cfg = configparser.ConfigParser()
cfg.sections()


class BotReactions(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    """ # EVENTS
    @commands.Cog.listener()
    async def on_message(self, message):
        cfg.read('config.cfg')
        # RETURN IF MESSAGE WAS SEND BY BOT
        if message.author == self.bot.user:
            return
        # PUT A CATJAM GIF IN CHAT IF CATJAM IST SET TRUE IN CFG AND MESSAGE CONTAINS WORD FROM CATJAM.JSON
        if cfg['GIFR']['catjam'] == "true":
            with open('catjam.json', 'r', encoding="utf8") as catjam:
                data = json.load(catjam)
            for word in data:
                if word in message.content:
                    await message.channel.send('*isert catjam gif here*')
                    break
            catjam.close()
        if 'ping' in message.content or 'Ping' in message.content:
            await message.channel.send("Pong!")
 """
    @commands.Cog.listener()
    async def on_member_remove(member):
        print(f'{member} has left a server')

    # COMMANDS
    #@commands.command(help='test')
    #async def


def setup(bot):
    bot.add_cog(BotReactions(bot))
