## Games and Fun Commands for Red Bot

import random
from logging import ERROR, INFO, DEBUG

from discord.ext import commands

from helpers import log_event, log_event__command_begin, log_event__command_end


class Games(commands.Cog):

    @commands.command()
    async def dice(self, context, number_of_sides: str):
        log_event__command_begin('die')

        message_instance = await context.message.channel.send(content='Rolling the die, clickety clack...')
        failed: bool = False

        if not number_of_sides.isdigit():
            log_event(level=ERROR, details="FAILED: the <sides> parameter is not an integer")
            await message_instance.edit(content="the <sides> parameter must be an integer")
            failed = True

        if int(number_of_sides) > 900:
            log_event(level=ERROR, details="FAILED: the <sides> parameter is above the bounds of <900>")
            await message_instance.edit(content="the <sides> parameter must be less than or equal to 900")
            failed = True

        if int(number_of_sides) <= 0:
            log_event(level=ERROR, details="FAILED: the <sides> parameter is below the bounds of <0>")
            await message_instance.edit(content="the <sides> parameter must be greater than or equal to 0")
            failed = False

        if failed is False:
            output_message = f'The {number_of_sides} sided die landed on a **{str(random.randint(1, int(number_of_sides)))}**'

            await message_instance.edit(content=output_message)
            log_event__command_end('die')
