## Moderation Commands for Red Bot

import datetime
from logging import INFO, ERROR, DEBUG

import discord
from discord.ext import commands
from discord.ext.commands import has_role

from helpers import log_event


class Moderation(commands.Cog):
    reportChannelID = 618183760482926620
    modRoleName = "scarlet"  # Lower Case
    modRole = ""

    muteRoleID = 618186776821104642

    # COMMAND: $report <reported user> <reasoning>

    @commands.command()
    async def report(self, context):

        log_event(event_type=DEBUG, event_details="'$report' command called")

        dateObj = datetime.datetime.now()
        dateStr = dateObj.strftime("%a %d %b - %H:%M ") + "GMT"

        msg1 = "Username: " + context.message.author.name + "| Nickname: " + context.message.author.display_name
        msg2 = context.message.content.split(" ")[1].strip()
        msg3temp = context.message.content.split(" ")

        for y in context.message.guild.roles:
            if self.modRoleName == y.name.lower():
                self.modRole = y

        await context.message.delete()

        msg3 = ""
        for i in range(2, len(msg3temp)):
            msg3 = msg3 + " " + msg3temp[i]

        reportChnl = self.client.get_channel(self.reportChannelID)

        embed = discord.Embed(title="**REPORT**: " + dateStr, color=0x4287f5)
        embed.add_field(name="User Reported By: ", value=msg1, inline=False)
        embed.add_field(name="User Reported: ", value=msg2, inline=False)
        embed.add_field(name="Reason: ", value=msg3, inline=False)

        await reportChnl.send(self.modRole.mention + " the following report has been recieved:")

        await reportChnl.send(embed=embed)

        log_event(event_type=DEBUG, event_details="Command Succesfull")

    # COMMAND: $ilence <member mention>

    @has_role("Scarlet")
    @commands.command()
    async def ilence(self, context):

        log_event(event_type=DEBUG, event_details="'$ilence' command called")

        toMute = context.message.mentions[0]
        reasonStr = "Muted by" + context.message.author.display_name

        muteRole = context.message.guild.get_role(self.muteRoleID)

        if muteRole == None:
            log_event(event_type=ERROR, event_details="ERROR: Mute role not found, check ID is correct")
        else:
            await toMute.add_roles(muteRole, reason=reasonStr)
            log_event(event_type=DEBUG, event_details="Command Succesfull")
            await context.message.channel.send("```**MUTED** {} indefinetly!```".format(toMute.display_name))


def setup(client):
    client.add_cog(Moderation(client))
