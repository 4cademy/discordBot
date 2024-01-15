import discord
from discord.ext import commands
from discord import app_commands, Embed
import typing
import random

import requests
import json

yes = {'yes', 'y', 'ja', 'j', 'true', 't', '1'}


class Slashs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='testslash')
    async def testslash(self, interaction: discord.Interaction):
        await interaction.response.send_message('Test Slash')

    @app_commands.command(name='unsichtbarer_slash')
    async def unsichtbarer_slash(self, interaction: discord.Interaction):
        await interaction.response.send_message('Diesen Text sieht nur du.', ephemeral=True)

    @app_commands.command(name='slash_mit_variablen')
    @app_commands.describe(zahl='Eine Zahl')
    @app_commands.describe(text='Ein Text')
    async def slash_mit_variablen(self, interaction: discord.Interaction, zahl: int, text: str):
        await interaction.response.send_message(f'Gesendet: \n Zahl: {zahl} \n Text: {text}')

    @app_commands.command(name='sichtbar_unsichtbar')
    @app_commands.describe(unsichtbar='yes/no')
    async def sichtbar_unsichtbar(self, interaction: discord.Interaction, unsichtbar: typing.Optional[str] = 'no'):
        if unsichtbar.lower() in yes:
            await interaction.response.send_message('Dieser Text ist unsichtbar.', ephemeral=True)
        else:
            await interaction.response.send_message('Dieser Text ist sichtbar.')

    @app_commands.command(name='ssp')
    async def ssp(self, interaction: discord.Interaction, wahl: typing.Literal['✂️', '🪨', '📰']):
        emojis = ['✂️', '🪨', '📰']

        user_no = emojis.index(wahl)

        com_no = random.randint(0, 2)

        embed = Embed(
            title='DUEL!',
        )

        embed.add_field(name='Du', value=emojis[user_no], inline=True)
        msg = await interaction.response.send_message(embed=embed)

        embed.add_field(name='vs', value='', inline=True)
        await interaction.edit_original_response(embed=embed)

        embed.add_field(name='Bot', value=emojis[com_no], inline=True)
        await interaction.edit_original_response(embed=embed)

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

        await interaction.edit_original_response(embed=embed)

    @app_commands.command(name='get_color')
    async def get_color(self, interaction: discord.Interaction, color: typing.Literal['rot', 'grün', 'blau', 'gelb']):
        color_roles = ['rot', 'grün', 'blau', 'gelb']

        server = interaction.guild
        user = interaction.user
        role = discord.utils.get(server.roles, name=color)

        user_roles = [role.name for role in user.roles]
        for c in color_roles:
            if c in user_roles:
                await user.remove_roles(discord.utils.get(server.roles, name=c))

        await user.add_roles(role)

        await interaction.response.send_message(f'Du hast die Rolle <@&{role.id}> erhalten.')

    @app_commands.command(name='meme')
    async def meme(self, interaction: discord.Interaction):
        while True:
            response = requests.get('https://meme-api.com/gimme')
            json_data = json.loads(response.text)

            nsfw = True
            if not json_data['nsfw']:
                nsfw = False

            upvotes = json_data['ups']
            print(upvotes)

            if upvotes >= 100 and not nsfw and json_data['url']:
                break

        embed = Embed(
            title=json_data['title'],
            color=discord.Color.green()
        )
        embed.set_image(url=json_data['url'])
        await interaction.response.send_message(embed=embed)
