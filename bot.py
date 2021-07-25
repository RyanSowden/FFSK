import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from sleeper_wrapper import League
from sleeper_wrapper import Players
import pandas as pd
from tabulate import tabulate

load_dotenv() #loading the .env file
TOKEN = os.getenv('DISCORD_TOKEN') #fetches the discord token from .env file
league = () #setting the league variable

client = commands.Bot(command_prefix=';')

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')



@client.command()
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')


@client.command()
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')


#error handling & logging for easy tracking, *writes to err.log
@client.event
async def on_error(event, *args, **kwargs):
    with open('err.log', 'a') as f:
        if event == 'on_message':
            f.write(f'Unhandled message: {args[0]}\n')
        else:
            raise

#@client.command(name='assign', help='This lests the admin user assign the league ID from sleeper to a key word e.g Green')
#async def assign_key_value(ctx,*args):
 #   league_number = args
#   league_name = args
 #   new_league_name = league_name(args)
  #  await ctx.send(new_leauge_name)


client.run(TOKEN)

