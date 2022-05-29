#	CHUNCHUNMARU's music bot
from typing import AsyncContextManager
from unicodedata import category
import discord
from discord.ext import commands, tasks
from random import choice
from ffmpeg import YTDLSource
from dotenv import load_dotenv
from os import getenv
load_dotenv('.env')

# Change only the no_category default string of help command
help_command = commands.DefaultHelpCommand(no_category = 'Commands')
client = commands.Bot(command_prefix='>',help_command = help_command)



#   EVENTS
#       Feedback if the bot is working or not.
@client.event
async def on_ready():
	change_status.start()
	print('Bot is Online!')

#       Change status every 20s.
status = ['& Jamming', ' & Vibing', 'Music']
@tasks.loop(seconds=20)
async def change_status():
	await client.change_presence(activity=discord.Game(choice(status)))

#       Intrduce bot on member join.
@client.event
async def on_member_join(member):
    channel = discord.utils.get(member.guild.channels, name='general')
    await channel.send(f'Welcome {member.mention}!  Ready to jam out? See `>help` command for details!')

#   COMMANDS - user triggered events
#       Return latency of bot
@client.command(name='ping', help='This command returns the latency.', category='Tools')
async def ping(ctx):
	await ctx.send(f'**Pong!** Latency: {round(client.latency * 1000)}ms')

#       The bot greets you
file_open = open("responses.txt","r")
responses= file_open.readlines()
file_open.close()
@client.command(name='hello', help='This command returns a random reply.', category='Tools')
async def hello(ctx):
	await ctx.send(choice(responses))

#       Prints the credits
@client.command(name='credits', help='This command returns the credits.')
async def credits(ctx):
	await ctx.send('Made by: CHUNCHUNMARU')
	await ctx.send('Last updated: 29/05/22 : 11:52')

#       Prints the rules of the server
file_open = open("rules.txt","r")
rules= file_open.readlines()
file_open.close()
@client.command(name='rule',help='This command prints the rules of the server.')
async def rule(ctx):
    for u in rules:
        await ctx.send(u)

#@client.command(name='play', help='This command plays music.')
#async def play(ctx, url):
#    if not ctx.message.author.voice:
#        await ctx.send('You are not connected to a voice channel.')
#        return
#    elif ctx.voice_client is not None:
#        await ctx.voice_client.move_to(ctx.message.author.voice.channel)
#    else:
#        channel = ctx.message.author.voice.channel
#        await channel.connect()
#
#    server = ctx.message.guild
#    voice_channel = server.voice_client
#
#    async with ctx.typing():
#        player = await YTDLSource.from_url(url, loop=client.loop)
#        voice_channel.play(player, after=lambda e: print('Player error: %s' % e) if e else None)
#   
#    await ctx.send('**Now playing:** {}'.format(player.title))
#
#@client.command(name='stop', help='This command stops music and makes the bot leave voice channel.')
#async def stop(ctx):
#    await ctx.voice_client.disconnect()

#@client.command(name='pause', help='This command pause music.')
#async def pause(ctx):
#	await ctx.voice_client.pause()
#
#@client.command(name='resume', help='This command resume music.')
#async def resume(ctx):
#	await ctx.voice_client.resume()

#@client.command(name='test', help='')
#async def test(ctx):
#	print(ctx.voice_channel, ctx.message.author.voice)
client.run(getenv("TOKEN"))	
