import discord
from discord.ext import commands
from discord import Embed
import os
from dotenv import load_dotenv
import random
from datetime import datetime

load_dotenv('.env')

intents = discord.Intents.all()

bot = commands.Bot(command_prefix='$', intents=intents)


@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')


@bot.event
async def on_voice_state_update(member, before, after):
    if before.channel is None and after.channel is not None:
        print(f'{datetime.now()}: {member.name} jointe Channel \"{after.channel}\"')
    elif before.channel is not None and after.channel is None:
        print(f'{datetime.now()}: {member.name} verließ Channel \"{before.channel}\"')
    else:
        print(f'{datetime.now()}: {member.name} bewegte sich \"{before.channel}\" -> \"{after.channel}\"')


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
        await ctx.send('Fehler: Fehlendes erforderliches Argumente. Format: **$add <Zahl1> <Zahl2>**')


@bot.command(name='münzwurf', aliases=['Münzwurf', 'MÜNZWURF'])
async def muenzwurf(ctx, wahl):
    if wahl != 'Kopf' and wahl != 'Zahl':
        raise commands.BadArgument

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
        await ctx.send('Fehler: Fehlendes erforderliches Argumente. Format: **$münzwurf <Kopf/Zahl>**')
    elif isinstance(error, commands.BadArgument):
        await ctx.send('Fehler: Ungültiges Argument. Format: **$münzwurf <Kopf/Zahl>**')


@bot.command(name='ssp')
async def ssp(ctx, wahl):
    valid_args = ['Schere', 'Stein', 'Papier']
    emojis = [':scissors:', ':rock:', ':newspaper:']
    if wahl not in valid_args:
        raise commands.BadArgument

    user_no = valid_args.index(wahl)

    com_no = random.randint(0, 2)

    await ctx.channel.send(f'{emojis[user_no]} vs {emojis[com_no]}')

    if user_no == 0 and com_no == 2:
        await ctx.channel.send(f'Du hast gewonnen!')
    elif user_no == 2 and com_no == 0:
        await ctx.channel.send(f'Du hast verloren!')
    elif user_no > com_no:
        await ctx.channel.send(f'Du hast gewonnen!')
    elif user_no < com_no:
        await ctx.channel.send(f'Du hast verloren!')
    else:
        await ctx.channel.send(f'Unentschieden!')


@ssp.error
async def ssp_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Fehler: Fehlendes erforderliches Argumente. Format: **$ssp <Schere/Stein/Papier>**')
    elif isinstance(error, commands.BadArgument):
        await ctx.send('Fehler: Ungültiges Argument. Format: **$ssp <Schere/Stein/Papier>**')


@bot.command(name='serverinfo')
async def embed(ctx):
    embed = Embed(
        title='Server Info',
        description='Auf diesem Server findest du:',
        color=discord.Color.blue(),
    )

    embed.add_field(name='Name', value=ctx.guild, inline=True)

    embed.add_field(name='ID', value=ctx.guild.id, inline=True)

    embed.add_field(name='Erstellt am:', value=ctx.guild.created_at.strftime("%d.%m.%Y, %H:%M:%S"), inline=True)

    embed.add_field(name='Mitglieder', value=ctx.guild.member_count, inline=True)

    embed.add_field(name='Rollen', value=len(ctx.guild.roles), inline=True)

    embed.add_field(name='Emojis', value=len(ctx.guild.emojis), inline=True)

    embed.add_field(name='Kategorien', value=len(ctx.guild.categories), inline=True)

    embed.add_field(name='Voice Channel', value=len(ctx.guild.voice_channels), inline=True)

    embed.add_field(name='Text Channel', value=len(ctx.guild.text_channels), inline=True)

    embed.set_footer(text='Du hast alle Infos bekommen!')

    embed.set_thumbnail(url=ctx.guild.icon)

    # embed.set_author(name=ctx.author.name, icon_url=ctx.author.display_avatar)

    embed.timestamp = datetime.utcnow()

    await ctx.channel.send(embed=embed)


@bot.command(name='userinfo')
async def embed(ctx, user: discord.Member=''):

    if user == '':
        user = ctx.author

    embed = Embed(
        title='User Info',
        color=user.top_role.color
    )

    embed.add_field(name='Name', value=user.name, inline=True)

    embed.add_field(name='ID', value=user.id, inline=True)

    embed.add_field(name='Höchste Rolle', value=user.top_role, inline=True)

    embed.add_field(name='Rollen', value=len(user.roles), inline=True)

    embed.add_field(name='Beigetreten am', value=user.joined_at.strftime("%d.%m.%Y, %H:%M:%S"), inline=True)

    embed.set_thumbnail(url=user.avatar)

    # embed.set_author(name=ctx.author.name, icon_url=ctx.author.display_avatar)

    embed.timestamp = datetime.utcnow()

    await ctx.channel.send(embed=embed)


TOKEN = os.getenv('TOKEN')
bot.run(TOKEN)
