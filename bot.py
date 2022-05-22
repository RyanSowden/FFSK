import os
import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv() #loading the .env file
TOKEN = os.getenv('DISCORD_TOKEN') #fetches the discord token from .env file
league = () #setting the league variable
GUILD = os.getenv('GUILD_ID')
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
#tree = app_commands.CommandTree(client)


'''
@tree.command(guild=discord.Object(id=GUILD), name='ping',description='Test slash command')
async def slash(interaction: discord.Interaction):
    await interaction.response.send_message('Pong', ephemeral=True)

@tree.command(guild=discord.Object(id=GUILD), name='test1',description='Test2 slash command')
async def slash(interaction: discord.Interaction):
    await interaction.response.send_message('Slash commands working correctly', ephemeral=True)
@client.event
async def on_ready():
    synced = False #we use this so the bot doesn't sync commands more than once
    await wait_until_ready()
    if not synced: #check if slash commands have been synced 
        await client.tree.copy_global_to(guild=discord.Object(id=GUILD)) 
        synced = True
    print("Commands successfully updated..")
    print(f'{client.user} has connected to Discord!')

#Error handling....
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, discord.ext.commands.errors.CommandNotFound):
        await ctx.send("Sorry, that command wasn't found, enter ;help for a list of commands.")
    elif isinstance(error, discord.ext.commands.MissingRequiredArgument):
        await ctx.send("Please provied the required amount of arguments.")
    elif isinstance(error, discord.ext.commands.MissingRole):
        await ctx.send("You don't have the sufficient role to perform this action")
    else:
        raise error

#error handling logging, *writes to err.log
@client.event
async def on_error(event, *args, **kwargs):
    with open('err.log', 'a') as f:
        if event == 'on_message':
            f.write(f'Unhandled message: {args[0]}\n')
        else:
            raise

@bot.command()
async def load(ctx, extension):
    bot.load_extension(f'cogs.{extension}')
'''
class Bot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix='', intents=intents)

    
    async def startup(self):
        await bot.wait_until_ready()
        await bot.tree.sync(guild=discord.Object(id=864073380612800522))
        print('Commands synced')
        print(f'Connected as {bot.user}')
    
    async def setup_hook(self):
        for filename in os.listdir("./cogs"):
            if filename.endswith(".py"):
                try:
                    await bot.load_extension(f"cogs.{filename[:-3]}")
                    print(f"Loaded {filename}")
                except Exception as e:
                    print(e)
                self.loop.create_task(self.startup())

bot = Bot()                        
bot.run(TOKEN)

