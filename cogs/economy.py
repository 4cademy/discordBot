import os
import pickle
import time

import discord
from discord.ext import commands
from discord import app_commands, Embed

from icecream import ic

economy_data = {}

daily_amount = 100

sad_money_cat_img = 'https://i.redd.it/uef724gewgf11.jpg'
stonks_img = 'https://printler.com/media/photo/150382.jpg'
make_it_rain_gif = 'https://c.tenor.com/lUhOtb4IYxAAAAAd/tenor.gif'
money_printer_gif = 'https://media1.tenor.com/m/SodieCmOhMIAAAAd/jerome-powell-powell.gif'


def save_data():
    ic(economy_data)
    for user_id in economy_data:
        print(user_id)
        print(economy_data[user_id])
    with open('economy_data.pkl', 'wb') as f:
        pickle.dump(economy_data, f)


class User:
    def __init__(self):
        self.coins = 100
        self.daily = 0

    def __str__(self):
        return f'Coins: {self.coins}\nDaily: {self.daily}'

    def add_coins(self, coins):
        self.coins += coins

    def get_coins(self):
        return self.coins

    def remove_coins(self, coins):
        if self.coins >= coins:
            self.coins -= coins
            return True
        return False

    def get_daily(self):
        if self.daily + 86400 <= time.time():
            self.daily = time.time()
            self.add_coins(daily_amount)
            return True
        return False


def user_in_economy(user_id):
    if user_id not in economy_data:
        embed = Embed(
            title='Economy',
            color=discord.Color.red()
        )
        embed.set_thumbnail(url=sad_money_cat_img)
        embed.add_field(name='',
                        value=f'**<@{user_id}> ist nicht in der Economy.\nTritt bei mit /join_economy**', inline=True)
        return False, embed
    return True, None


def send_not_enough_coins(user_id):
    embed = Embed(
        title='Economy',
        color=discord.Color.red()
    )
    embed.add_field(name=f'Du hast nur {economy_data[user_id].get_coins()} 🪙.', value='', inline=True)
    return embed


class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        global economy_data
        if not os.path.exists('economy_data.pkl'):
            with open('economy_data.pkl', 'wb') as f:
                pickle.dump(economy_data, f)
        else:
            with open('economy_data.pkl', 'rb') as f:
                economy_data = pickle.load(f)

    @app_commands.command(name='join_economy')
    async def join_economy(self, interaction: discord.Interaction):
        user_id = interaction.user.id

        if user_id not in economy_data:
            economy_data[user_id] = User()
            ic(economy_data)
            embed = Embed(
                title='Economy',
                color=discord.Color.green()
            )
            embed.set_thumbnail(url=stonks_img)
            embed.add_field(name='Du bist der Economy beigetreten.', value='', inline=True)
        else:
            embed = Embed(
                title='Economy',
                color=discord.Color.red()
            )
            embed.add_field(name='Du bist bereits in der Economy.', value='', inline=True)

        save_data()
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @app_commands.command(name='kontostand')
    async def kontostand(self, interaction: discord.Interaction):
        user_id = interaction.user.id
        already_joined, embed = user_in_economy(user_id)
        if already_joined:
            embed = Embed(
                title='Economy',
                color=discord.Color.green()
            )
            embed.set_thumbnail(url=make_it_rain_gif)
            coins = economy_data[user_id].get_coins()
            embed.add_field(name='Dein Kontostand', value=f'{coins} 🪙', inline=True)

        await interaction.response.send_message(embed=embed, ephemeral=True)

    @app_commands.command(name='daily')
    async def daily(self, interaction: discord.Interaction):
        user_id = interaction.user.id

        already_joined, embed = user_in_economy(user_id)
        if already_joined:
            if economy_data[user_id].get_daily():
                save_data()

                embed = Embed(
                    title='Economy',
                    color=discord.Color.green()
                )
                embed.add_field(name=f'Du hast {daily_amount} tägliche 🪙 erhalten.', value='', inline=True)
            else:
                embed = Embed(
                    title='Economy',
                    color=discord.Color.red()
                )
                embed.add_field(name='Du hast deine täglichen 🪙 bereits erhalten.', value='', inline=True)

        await interaction.response.send_message(embed=embed, ephemeral=True)

    @app_commands.command(name='send_coins')
    async def send_coins(self, interaction: discord.Interaction, user: discord.Member, amount: int):
        send_user_id = interaction.user.id
        receive_user_id = user.id

        already_joined, embed = user_in_economy(send_user_id)
        if already_joined:
            already_joined, embed = user_in_economy(receive_user_id)
            if already_joined:
                if economy_data[send_user_id].remove_coins(amount):
                    economy_data[receive_user_id].add_coins(amount)
                    save_data()

                    embed = Embed(
                        title='Economy',
                        color=discord.Color.green()
                    )
                    # send message to sender
                    embed.add_field(name='', value=f'**Du hast {amount} 🪙 an <@{receive_user_id}> gesendet.**',
                                    inline=True)
                    # send message to receiver
                    channel = await user.create_dm()
                    await channel.send(f'Du hast {amount} 🪙 von <@{send_user_id}> erhalten.')
                else:
                    embed = send_not_enough_coins(send_user_id)

        await interaction.response.send_message(embed=embed, ephemeral=True)

    @app_commands.command(name='print_money')
    async def print_money(self, interaction: discord.Interaction, user: discord.Member, amount: int):
        if interaction.user.guild_permissions.administrator:
            user_id = user.id

            already_joined, embed = user_in_economy(user_id)
            if already_joined:
                economy_data[user_id].add_coins(amount)
                save_data()

                embed = Embed(
                    title='Economy',
                    color=discord.Color.green()
                )
                embed.set_image(url=money_printer_gif)
                embed.add_field(name='', value=f'**Die Zentralbank hat {amount} 🪙 gedruckt und {user.mention} gegeben.**', inline=True)
                await interaction.response.send_message(embed=embed)
            else:
                await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            embed = Embed(
                title='Economy',
                color=discord.Color.red()
            )
            embed.add_field(name='', value=f'**Du hast keine Berechtigung.**', inline=True)
            await interaction.response.send_message(embed=embed, ephemeral=True)
