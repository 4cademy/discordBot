import discord
from discord.ext import commands
from discord import Embed
import os
from dotenv import load_dotenv
import random
from datetime import datetime
import time
import pickle

load_dotenv('.env')


class User:
    def __init__(self, user_id):
        self.id = user_id
        self.coins = 100

    def add_coins(self, coins):
        self.coins += coins

    def remove_coins(self, coins):
        if self.coins >= coins:
            self.coins -= coins
            return True
        return False


user_data = {}

if not os.path.exists('user_data.pkl'):
    with open('user_data.pkl', 'wb') as f:
        pickle.dump(user_data, f)
else:
    with open('user_data.pkl', 'rb') as f:
        user_data = pickle.load(f)

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

    embed = Embed(
        title='Münzwurf',
    )
    msg = await ctx.channel.send(embed=embed)

    embed.add_field(name='Werfen', value='', inline=False)

    await msg.edit(embed=embed)

    for i in range(3):
        time.sleep(0.1)
        embed.set_field_at(index=0, name='Werfen.', value='', inline=False)
        await msg.edit(embed=embed)
        time.sleep(0.1)
        embed.set_field_at(index=0, name='Werfen..', value='', inline=False)
        await msg.edit(embed=embed)
        time.sleep(0.1)
        embed.set_field_at(index=0, name='Werfen...', value='', inline=False)
        await msg.edit(embed=embed)
        time.sleep(0.1)
        embed.set_field_at(index=0, name='Werfen', value='', inline=False)
        await msg.edit(embed=embed)

    zahl = random.randint(0, 1)
    if zahl == 0:
        result = 'Kopf'
    else:
        result = 'Zahl'

    embed.set_field_at(index=0, name='Ergebnis:', value=result, inline=False)

    if wahl == result:
        embed.add_field(name='Du hast gewonnen!', value='', inline=False)
    else:
        embed.add_field(name='Du hast verloren.', value='', inline=False)

    await msg.edit(embed=embed)


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

    embed = Embed(
        title='DUEL!',
    )

    embed.add_field(name='Du', value=emojis[user_no], inline=True)
    msg = await ctx.channel.send(embed=embed)

    embed.add_field(name='vs', value='', inline=True)
    await msg.edit(embed=embed)

    embed.add_field(name='Bot', value=emojis[com_no], inline=True)
    await msg.edit(embed=embed)

    if user_no == 0 and com_no == 2:
        result_msg = 'Du hast gewonnen!'
    elif user_no == 2 and com_no == 0:
        result_msg = 'Du hast verloren!'
    elif user_no > com_no:
        result_msg = 'Du hast gewonnen!'
    elif user_no < com_no:
        result_msg = 'Du hast gewonnen!'
    else:
        result_msg = 'Unentschieden!'

    embed.add_field(name=result_msg, value='', inline=True)

    await msg.edit(embed=embed)


@ssp.error
async def ssp_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Fehler: Fehlendes erforderliches Argumente. Format: **$ssp <Schere/Stein/Papier>**')
    elif isinstance(error, commands.BadArgument):
        await ctx.send('Fehler: Ungültiges Argument. Format: **$ssp <Schere/Stein/Papier>**')


@bot.command(name='serverinfo')
async def serverinfo(ctx):
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
async def userinfo(ctx, user: discord.Member = ''):
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


@bot.command(name='editMsg')
async def editMsg(ctx):
    msg = await ctx.channel.send('Originale Nachricht')
    time.sleep(2)
    await msg.edit(content='**Bearbeitete Nachricht**')
    time.sleep(2)
    await msg.edit(content='*Bearbeitete Nachricht*')
    time.sleep(2)
    await msg.edit(content='__Bearbeitete Nachricht__')
    time.sleep(2)
    await msg.edit(content='~~Bearbeitete Nachricht~~')
    time.sleep(2)
    await msg.edit(content='||Bearbeitete Nachricht||')
    time.sleep(2)
    await msg.edit(content='> Bearbeitete Nachricht')
    time.sleep(2)
    await msg.edit(content='>>> Bearbeitete\nNachricht')
    time.sleep(2)
    await msg.edit(content='`Bearbeitete Nachricht`')
    time.sleep(2)
    await msg.edit(content='```\nBearbeitete\nNachricht\n```')


@bot.command(name='YN')
async def YN(ctx, *question):
    embed = Embed(
        title='Umfrage von ' + ctx.author.name,
        color=ctx.author.top_role.color
    )
    embed.set_author(name=ctx.author.name, icon_url=ctx.author.display_avatar)

    question = ' '.join(question)
    embed.add_field(name='Frage:', value=f'{question}', inline=False)

    msg = await ctx.channel.send(embed=embed)

    await msg.add_reaction('👍')
    await msg.add_reaction('👎')


@bot.command(name='helloWorld')
async def helloWorld(ctx):
    msg = await ctx.channel.send('```py\nprint(\'Hello World!\')\n```')


@bot.command(name='code')
async def code(ctx, lang, *codeblock):
    codeblock = ' '.join(codeblock)
    await ctx.channel.send(f'```{lang}\n{codeblock}\n```')


@bot.command(name='createRole')
async def createRole(ctx, rolename, color=discord.Color.blue()):
    server = ctx.guild
    if discord.utils.get(server.roles, name=rolename) is not None:
        embed = Embed(
            title='Rolleninfo',
            color=discord.Color.red()
        )
        embed.add_field(name='Fehler:', value=f'Rolle **{rolename}** existiert bereits!', inline=True)
    else:
        await server.create_role(name=rolename, color=color)
        embed = Embed(
            title='Rolleninfo',
            color=discord.Color.green()
        )
        embed.add_field(name='Rolle erstellt', value=f'**{rolename}**', inline=True)
    await ctx.channel.send(embed=embed)


@bot.command(name='setRole')
async def setRole(ctx, rolename, user: discord.Member):
    server = ctx.guild
    role = discord.utils.get(server.roles, name=rolename)
    if role is None:
        embed = Embed(
            title='Rolleninfo',
            color=discord.Color.red()
        )
        embed.add_field(name='Fehler:', value=f'Rolle **{rolename}** existiert nicht!', inline=True)
    else:
        if role in user.roles:
            await user.remove_roles(role)
            embed = Embed(
                title='Rolleninfo',
                color=discord.Color.green()
            )
            embed.add_field(name='Rolle entfernt', value=f'**{rolename}**', inline=True)
        else:
            await user.add_roles(role)
            embed = Embed(
                title='Rolleninfo',
                color=discord.Color.green()
            )
            embed.add_field(name='Rolle hinzugefügt', value=f'**{rolename}**', inline=True)
    await ctx.channel.send(embed=embed)


@bot.command(name='botColor')
async def botColor(ctx):
    server = ctx.guild
    role = discord.utils.get(server.roles, name="ServerSurfer")

    for i in range(0, 10):
        color = random.randint(0, 0xFFFFFF)
        await role.edit(color=color)
        time.sleep(1)


@bot.command(name='dice')
async def dice(ctx):
    dice = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣']

    user_roll1 = random.randint(1, 6)
    user_roll2 = random.randint(1, 6)
    server_roll1 = random.randint(1, 6)
    server_roll2 = random.randint(1, 6)

    user_sum = user_roll1 + user_roll2
    server_sum = server_roll1 + server_roll2

    if user_roll1 == user_roll2:
        user_sum *= 2
    if server_roll1 == server_roll2:
        server_sum *= 2

    embed = Embed(
        title='Dice'
    )
    embed.add_field(name='Dein Wurf', value=f'{dice[user_roll1 - 1]} {dice[user_roll2 - 1]} (∑ {user_sum})',
                    inline=True)
    embed.add_field(name='Server Wurf', value=f'{dice[server_roll1 - 1]} {dice[server_roll2 - 1]} (∑ {server_sum})',
                    inline=True)
    embed.add_field(name='Ergebnis', value='', inline=False)

    if user_sum > server_sum:
        embed.color = discord.Color.green()
        result = 'Du hast gewonnen!'
    elif user_sum < server_sum:
        embed.color = discord.Color.red()
        result = 'Du hast verloren!'
    else:
        embed.color = discord.Color.light_gray()
        result = 'Unentschieden!'

    embed.set_field_at(index=2, name='Ergebnis', value=result, inline=False)

    await ctx.channel.send(embed=embed)


TOKEN = os.getenv('TOKEN')
bot.run(TOKEN)
