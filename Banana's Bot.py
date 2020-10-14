import discord
import random
import os
import pyttsx3
import json
from discord.ext import commands, tasks
from itertools import cycle
from discord.utils import get
from random import choice

with open("config.json", "r") as config_file:
    config = json.load(config_file)
    token = config["token"]
    prefix = config["prefix"]
    link = config["link"]

client = commands.Bot(command_prefix = prefix)

@client.event
async def on_ready():
    print("Banana's Bot Is Ready.")

@client.event
async def on_member_join(member):
    print(f'{member} has joined a server.\n')

@client.event
async def on_member_remove(member):
    print(f'{member} has left a server\n')

@client.command()
async def ping(ctx):
    await ctx.send(f'Pong! {round(client.latency * 1000)}ms')

@client.command(name='8ball')
async def _8ball(ctx, *, question):
    responses = ['No Fuck You.', 'Yes.', 'Ask Again Later.', 'No.', 'Hopefully.']
    await ctx.send(f'Question: {question}\nAnswer: {random.choice(responses)}')

@client.command()
async def penis(ctx):
    await ctx.send('https://memegenerator.net/img/instances/52004322.jpg')

@client.command()
@commands.has_permissions(manage_messages = True)
async def clr(ctx, amount=2):
    await ctx.channel.purge(limit=amount)

@client.command()
async def pp(ctx):
    await ctx.send(f'Haha {ctx.author.mention} said pp')

@client.command()
async def meme(ctx):
    memes = ['https://imgur.com/OJvWhW6', 'https://imgur.com/MEBXSIE',
    'https://imgur.com/Rh35vd9', 'https://imgur.com/r7pEkq8',
    'https://imgur.com/Q353o5m', 'https://imgur.com/oXYKJjc',
    'https://imgur.com/hWGS7XD', 'https://imgur.com/akiD7XX',
    'https://imgur.com/0JKlE0Q', 'https://imgur.com/9xvT3j4',
    'https://imgur.com/wq8y0Pv', 'https://imgur.com/oKZR5HE',
    'https://imgur.com/D0tYXtc', 'https://imgur.com/Emfs7kw',
    'https://imgur.com/SQK2m6B', 'https://imgur.com/zDuRLcr',
    'https://imgur.com/VaDNNji', 'https://imgur.com/f4NghNL',
    'https://imgur.com/iShOV9V', 'https://imgur.com/TGWVXzC',
    'https://imgur.com/EXZZhoi', 'https://imgur.com/riyLQyk',
    'https://imgur.com/qhLS7Q3',]
    await ctx.send(f'{random.choice(memes)}')

@client.command(pass_context=True)
async def bored(ctx):
    user = choice(ctx.message.channel.guild.members)
    await ctx.send(f'{ctx.message.author.mention} you should see if {user.mention} can play')

@client.command()
async def bruh(ctx):
    await ctx.send('https://i.redd.it/omalowmgrn541.jpg')

@client.command()
@commands.has_permissions(manage_channels = True)
async def slowmode(ctx, seconds: int):
    await ctx.channel.edit(slowmode_delay=seconds)
    await ctx.send(f"Set the slowmode delay in this channel to {seconds} seconds!")

@client.command()
async def invite(ctx):
    await ctx.author.send(link)
    print(f'Main invite command was run by {ctx.author} in {ctx.guild}')

@client.command()
async def repeat(ctx, *, word_to_repeat):
    await ctx.send(word_to_repeat)
    print(f'{ctx.author} made the bot repeat "{word_to_repeat}" in "{ctx.guild}"\n')

@client.command()
async def say(ctx, *, word_to_say):
    print(f'{ctx.author} made the bot say "{word_to_say}" and the server was "{ctx.guild}"\n')
    speaker = pyttsx3.init()
    rate = speaker.getProperty('rate')
    speaker.setProperty('rate', rate-50)
    speaker.say(word_to_say)
    speaker.runAndWait()
    await ctx.send(f'{ctx.author.mention} I have finished saying {word_to_say}')

@client.command()
async def water(ctx):
    await ctx.send('https://scx2.b-cdn.net/gfx/news/hires/2019/water.jpg')

@client.command()
async def info(ctx):
    await ctx.author.send(f'Hello! I am a discord bot made by Banana#8765.\nJoin the support server! https://discord.gg/6guQaJp')

client.run(token)
