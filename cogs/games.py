## Games and Fun Commands for Red Bot

import random

from discord.ext import commands

from helpers import log_event


class Games(commands.Cog):

    def __init__(self, client, sheets):
        self.client = client
        self.gsheet = sheets

    # COMMAND: $dice <sides>

    @commands.command()
    async def dice(self, context):
        log_event(txt="'$dice' command called")

        msgOut = await context.message.channel.send(content='Rolling the Die, Clickety Clack...')
        failed = 0

        try:
            input = context.message.content.split(" ")[1].strip()
            max = int(input)

        except Exception as error:
            failed = 1
            log_event(txt="FAILED: <sides> Parameter Not an Integer [{}]".format(error))
            await msgOut.edit(content="<sides> Parameter Must be an Integer")

        if len(str(max)) > 900:
            failed = 1
            log_event(txt="FAILED: <sides> Parameter Too Big")
            await msgOut.edit(content="<sides> Parameter Must be smaller than 900 characters")

        if max < 1:
            failed = 0
            log_event(txt="FAILED: <sides> Parameter Too Small")
            await msgOut.edit(content="<sides> Parameter Must be Larger than 0")

        if failed == 0:
            out = "The " + input + " sided die Landed On a **" + str(random.randint(1, max)) + "**"

            await msgOut.edit(content=out)
            log_event(txt="Command Succesfull, " + out)
