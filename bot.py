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

client = commands.Bot(command_prefix=';', help_command=None)

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

#Error hadnling....
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

@client.command()
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')


@client.command()
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')


client.run(TOKEN)

