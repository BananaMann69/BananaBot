import discord
import random
import os
import pyttsx3
import json
from discord.ext import commands, tasks
from itertools import cycle
from discord.utils import get
import datetime
import asyncio
import time

with open("config.json", "r") as config_file:
    config = json.load(config_file)
    token = config["token"]
    prefix = config["prefix"]
    link = config["link"]
    owner = config["owner"]
    musiclink = config["musiclink"]

client = commands.Bot(command_prefix = prefix)

def banana(ctx):
    return ctx.author.id == 406905188209655808

@client.event
async def on_ready():
    print("Banana's Bot Is Ready.")

@client.event
async def on_member_join(member):
    print(f'{member} has joined a server.\n')

@client.event
async def on_member_remove(member):
    print(f'{member} has left a server\n')

@client.command(help = "Shows client latency.")
async def ping(ctx):
    start = time.perf_counter()
    message = await ctx.send("Ping...")
    end = time.perf_counter()
    duration = (end - start) * 1000
    await message.edit(content='Pong! {:.2f}ms'.format(duration))

@client.command(name='8ball', help = "8ball random response command.")
async def _8ball(ctx, *, question):
    responses = ['No stop asking', 'Yes.', 'Ask again later.', 'No.', 'Hopefully.', 'Bro, shut up.']
    await ctx.send(f'Question: {question}\nAnswer: {random.choice(responses)}')

@client.command(help = "Display penis size for the member specified")
async def penis(ctx, member: discord.Member):
    penissize = ["8=D", '8==D', '8===D', '8====D', '8=====D', '8======D', '8=======D', '8========D', '8========D', '8==========D']
    await ctx.send(f'{member.mention} has ``{random.choice(penissize)}``')

@client.command(help = 'Will delete amount of messages specified.')
@commands.has_permissions(manage_messages = True)
async def clr(ctx, amount=2):
    await ctx.channel.purge(limit=amount)

@client.command(help = 'Haha pp funny.')
async def pp(ctx):
    await ctx.send(f'Haha {ctx.author.mention} said pp')

@client.command(help = 'Will show random meme.')
async def meme(ctx):
    meme = random.choice(os.listdir(r"C:\Users\Eli\Documents\Memes"))
    if meme == "Meme31.png":
        await ctx.send('Mac now supports windows.')
    await ctx.send(file=discord.File(r"C:\Users\Eli\Documents\Memes\\" + meme))

@client.command(help = 'Bruh.')
async def bruh(ctx):
    await ctx.send('https://i.redd.it/omalowmgrn541.jpg')

@client.command(help = 'Will change slowmode delay of channel')
@commands.has_permissions(manage_channels = True)
async def slowmode(ctx, seconds: int):
    await ctx.channel.edit(slowmode_delay=seconds)
    await ctx.send(f"Set the slowmode delay in this channel to {seconds} seconds!")

@client.command(help = 'Will send invite link of bot.')
async def invite(ctx):
    await ctx.author.send(link)
    print(f'Main invite command was run by {ctx.author} in {ctx.guild}')

@client.command(help = 'Will hydrate bot.')
async def water(ctx):
    await ctx.send('https://scx2.b-cdn.net/gfx/news/hires/2019/water.jpg')

@client.command(help = 'Displays info on the bot.')
async def info(ctx):
    await ctx.author.send(f'Hello! I am a discord bot made by <@406905188209655808>.\nJoin the support server!\nhttps://discord.gg/6guQaJp')

@client.command(help = 'Sends the owner of the bot a suggestion for the bot.')
async def suggest(ctx, *, suggestion):
    user = client.get_user(406905188209655808)
    await user.send(f'{ctx.author.mention} suggested {suggestion} from "{ctx.guild}"')
    await ctx.send(f'{ctx.author.mention} I sent {suggestion} to <@406905188209655808> :)')
    print(f'{ctx.author} suggested {suggestion} and the server was "{ctx.guild}".\n')

@client.command(help = 'Insults the member you mention.')
async def insult(ctx, member: discord.Member, target):
    intelligence = [f'Lol "{member.display_name}" has a smooth brain.',
                    f'Lol "{member.display_name}" has a small brain.']
    personality = [f'Lol "{member.display_name}" is a crybaby.',
                   f'Lol "{member.display_name}" gets angry easily.']
    looks = [f'Lol "{member.display_name}" is fucking ugly',
            f'Lol "{member.display_name}" looks like Trump if Joe Biden was Trumps Father.']
    if target=="intelligence":
        await ctx.send(random.choice(intelligence))
    if target=="personality":
        await ctx.send(random.choice(personality))
    if target=="looks":
        await ctx.send(random.choice(looks))
    else:
        await ctx.send(f'Lol {ctx.author.mention} your pretty dumb use ``intelligence``, ``personality``, or ``looks``.')

@insult.error
async def insult_error(ctx, error):
    if isinstance(error, commands.BadArgument):
        await ctx.send('I could not find that member...')
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('You forgot to specify a member.')

@client.command(help = 'Will delete all messages in the channel.')
@commands.has_permissions(manage_messages = True)
async def purge(ctx):
    await ctx.channel.clone()
    await ctx.channel.delete()

@client.command(help = 'Bans the member you specify.')
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason="Unspecified"):
    if not member:
        embed = discord.Embed(
            description=f"**{ctx.author}** Please specify a member",
            color=0xff0000)
        return await ctx.send(embed=embed)

    if member == ctx.author:
        embed = discord.Embed(
            description=f"**{ctx.author}** You cannot ban yourself",
            color=0xff0000)
        return await ctx.send(embed=embed)

    try:
        await member.ban(reason=reason)
        embed = discord.Embed(
            description=f"{member.mention} was banned\nReason: {reason}",
            color=0xff0000)
        return await ctx.send(embed=embed)

    except discord.Forbidden:
        embed = discord.Embed(
            description=f"**{ctx.author}** No permission to ban the member",
            color=0xff0000)
        await ctx.send(embed=embed)
        return await ctx.send(embed=embed)

@client.command(help = 'Will unban the member you specify.')
@commands.has_permissions(ban_members=True)
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split("#")
    for ban_entry in banned_users:
        user = ban_entry.user

        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f'Unbanned {user.mention}')
            return

@unban.error
async def unban_error(ctx, error):
    if isinstance(error, commands.BadArgument):
        await ctx.send('That member is not banned.')
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('You forgot to specify a member.')

@client.command(help = 'Will change the nickname of the user you specify.')
@commands.has_guild_permissions(manage_nicknames = True )
async def nickchange(ctx, member: discord.Member, *, nick):
    await member.edit(nick=nick)

@nickchange.error
async def nickchange_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('You forgot to specify a member.')
    if isinstance(error, commands.BadArgument):
        await ctx.send('Member not found.')

@client.command(help = "Displays amount of member in the server.")
async def members(ctx):
    await ctx.send(f'\"{ctx.guild}\" has `{ctx.guild.member_count}` members, nice!')

@client.command(help = 'Only available to Banana, will shutdown bot.')
@commands.check(banana)
async def shutdown(ctx):
    await ctx.send(':bulb: Shutting down...')
    await client.close()

client.run(token)
