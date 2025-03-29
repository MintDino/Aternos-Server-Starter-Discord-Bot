import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from start_server import start_aternos_server

# Load environment variables
load_dotenv()

TOKEN = os.getenv("DISCORD_BOT_TOKEN")

# Intents setup
intents = discord.Intents.default()
intents.messages = True
intents.guilds = True

bot = commands.Bot(command_prefix="/", intents=intents)

@bot.event
async def on_ready():
    print(f'✅ Logged in as {bot.user}')

@bot.command()
async def start(ctx):
    if ctx.channel.name != "bot":
        await ctx.send("⚠️ Please use this command in the #bot channel.")
        return

    await ctx.send("⏳ Starting the server, please wait...")
    
    logs = start_aternos_server()
    
    # Send logs to #logs channel
    logs_channel = discord.utils.get(ctx.guild.text_channels, name="logs")
    if logs_channel:
        await logs_channel.send(f"```\n{logs}\n```")

    # Send status update to #status channel
    status_channel = discord.utils.get(ctx.guild.text_channels, name="status")
    if status_channel:
        await status_channel.send("✅ Server started successfully!")

bot.run(TOKEN)
