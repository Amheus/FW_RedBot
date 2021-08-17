## Help adn Info Commands for Red Bot
from logging import INFO, DEBUG

from discord.ext import commands

from helpers import log_event


class Help(commands.Cog):

    def __init__(self, client):
        self.client = client

        # Get help File
        f = open('HELP.md', 'r+')
        self.helpContents = f.read()

        if self.helpContents == "":
            log_event(event_type=INFO, event_details="No Help File Found. Created Empty One")

        f.close()

    def set_refs(self, logger, sheets):
        self.gsheet = sheets

    # COMMAND: $help

    @commands.command()
    async def help(self, context):
        log_event(event_type=DEBUG, event_details="'$help' command called")

        await context.message.channel.send(self.helpContents)

        log_event(event_type=DEBUG, event_details="Command Succesfull")


def setup(client):
    client.add_cog(Help(client))
