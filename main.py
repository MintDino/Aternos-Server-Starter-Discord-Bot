import os
import discord
from discord.ext import commands
import asyncio
from start_server import start_aternos_server

TOKEN = os.getenv("DISCORD_BOT_TOKEN")
CATEGORY_NAME = "Server Status"

intents = discord.Intents.default()
intents.message_content = True

client = commands.Bot(command_prefix="/", intents=intents)

@client.event
async def on_ready():
    print(f"Logged in as {client.user}")

@client.command()
async def start(ctx):
    # Ensure command is used in the #bot channel within the correct category
    if isinstance(ctx.channel, discord.DMChannel):
        await ctx.send("Please use this command in the #bot channel on the server.")
        return

    if ctx.channel.name != "bot" or ctx.channel.category.name != CATEGORY_NAME:
        await ctx.send(f"Please use this command in the #bot channel inside the '{CATEGORY_NAME}' category.")
        return

    # Get the status and logs channels
    status_channel = discord.utils.get(ctx.guild.text_channels, name="status")
    logs_channel = discord.utils.get(ctx.guild.text_channels, name="logs")

    if not status_channel or not logs_channel:
        await ctx.send("Couldn't find #status or #logs channels. Please make sure they exist.")
        return

    await ctx.send("Starting the server...")

    # Start the server and get logs
    logs = start_aternos_server()

    # Send logs to #logs channel
    if logs_channel:
        await logs_channel.send(f"**Server Logs:**\n```{logs}```")

    # Send server status update
    if status_channel:
        await status_channel.send("✅ **Server start request sent!**")

client.run(TOKEN)
