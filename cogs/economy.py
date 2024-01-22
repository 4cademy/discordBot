import os
import pickle
from datetime import datetime

import discord
from discord.ext import commands
from discord import app_commands, Embed

from icecream import ic

economy_data = {}

daily_amount = 100

sad_money_cat_img = 'https://i.redd.it/uef724gewgf11.jpg'
stonks_img = 'https://printler.com/media/photo/150382.jpg'
make_it_rain_gif = 'https://c.tenor.com/lUhOtb4IYxAAAAAd/tenor.gif'


def save_data():
    with open('economy_data.pkl', 'wb') as f:
        pickle.dump(economy_data, f)


class User:
    def __init__(self):
        self.coins = 100
        self.daily = datetime.now().day - 1

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
        if self.daily != datetime.now().day:
            self.daily = datetime.now().day
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
        embed.add_field(name='Du bist nicht in der Economy. Tritt bei mit /join_economy', value='', inline=True)
        return False, embed
    return True, None


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
        save_data()
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @app_commands.command(name='daily')
    async def daily(self, interaction: discord.Interaction):
        user_id = interaction.user.id

        already_joined, embed = user_in_economy(user_id)
        if already_joined:
            if economy_data[user_id].get_daily():
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
        save_data()
        await interaction.response.send_message(embed=embed, ephemeral=True)
