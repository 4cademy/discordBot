import discord

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

bot.run('MTE3MTA2NzI5OTU2MjgwMzIzMQ.GmQ1kg.SB6J08G8Hce4xW7YUCgoVPV4hbHY2H-cnqeXCY')
