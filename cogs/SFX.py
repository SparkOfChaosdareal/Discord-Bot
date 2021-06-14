from contextlib import ContextDecorator
import contextlib
from typing import ContextManager, List, Type
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

            await mp3message.attachments[0].save(f".\Audio\{ctx.guild.id}\{SoundName}.mp3")
            c.execute(f"INSERT INTO SFX (Belongs_To_Server, Sound_Name, Is_Public, Sound_Path) VALUES ('{ctx.guild.id}', '{SoundName}', {public}, '.\Audio\{ctx.guild.id}\{SoundName}.mp3')")
            await mp3message.channel.send(f"Sound is now save with the name *{SoundName}*")
            con.commit()

        else:
            # SFX with that name already exists
            await ctx.channel.send(f'Soundeffect with name *{SoundName}* already exists on this server')

        con.close()
        
    @commands.command()
    async def play(self, ctx, SoundName):
        BotVoice: discord.VoiceChannel = discord.utils.get(
            self.bot.voice_clients, guild=ctx.guild)
        if ctx.voice_client.is_playing():
            print("Voice is Playing")
            ctx.voice_client.stop()

        if BotVoice == None:
            print("Bot is not in a Channel")
            if ctx.author.voice:
                print("connect to author voice channel")
                await ctx.author.voice.channel.connect()
            else:
                await ctx.send("You are not connected to a voice channel.")
                raise commands.CommandError(
                    "Author not connected to a voice channel.")
        elif ctx.author.voice:
            print("Author and bot are connected")
            if BotVoice == ctx.author.voice.channel:
                print("author and Bot in same channel")
            else:
                print("move Bot to author voicechannel")
                await ctx.voice_client.move_to(ctx.author.voice.channel)
        else:
            await ctx.send("You are not connected to a voice channel.")
            raise commands.CommandError(
                "Author not connected to a voice channel.")
        
        
        
        
        if SoundName.isdecimal():
            SearchResult = c.execute(f"SELECT Sound_Path, Sound_Name FROM SFX WHERE Sound_ID = {SoundName}")
            if not SearchResult.rowcount == 0:
                # IF THE SQL REQUEST HAS A RESULT
                List = SearchResult.fetchall()
                x = List[0]
                SoundPath = "./" + x[0][2:7] + "/" + x[0][8:]
                _SoundName = x[1][1:-2]
                source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(SoundPath))
                ctx.voice_client.play(source, after=lambda e: print(
                    f'Player error: {e}') if e else None)

                await ctx.send(f'Now playing: **{_SoundName}** with ID {SoundName}')
                con.close()
                return
        elif type(SoundName) == str:
            source = discord.PCMVolumeTransformer(
                discord.FFmpegPCMAudio(f"./Audio/{ctx.guild.id}/{SoundName}.mp3"))
            ctx.voice_client.play(source, after=lambda e: print(
                f'Player error: {e}') if e else None)

            await ctx.send(f'Now playing: **{SoundName}**')
            con.close()
            return

                



    @commands.command(aliases=['Search', 's'])
    async def search(self, ctx, SearchTerm):
        SearchResult = c.execute(
            f"SELECT Sound_ID, Sound_Name FROM SFX WHERE Sound_Name LIKE '%{SearchTerm}%S' AND Is_Public = 1 UNION SELECT Sound_ID, Sound_Name FROM SFX WHERE Sound_Name LIKE '%{SearchTerm}%' AND Belongs_To_Server = {ctx.guild.id}")
        #print (SearchResult.fetchall())
        await ctx.channel.send(SearchResult.fetchall())
        con.close()
    
    @commands.command(aliases=['List', 'l'])
    async def list(self, ctx):
        SearchResult = c.execute(
            f"SELECT Sound_ID, Sound_Name, Is_Public FROM SFX WHERE Belongs_To_Server = {ctx.guild.id}")
        #print (SearchResult.fetchall())
        await ctx.channel.send(SearchResult.fetchall())
        con.close()

    @commands.command(aliases=['publicity', 'public'], help = 'Change publicity of Server Sound Effekt with SoundID to either Public(1) or Private(0)')
    async def change_privacy(self, ctx, SoundID, Public_):
        if not c.execute(f"SELECT Sound_ID FROM SFX WHERE Sound_ID = '{SoundID}' AND Belongs_To_Server = {ctx.guild.id}").rowcount == -1:
            c.execute(f"UPDATE SFX SET Is_Public = {Public_} WHERE Sound_ID = {SoundID}")
            con.commit()
            await ctx.channel.send(f"Updated privacy of SoundEffekt {SoundID} to {Public_} (0 = private / 1 = public)")
        else:
            await ctx.channel.send(f"Sry there's no Sound with the ID {SoundID} that Belongs to this server")
        con.close()

    @commands.command()
    async def join(self, ctx, *, channel: discord.VoiceChannel = None):
        """Joins a voice channel"""

        # NO CHANNEL GIVEN AND USER IS IN A VOICE CHANNEL
        if channel is None and ctx.author.voice.channel is not None:
            voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild) # GETS THE AUDIO CHANNEL THE BOT IS IN
            if voice == None:
                # IF THE BOT IS NOT IN A VOICE CHANNEL
                return await ctx.author.voice.channel.connect()
            else:
                # IF THE BOT IS IN A VOICE CHANNEL
                return await ctx.voice_client.move_to(ctx.author.voice.channel)

        if ctx.voice_client is not None:
            return await ctx.voice_client.move_to(channel)

        await channel.connect()
    
    @commands.command()
    async def volume(self, ctx, volume: int):
        """Changes the player's volume"""

        if ctx.voice_client is None:
            return await ctx.send("Not connected to a voice channel.")
        
        self.bot.PCMVolumeTransformer = volume / 100
        await ctx.send(f"Changed volume to {volume}%")

    @commands.command()
    async def stop(self, ctx):
        """Stops and disconnects the bot from voice"""

        await ctx.voice_client.disconnect()
    
    @upload.before_invoke
    @play.before_invoke
    @change_privacy.before_invoke
    @list.before_invoke
    @search.before_invoke
    async def build_database_connection(self, ctx):
        global con
        global c
        con = sqlite3.connect('DataBase.db')
        c = con.cursor()
        return con, c
        

def setup(bot):
    bot.add_cog(SFX(bot))
