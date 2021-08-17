import configparser
import logging
import os
import time

import gspread
from discord.ext import commands
from oauth2client.service_account import ServiceAccountCredentials

from cogs.games import Games
from cogs.polling import Polling
from cogs.utility import Utility
from helpers import log_event

log_event(level=logging.INFO, details="---------------------- Starting Up ----------------------")

# Gspread variables
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']

credentials = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)

# global variables
gsheet = ""


# Non-Discord Functions

def setup_gSpread():
    try:
        global gSheet
        global comradeSheetMain
        global comradeEventsSheetMain

        gSheet = gspread.authorize(credentials)

        log_event(level=logging.INFO, details="Loaded gSpread")

    except Exception as error:
        log_event(level=logging.ERROR, details="ERROR: Couldnt load gSpread [{}]".format(error))


def find_extensions(folder):
    cogs = []

    extensionFiles = os.listdir("./{}".format(folder))

    for file in extensionFiles:
        pyPos = file.find(".py")
        if pyPos != -1:
            cogs.append(file[:pyPos])

    return cogs


## Setup
setup_gSpread()

# Discord setup
client = commands.Bot(command_prefix='$')
lastLoginTime = time.time()


# Discord functions

@client.event
async def on_ready():
    log_event(level=logging.INFO, details='We have logged in as {0.user}, setup complete'.format(client))


@client.event
async def on_message(msg):
    global lastLoginTime

    ## Check if gSpread token has expired, reload
    if credentials.access_token_expired:
        log_event(level=logging.INFO, details="GSheets Token expired. Last login at {}".format(lastLoginTime))
        gSheet.login()
        lastLoginTime = time.time()

    await client.process_commands(msg)


def main():
    global gSheets

    client.remove_command("help")

    with open("config.ini") as file:
        config = configparser.RawConfigParser(allow_no_value=True)
        config.read_string(file.read())

    client.add_cog(Games())
    client.add_cog(Utility())
    client.add_cog(Polling())
    client.run(config.get('discord', 'token'))


if __name__ == '__main__':
    main()
