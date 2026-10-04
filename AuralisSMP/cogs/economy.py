import random
import time

import discord

from discord import app_commands
from discord.ext import commands

from database import (
    get_user,
    get_balance,
    update_money,
    add_item
)


class Economy(commands.Cog):

    def __init__(self, bot):

        self.bot = bot


    # ========================================================
    # BALANCE
    # ========================================================

    @app_commands.command(
        name="balance",
        description="Check your balance."
    )
    async def balance(
        self,
        interaction: discord.Interaction
    ):

        user = await get_user(
            interaction.user.id,
            interaction.guild.id
        )

        embed = discord.Embed(
            title="💰 Auralis Wallet",
            color=discord.Color.gold()
        )

        embed.add_field(
            name="💵 Wallet",
            value=f"${user[2]:,}"
        )

        embed.add_field(
            name="🏦 Bank",
            value=f"${user[3]:,}"
        )

        await interaction.response.send_message(
            embed=embed
        )


    # ========================================================
    # DAILY
    # ========================================================

    @app_commands.command(
        name="daily",
        description="Claim your daily reward."
    )
    async def daily(
        self,
        interaction: discord.Interaction
    ):

        user = await get_user(
            interaction.user.id,
            interaction.guild.id
        )

        now = int(time.time())

        if now - user[7] < 86400:

            remaining = 86400 - (
                now - user[7]
            )

            hours = remaining // 3600

            minutes = (
                remaining % 3600
            ) // 60

            return await interaction.response.send_message(
                f"⏰ Come back in "
                f"**{hours}h {minutes}m**."
            )

        streak = user[6] + 1

        reward = 1000 + (
            streak * 250
        )

        import aiosqlite

        async with aiosqlite.connect(
            "auralis.db"
        ) as db:

            await db.execute("""
                UPDATE users

                SET balance = balance + ?,
                    daily_streak = ?,
                    last_daily = ?

                WHERE user_id = ?
                AND guild_id = ?
            """, (
                reward,
                streak,
                now,
                interaction.user.id,
                interaction.guild.id
            ))

            await db.commit()

        await interaction.response.send_message(
            f"🎁 **DAILY REWARD!**\n\n"
            f"💰 **${reward:,}**\n"
            f"🔥 Streak: **{streak}**"
        )


    # ========================================================
    # WORK
    # ========================================================

    @app_commands.command(
        name="work",
        description="Work for money."
    )
    async def work(
        self,
        interaction: discord.Interaction
    ):

        jobs = [
            ("💻 Developer", 300, 900),
            ("🎣 Fisher", 200, 700),
            ("⛏️ Miner", 250, 800),
            ("🍕 Pizza Delivery", 150, 500),
            ("🧑‍🍳 Chef", 300, 850),
            ("🐟 Fish Dealer", 350, 1000)
        ]

        job, minimum, maximum = random.choice(
            jobs
        )

        reward = random.randint(
            minimum,
            maximum
        )

        await update_money(
            interaction.user.id,
            interaction.guild.id,
            reward
        )

        await interaction.response.send_message(
            f"💼 You worked as a **{job}**!\n\n"
            f"💰 Earned **${reward:,}**"
        )


    # ========================================================
    # FISH
    # ========================================================

    @app_commands.command(
        name="fish",
        description="Go fishing."
    )
    async def fish(
        self,
        interaction: discord.Interaction
    ):

        fish = [
            ("🐟 Common Fish", 100),
            ("🐠 Tropical Fish", 300),
            ("🦈 Shark", 1000),
            ("🐋 Whale", 3000),
            ("🐙 Kraken", 10000),
            ("👑 Golden Fish", 25000)
        ]

        name, reward = random.choice(
            fish
        )

        reward = random.randint(
            reward // 2,
            reward
        )

        await update_money(
            interaction.user.id,
            interaction.guild.id,
            reward
        )

        await add_item(
            interaction.user.id,
            interaction.guild.id,
            name
        )

        await interaction.response.send_message(
            f"🎣 You caught **{name}**!\n\n"
            f"💰 Value: **${reward:,}**"
        )


    # ========================================================
    # COINFLIP
    # ========================================================

    @app_commands.command(
        name="coinflip",
        description="Flip a coin."
    )
    async def coinflip(
        self,
        interaction: discord.Interaction
    ):

        result = random.choice([
            "HEADS 🪙",
            "TAILS 🪙"
        ])

        await interaction.response.send_message(
            f"🪙 **{result}**"
        )


async def setup(bot):

    await bot.add_cog(
        Economy(bot)
    )