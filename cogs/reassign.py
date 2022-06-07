import discord
from discord import app_commands
from discord.ext import commands
import os 
from db_connect import connection
            
c = connection.cursor()
GUILD = os.getenv('GUILD_ID')
#function that allows user to reassign leagues to names of their choice
class Reassign(commands.Cog):

    def __init___(self,bot:commands.bot,rows) -> None:
        self.bot = bot
        self.rows = rows

    @app_commands.command(name='reassign')
    @app_commands.checks.has_role('Admin')#Ensuring the approiate role is met, will be diffeerent for each server... must ensure user has the role to be able to use the below function
    async def reassign_league(self, interaction: discord.Interaction, league:str, number:str) -> None:
        """Reassign league name to different ID"""
        self.league_number = number
        self.league_name = league

        c.execute("SELECT * FROM league WHERE league_name = %s;",(self.league_name,))
        self.rows = c.fetchall()

        if len(self.rows) != 0:
            c.execute("UPDATE league SET league_name= %s, league_number= %s WHERE league_name= %s",(self.league_name,self.league_number,self.league_name,))
            connection.commit()
            return await interaction.response.send_message('League successfully reassigned.')
        
        else:
            return await interaction.response.send_message('League name or number does not  exist, please try again with a different combination.')

    

async def setup(bot: commands.Bot) -> None:
  await bot.add_cog(Reassign(bot), guilds=[discord.Object(id=GUILD)])

    
