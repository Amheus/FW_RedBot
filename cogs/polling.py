## Games and Fun Commands for Red Bot

from logging import ERROR, DEBUG
import discord
from discord.ext import commands
from helpers import log_event
import string
from unicodedata import *


emoji_letters = list((lookup(f'REGIONAL INDICATOR SYMBOL LETTER {letter}')) for letter in string.ascii_uppercase)


class Polling(commands.Cog):

    @commands.command()
    async def poll(self, context):
        log_event(level=DEBUG, details="'$poll' command called")

        msg = context.message

        message_content = msg.clean_content

        # --------------------------------------------------
        # NO PARAMETERS
        # --------------------------------------------------

        if message_content.find("{") == -1:
            await context.message.add_reaction(u"\U0001F44D")
            await context.message.add_reaction(u"\U0001F44E")
            await context.message.add_reaction(u"\U0001F937")
            return

        # --------------------------------------------------
        # CUSTOM OPTIONS
        # --------------------------------------------------

        title = message_content[message_content.find("{") + 1:message_content.find("}")]

        # gets the number of options and assigns them to an array
        new_message = message_content[message_content.find("}"):]
        loop_time = 0

        option = []
        for _ in message_content:
            still_options = new_message.find("[")
            if still_options != -1:
                if loop_time == 0:
                    first = new_message.find("[") + 1
                    second = new_message.find("]")
                    second1 = second + 1
                    option.append(new_message[first:second])
                    loop_time += 1
                else:
                    new_message = new_message[second1:]
                    first = new_message.find("[") + 1
                    second = new_message.find("]")
                    second1 = second + 1
                    option.append(new_message[first:second])
                    loop_time += 1

        try:
            poll_message = ""
            i = 0
            for choice in option:
                if not option[i] == "":
                    if len(option) > 20:
                        await msg.channel.send("Maximum of 20 options")
                        log_event(level=ERROR, details="Command Failed, Too many Options")
                        return
                    elif not i == len(option) - 1:
                        poll_message = poll_message + "\n\n" + emoji_letters[i] + " " + choice
                i += 1

            e = discord.Embed(
                title="**" + title + "**",
                description=poll_message,
                colour=0x83bae3
            )
            poll_message = await msg.channel.send(embed=e)
            i = 0
            final_options = []
            for choice in option:
                if not i == len(option) - 1 and not option[i] == "":
                    final_options.append(choice)
                    await poll_message.add_reaction(emoji_letters[i])
                i += 1
            log_event(level=DEBUG, details="Command successfully executed")
        except Exception as error:
            log_event(level=ERROR, details="Command Failed, Incorrect Format [{error}]")
            await msg.channel.send(
                "Please make sure you are using the format **'$poll {<question>} [<itemA>] [<itemB>] [<itemC>]'**"
            )
