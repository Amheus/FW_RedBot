## Moderation Commands for Red Bot

import datetime
import discord
from discord.ext import commands

class Moderation(commands.Cog):
  
	reportChannelID = 618183760482926620
	modRoleName = "scarlet"	#Lower Case
	modRole = ""

	def __init__(self, client):
		self.client = client
	
	def set_refs(self, logger, sheets):
		self.logs = logger
		self.gsheet = sheets
		
# COMMAND: $report <reported user> <reasoning>

	@commands.command()
	async def report(self, context):
	
		self.logs.log("'$report' command called")    
	
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
		
		self.logs.log("Command Succesfull")
		
def setup(client):
	client.add_cog(Moderation(client))