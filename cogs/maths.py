import discord
from discord.ext import commands
from discord import Embed
import time
import random
import asyncio


class Maths(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='square')
    async def square(self, ctx):
        embed = Embed(
            title='Square',
            description='Enter a number to get the square of it.',
            colour=discord.Colour.blue()
        )
        send_msg = await ctx.channel.send(embed=embed)

        while True:
            try:
                msg = await self.bot.wait_for('message', timeout=10.0, check=lambda message: message.author == ctx.author)
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
                    number = int(msg.content)
                except ValueError:
                    embed = discord.Embed(
                        title='Error',
                        description='Enter a valid number.',
                        colour=discord.Colour.yellow()
                    )
                    await send_msg.edit(embed=embed)
                else:
                    break

        embed = Embed(
            title='Square',
            description=f'The square of {number} is {number**2}.',
            colour=discord.Colour.green()
        )

        await send_msg.edit(embed=embed)
