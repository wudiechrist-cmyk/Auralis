import os
import discord

from discord.ext import commands

from config import PREFIX
from database import init_database


# ============================================================
# INTENTS
# ============================================================

intents = discord.Intents.default()

intents.message_content = True
intents.members = True


# ============================================================
# BOT
# ============================================================

bot = commands.Bot(
    command_prefix=PREFIX,
    intents=intents,
    help_command=None
)


# ============================================================
# LOAD COGS
# ============================================================

async def load_extensions():

    extensions = [

        "cogs.moderation",
        "cogs.economy",
        "cogs.games",
        "cogs.leveling",
        "cogs.fun",
        "cogs.utility"
	
    ]

    for extension in extensions:

        try:

            await bot.load_extension(extension)

            print(f"Loaded: {extension}")

        except Exception as e:

            print(f"FAILED: {extension}")
            print(e)


# ============================================================
# READY
# ============================================================

@bot.event
async def on_ready():

    print(f"Logged in as {bot.user}")

    # Sync slash commands to every server immediately
    for guild in bot.guilds:
        try:
            bot.tree.copy_global_to(guild=guild)
            synced = await bot.tree.sync(guild=guild)

            print(
                f"[SLASH] Synced {len(synced)} commands "
                f"to {guild.name}"
            )

        except Exception as e:
            print(
                f"[SLASH ERROR] {guild.name}: {e}"
            )

    print("Auralis SMP is ONLINE!")
# ============================================================
# START
# ============================================================

async def main():

    await load_extensions()

    token = os.getenv("AURALIS_TOKEN")

    if not token:

        print("ERROR: AURALIS_TOKEN is not set.")

        return

    await bot.start(token)


import asyncio

asyncio.run(main())