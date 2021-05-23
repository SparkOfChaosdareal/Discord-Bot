from contextlib import ContextDecorator
import contextlib
from typing import ContextManager, Type
import discord
from discord.client import Client
from discord.ext import commands
import asyncio
import json
import configparser
import sqlite3

from discord.ext.commands.bot import Bot

cfg = configparser.ConfigParser()
cfg.sections()

con = sqlite3.connect('DataBase.db')
c = con.cursor()

class SFX(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def upload(self, ctx, SoundName):
        if c.execute(f"SELECT Sound_ID FROM SFX WHERE Sound_Name = '{SoundName}' AND Belongs_To_Server = '{ctx.guild.id}'").rowcount == -1:
            # ASK for audio file

            await ctx.channel.send('Upload an Mp3 file (u got 30secs)')
            
            # CHECKS FOR NEXT MESSAGE
            def check(m: discord.Message):
                return m.author == ctx.author and m.channel == ctx.channel


            # WAITS FOR NEXT MESSAGE TO BE UPLOADED
            try:
                mp3message: discord.Message = await self.bot.wait_for(event='message', check=check, timeout=30.0)
            except asyncio.TimeoutError:
                return await ctx.channel.send('Sorry, you took too long.')

            await ctx.channel.send("Do you want your sound to be public? (y/n) (defaults to yes in 30secs)")
            try:
                publicmessage: discord.Message = await self.bot.wait_for(event='message', check=check, timeout=30.0)
            except asyncio.TimeoutError:
                # defualts to public after 30secs
                public = 1
                return
            # If the user post random shit sound still gonna be public
            public = 1
            # checks what the user wants
            if 'y' in publicmessage.content:
                public = 1
                await mp3message.channel.send("Sound gonna be public")
            if 'n' in publicmessage.content:
                public = 0
                await mp3message.channel.send("Sound gonna be private")

            await mp3message.attachments[0].save(f".\Audio\{SoundName}.mp3")
            c.execute(f"INSERT INTO SFX (Belongs_To_Server, Sound_Name, Is_Public, Sound_Path) VALUES ('{ctx.guild.id}', '{SoundName}', {public}, '.\Audio\{SoundName}.mp3')")
            await mp3message.channel.send(f"Sound is now save with the name *{SoundName}*")
            con.commit()

        else:
            # SFX with that name already exists
            await ctx.channel.send(f'Soundeffect with name *{SoundName}* already exists on this server')
        
    @commands.command()
    async def play(self, ctx, SoundName):
        if not ctx.message.author.voice:
            await ctx.send("You gotta be in a Voice Channel to do that shit")
            return

        VoiceChannel = ctx.author.voice.channel
        try:
            VoiceChannel = await VoiceChannel.connect()

        # CATCHIING ERROR THAT CAN OCCUR WHILE JOINING A VOICE
        except discord.Forbidden:
            await ctx.send("Raised error \"403 Forbidden\". Please check if bot has permission to join and speak in voice channel")
            return
        
        except TimeoutError:
            await ctx.send("Bro is just got timeoutet WTF. So eithe me or Discords APi have connection issues rn. Try again later. If this keeps happening pls contact the Bot owner")
            return
        
        except discord.ClientException:
            await ctx.send("Bro im already doing shit")
            return
        
        except Exception as e:
            await ctx.send(
                "Bro idk whta just happend but i cant join ur voice channel. If this keeps happening pls contact my owner.")
            print(f'Error trying to join a VoiceChannel: {e}')
            return

        ###########################
        #DAtabades shit
        ###########################
        try:
            source = discord.FFmpegPCMAudio(f"./Audio/{SoundName}.mp3")

        # MISSING FILE ERROR
        except FileNotFoundError:
            await ctx.send("File not found")
        
        try:
            VoiceChannel.play(source, after=lambda: print("played SFX"))
        # catching most common errors that can occur while playing effects
        except discord.Forbidden:
            await ctx.send("There was issue playing a sound effect. please check if bot has speak permission")
            await VoiceChannel.disconnect()
            return
        
        except TimeoutError:
            await ctx.send("Bro is just got timeoutet WTF. So eithe me or Discords APi have connection issues rn. Try again later. If this keeps happening pls contact the Bot owner")
            await VoiceChannel.disconnect()
            return
        
        except Exception as e:
            await ctx.send(
                "Bro idk whta just happend but i cant join ur voice channel. If this keeps happening pls contact my owner.")
            await VoiceChannel.disconnect()
            print(f'Error trying to play a sound: {e}')
            return

        await ctx.send(f'playing soundeffect {SoundName}')
        while VoiceChannel.is_playing():
            await asyncio.sleep(1)

        VoiceChannel.stop()

        await VoiceChannel.disconnect()

        
    

def setup(bot):
    bot.add_cog(SFX(bot))
