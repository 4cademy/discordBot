import discord
from discord.ext import commands
from discord import Embed
import time
import random
import asyncio


class Games(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='münzwurf', aliases=['Münzwurf', 'MÜNZWURF'])
    async def muenzwurf(self, ctx, wahl):
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
    async def muenzwurf_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Fehler: Fehlendes erforderliches Argumente. Format: **$münzwurf <Kopf/Zahl>**')
        elif isinstance(error, commands.BadArgument):
            await ctx.send('Fehler: Ungültiges Argument. Format: **$münzwurf <Kopf/Zahl>**')

    @commands.command(name='dice')
    async def dice(self, ctx):
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

    @commands.command(name='ssp')
    async def ssp(self, ctx, wahl):
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
    async def ssp_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Fehler: Fehlendes erforderliches Argumente. Format: **$ssp <Schere/Stein/Papier>**')
        elif isinstance(error, commands.BadArgument):
            await ctx.send('Fehler: Ungültiges Argument. Format: **$ssp <Schere/Stein/Papier>**')

    @commands.command(name='guess')
    async def guess(self, ctx, min, max):
        try:
            min = int(min)
            max = int(max)
        except ValueError:
            raise commands.BadArgument

        number = random.randint(min, max)

        embed = Embed(
            title='Guess',
            description=f'Guess a number between {min} and {max}.',
            colour=discord.Colour.blue()
        )
        send_msg = await ctx.channel.send(embed=embed)

        tries = 5
        while tries > 0:
            try:
                msg = await self.bot.wait_for('message', timeout=10.0,
                                              check=lambda message: message.author == ctx.author)
                await msg.delete()
            except asyncio.TimeoutError:
                embed = discord.Embed(
                    title='Timeout',
                    description='Try again.',
                    colour=discord.Colour.red()
                )
                await send_msg.edit(embed=embed)
                return
            else:
                try:
                    guess = int(msg.content)
                except ValueError:
                    embed = discord.Embed(
                        title='Error',
                        description='Enter a valid number.',
                        colour=discord.Colour.yellow()
                    )
                    await send_msg.edit(embed=embed)
                else:
                    if guess == number:
                        embed = Embed(
                            title='Guess',
                            description=f'You guessed the number {number} correctly.',
                            colour=discord.Colour.green()
                        )
                        await send_msg.edit(embed=embed)
                        break
                    else:
                        tries -= 1
                        if tries == 0:
                            embed = Embed(
                                title='Guess',
                                description=f'You guessed incorrectly. The number was {number}.',
                                colour=discord.Colour.red()
                            )
                        else:
                            embed = Embed(
                                title='Guess',
                                description=f'You guessed incorrectly. Try again. {tries} tries left.',
                                colour=discord.Colour.red()
                            )
                        await send_msg.edit(embed=embed)

    @guess.error
    async def guess_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Fehler: Fehlendes erforderliches Argumente. Format: **$guess <min> <max>**')
        elif isinstance(error, commands.BadArgument):
            await ctx.send('Fehler: Ungültiges Argument. Format: **$ssp <Schere/Stein/Papier>**')

