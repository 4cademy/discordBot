import discord
import os
from dotenv import load_dotenv

load_dotenv('.env')

intents = discord.Intents.all()

bot = discord.Client(intents=intents)


@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello! ' + message.author.name)


TOKEN = os.getenv('TOKEN')
bot.run(TOKEN)
