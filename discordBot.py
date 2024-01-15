import discord
from discord.ext import commands
from discord import app_commands
from discord import Embed
import os
from dotenv import load_dotenv
import random
from datetime import datetime
import time
import pickle



from cogs.games import Games
from cogs.help import CustomHelp
from cogs.maths import Maths
from cogs.slashs import Slashs

load_dotenv('.env')


class User:
    def __init__(self):
        self.coins = 100
        self.daily = datetime.now().day-1

    def add_coins(self, coins):
        self.coins += coins

    def remove_coins(self, coins):
        if self.coins >= coins:
            self.coins -= coins
            return True
        return False


user_data = {}


def save_data():
    with open('user_data.pkl', 'wb') as f:
        pickle.dump(user_data, f)


def add_user(user_id):
    if user_id not in user_data:
        user_data[user_id] = User()
        save_data()
        return True
    return False


intents = discord.Intents.all()

bot = commands.Bot(command_prefix='$', description='This is Marcels bot', help_command=CustomHelp(), intents=intents)


@bot.event
async def on_ready():
    await bot.add_cog(Games(bot))
    await bot.add_cog(Maths(bot))
    await bot.add_cog(Slashs(bot))

    try:
        synced = await bot.tree.sync()
        print(f'Synced {len(synced)} application commands')
    except Exception as e:
        print(f'Failed to sync application commands: {e}')

    global user_data
    if not os.path.exists('user_data.pkl'):
        with open('user_data.pkl', 'wb') as f:
            pickle.dump(user_data, f)
    else:
        with open('user_data.pkl', 'rb') as f:
            user_data = pickle.load(f)
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


# Economy Commands
@bot.command(name='join_economy')
async def join_economy(ctx):
    if add_user(ctx.author.id):
        await ctx.channel.send(f'Willkommen in der Economy, {ctx.author.name}!')
    else:
        await ctx.channel.send(f'Du bist bereits in der Economy, {ctx.author.name}!')


@bot.tree.context_menu(name='Get Joined Date')
async def get_joined_date(interaction: discord.Interaction, user: discord.Member):
    await interaction.response.send_message(f'{user.name} joined on {discord.utils.format_dt(user.joined_at)}', ephemeral=True)


@bot.tree.context_menu(name='User Info')
async def userinfo(interaction: discord.Interaction, user: discord.Member):
    embed = Embed(
        title='User Info',
        color=user.top_role.color
    )

    embed.add_field(name='Name', value=user.name, inline=True)

    embed.add_field(name='ID', value=user.id, inline=True)

    embed.add_field(name='Höchste Rolle', value=user.top_role, inline=True)

    embed.add_field(name='Rollen', value=len(user.roles), inline=True)

    embed.add_field(name='Auf Discord seit', value=discord.utils.format_dt(user.created_at), inline=True)

    embed.add_field(name='Server beigetreten am', value=discord.utils.format_dt(user.joined_at), inline=True)

    embed.set_thumbnail(url=user.avatar)

    # embed.set_author(name=ctx.author.name, icon_url=ctx.author.display_avatar)

    embed.timestamp = datetime.utcnow()

    await interaction.response.send_message(embed=embed, ephemeral=True)



TOKEN = os.getenv('TOKEN')
bot.run(TOKEN)
