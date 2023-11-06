import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv('.env')

intents = discord.Intents.all()

bot = commands.Bot(command_prefix='$', intents=intents)

emoji = '<:bot_box:1171090169257017344>'


@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')


@bot.command(name='hello')
async def ping(ctx):
    await ctx.channel.send(f'Hello {emoji}')


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
        await ctx.send('Fehler: Es fehlen erforderliche Argumente. Format: $add <Zahl1> <Zahl2>')


TOKEN = os.getenv('TOKEN')
bot.run(TOKEN)
