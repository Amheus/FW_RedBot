## Games and Fun Commands for Red Bot

import random
from logging import ERROR, INFO, DEBUG, WARNING

from discord.ext import commands

from helpers import log_event, log_event__command_begin, log_event__command_end


class Utility(commands.Cog):

    @commands.command()
    async def help(self, context):
        log_event__command_begin('help')

        with open('HELP.md', 'r+') as help_file:
            help_contents = help_file.read()

            if help_contents == '': log_event(level=WARNING, details="No Help File Found. Created Empty One")

            help_file.close()
            await context.message.channel.send(help_contents)

        log_event__command_end('help')
