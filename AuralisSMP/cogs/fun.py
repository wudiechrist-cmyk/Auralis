import random

import discord

from discord import app_commands
from discord.ext import commands


class Fun(commands.Cog):

    def __init__(self, bot):

        self.bot = bot


    @app_commands.command(
        name="roll",
        description="Roll a random number."
    )
    async def roll(
        self,
        interaction: discord.Interaction,
        maximum: int = 100
    ):

        if maximum < 1:

            return await interaction.response.send_message(
                "❌ Maximum must be at least 1."
            )

        number = random.randint(
            1,
            maximum
        )

        await interaction.response.send_message(
            f"🎲 You rolled **{number} / {maximum}**!"
        )


    @app_commands.command(
        name="choose",
        description="Choose between two options."
    )
    async def choose(
        self,
        interaction: discord.Interaction,
        option1: str,
        option2: str
    ):

        choice = random.choice([
            option1,
            option2
        ])

        await interaction.response.send_message(
            f"🤔 I choose **{choice}**!"
        )


    @app_commands.command(
        name="ship",
        description="Calculate compatibility."
    )
    async def ship(
        self,
        interaction: discord.Interaction,
        user1: discord.Member,
        user2: discord.Member
    ):

        percentage = random.randint(
            0,
            100
        )

        await interaction.response.send_message(
            f"💘 **{user1.display_name} × "
            f"{user2.display_name}**\n\n"
            f"❤️ Compatibility: **{percentage}%**"
        )


    @app_commands.command(
        name="rate",
        description="Rate something."
    )
    async def rate(
        self,
        interaction: discord.Interaction,
        thing: str
    ):

        rating = random.randint(
            0,
            10
        )

        await interaction.response.send_message(
            f"📊 I'd rate **{thing}** "
            f"**{rating}/10**."
        )


async def setup(bot):

    await bot.add_cog(
        Fun(bot)
    )