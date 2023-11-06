import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import random

load_dotenv('.env')

intents = discord.Intents.all()

bot = commands.Bot(command_prefix='$', intents=intents)

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')


@bot.command(name='hello')
async def ping(ctx):
    await ctx.channel.send(f'Hello')


@bot.command(name='ping', aliases=['PING'])
async def ping(ctx):
    await ctx.channel.send('pong')


@bot.command(name='add', aliases=['ADD', 'aDD', 'Add'])
async def add(ctx, a, b):
    summe = float(a) + float(b)
    await ctx.channel.send(f'{a} + {b} = {summe}')


@add.error
async def add_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Fehler: Es fehlen erforderliche Argumente. Format: **$add <Zahl1> <Zahl2>**')


@bot.command(name='münzwurf', aliases=['Münzwurf', 'MÜNZWURF'])
async def muenzwurf(ctx, wahl):
    await ctx.channel.send(f'Münze wird geworfen...')
    zahl = random.randint(0, 1)
    if zahl == 0:
        result = 'Kopf'
        await ctx.channel.send(f':coin:')
    else:
        result = 'Zahl'
        await ctx.channel.send(f':100:')

    if wahl == result:
        await ctx.channel.send(f'{ctx.author.mention} hat gewonnen!')
    else:
        await ctx.channel.send(f'{ctx.author.mention} hat verloren!')


@muenzwurf.error
async def muenzwurf_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Fehler: Es fehlen erforderliche Argumente. Format: **$münzwurf <Kopf/Zahl>**')


TOKEN = os.getenv('TOKEN')
bot.run(TOKEN)
