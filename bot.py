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
if __name__ == "__main__":                     
    bot.run(TOKEN)

