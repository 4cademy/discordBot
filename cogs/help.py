from typing import Any

import discord
from discord.ext import commands
from discord import Embed
from discord.ext.commands import Command


class CustomHelp(commands.HelpCommand):
    def get_command_signature(self, command):
        return f'{self.context.clean_prefix}{command.qualified_name} {command.signature}'

    # $help
    async def send_bot_help(self, mapping):
        embed = Embed(title='Help', color=discord.Color.green())
        all_commands = []
        for cog, commands in mapping.items():
            all_commands += commands
        for command in all_commands:
            embed.add_field(name=command.qualified_name, value=self.get_command_signature(command), inline=False)
        await self.get_destination().send(embed=embed)

    # $help <command>
    async def send_command_help(self, command):
        embed = Embed(title=self.get_command_signature(command), color=discord.Color.blue())
        if command.help:
            embed.description = command.help

        await self.get_destination().send(embed=embed)

    async def send_group_help(self, group):
        pass

    async def send_cog_help(self, cog):
        pass
