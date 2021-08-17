## Poll Commands for Red Bot
from logging import INFO, ERROR, DEBUG

import discord
from discord.ext import commands

from helpers import log_event


class Polling(commands.Cog):
    emojiLetters = [
        "\N{REGIONAL INDICATOR SYMBOL LETTER A}",
        "\N{REGIONAL INDICATOR SYMBOL LETTER B}",
        "\N{REGIONAL INDICATOR SYMBOL LETTER C}",
        "\N{REGIONAL INDICATOR SYMBOL LETTER D}",
        "\N{REGIONAL INDICATOR SYMBOL LETTER E}",
        "\N{REGIONAL INDICATOR SYMBOL LETTER F}",
        "\N{REGIONAL INDICATOR SYMBOL LETTER G}",
        "\N{REGIONAL INDICATOR SYMBOL LETTER H}",
        "\N{REGIONAL INDICATOR SYMBOL LETTER I}",
        "\N{REGIONAL INDICATOR SYMBOL LETTER J}",
        "\N{REGIONAL INDICATOR SYMBOL LETTER K}",
        "\N{REGIONAL INDICATOR SYMBOL LETTER L}",
        "\N{REGIONAL INDICATOR SYMBOL LETTER M}",
        "\N{REGIONAL INDICATOR SYMBOL LETTER N}",
        "\N{REGIONAL INDICATOR SYMBOL LETTER O}",
        "\N{REGIONAL INDICATOR SYMBOL LETTER P}",
        "\N{REGIONAL INDICATOR SYMBOL LETTER Q}",
        "\N{REGIONAL INDICATOR SYMBOL LETTER R}",
        "\N{REGIONAL INDICATOR SYMBOL LETTER S}",
        "\N{REGIONAL INDICATOR SYMBOL LETTER T}",
        "\N{REGIONAL INDICATOR SYMBOL LETTER U}",
        "\N{REGIONAL INDICATOR SYMBOL LETTER V}",
        "\N{REGIONAL INDICATOR SYMBOL LETTER W}",
        "\N{REGIONAL INDICATOR SYMBOL LETTER X}",
        "\N{REGIONAL INDICATOR SYMBOL LETTER Y}",
        "\N{REGIONAL INDICATOR SYMBOL LETTER Z}"]

    def __init__(self, client):
        self.client = client

    # COMMAND: $poll <question> OR $poll {<question>} [<itemA>] [<itemB>] [<itemC>] ...

    @commands.command()
    async def poll(self, context):
        log_event(level=DEBUG, details="'$poll' command called")

        msg = context.message

        messageContent = msg.clean_content

        if messageContent.find("{") == -1:
            await context.message.add_reaction(u"\U0001F44D")
            await context.message.add_reaction(u"\U0001F44E")
            await context.message.add_reaction(u"\U0001F937")
        else:
            first = messageContent.find("{") + 1
            second = messageContent.find("}")
            title = messageContent[first:second]

            # gets the number of options and assigns them to an array
            newMessage = messageContent[second:]
            loopTime = 0

            option = []
            for options in messageContent:
                # get from } [option 1]
                stillOptions = newMessage.find("[")
                if stillOptions != -1:
                    if loopTime == 0:
                        first = newMessage.find("[") + 1
                        second = newMessage.find("]")
                        second1 = second + 1
                        option.append(newMessage[first:second])
                        loopTime += 1
                    else:
                        newMessage = newMessage[second1:]
                        first = newMessage.find("[") + 1
                        second = newMessage.find("]")
                        second1 = second + 1
                        option.append(newMessage[first:second])
                        loopTime += 1

            try:
                pollMessage = ""
                i = 0
                for choice in option:
                    if not option[i] == "":
                        if len(option) > 20:
                            await msg.channel.send("Maximum of 20 options")
                            log_event(level=ERROR, details="Command Failed, Too many Options")
                            return
                        elif not i == len(option) - 1:
                            pollMessage = pollMessage + "\n\n" + self.emojiLetters[i] + " " + choice
                    i += 1

                e = discord.Embed(title="**" + title + "**",
                                  description=pollMessage,
                                  colour=0x83bae3)
                pollMessage = await msg.channel.send(embed=e)
                i = 0
                final_options = []
                for choice in option:
                    if not i == len(option) - 1 and not option[i] == "":
                        final_options.append(choice)
                        await pollMessage.add_reaction(self.emojiLetters[i])
                    i += 1
                log_event(level=DEBUG, details="Command Succesfull")
            except Exception as error:
                log_event(level=ERROR, details="Command Failed, Incorrect Format [{error}]")
                await msg.channel.send(
                    "Please make sure you are using the format **'$poll {<question>} [<itemA>] [<itemB>] [<itemC>]'**")


def setup(client):
    client.add_cog(Polling(client))
