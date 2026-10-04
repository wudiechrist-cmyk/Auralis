import random

import discord

from discord import app_commands
from discord.ext import commands


class Games(commands.Cog):

    def __init__(self, bot):

        self.bot = bot


    @app_commands.command(
        name="dice",
        description="Roll a dice."
    )
    async def dice(
        self,
        interaction: discord.Interaction
    ):

        number = random.randint(1, 6)

        await interaction.response.send_message(
            f"🎲 You rolled **{number}**!"
        )


    @app_commands.command(
        name="rps",
        description="Play rock paper scissors."
    )
    @app_commands.describe(
        choice="Your choice"
    )
    @app_commands.choices(
        choice=[
            app_commands.Choice(
                name="Rock 🪨",
                value="rock"
            ),
            app_commands.Choice(
                name="Paper 📄",
                value="paper"
            ),
            app_commands.Choice(
                name="Scissors ✂️",
                value="scissors"
            )
        ]
    )
    async def rps(
        self,
        interaction: discord.Interaction,
        choice: app_commands.Choice[str]
    ):

        bot_choice = random.choice([
            "rock",
            "paper",
            "scissors"
        ])

        if choice.value == bot_choice:

            result = "🤝 Draw!"

        elif (
            (choice.value == "rock" and bot_choice == "scissors")
            or
            (choice.value == "paper" and bot_choice == "rock")
            or
            (choice.value == "scissors" and bot_choice == "paper")
        ):

            result = "🎉 You win!"

        else:

            result = "💀 You lose!"

        emojis = {
            "rock": "🪨",
            "paper": "📄",
            "scissors": "✂️"
        }

        await interaction.response.send_message(
            f"**You:** {emojis[choice.value]}\n"
            f"**Auralis:** {emojis[bot_choice]}\n\n"
            f"{result}"
        )


    @app_commands.command(
        name="slots",
        description="Play slots."
    )
    async def slots(
        self,
        interaction: discord.Interaction
    ):

        symbols = [
            "🍒",
            "🍋",
            "🍊",
            "🍉",
            "💎",
            "7️⃣"
        ]

        result = [
            random.choice(symbols),
            random.choice(symbols),
            random.choice(symbols)
        ]

        text = " | ".join(result)

        if len(set(result)) == 1:

            outcome = "🎉 **JACKPOT!**"

        elif len(set(result)) == 2:

            outcome = "✨ **Two matching!**"

        else:

            outcome = "💀 **You lost!**"

        await interaction.response.send_message(
            f"🎰 **SLOTS**\n\n"
            f"**{text}**\n\n"
            f"{outcome}"
        )


    @app_commands.command(
        name="8ball",
        description="Ask the Auralis 8-ball."
    )
    async def eightball(
        self,
        interaction: discord.Interaction,
        question: str
    ):

        answers = [
            "Absolutely.",
            "Definitely.",
            "Probably.",
            "Maybe.",
            "Ask again later.",
            "Probably not.",
            "No.",
            "The Auralis gods have spoken: NO."
        ]

        await interaction.response.send_message(
            f"🎱 **{random.choice(answers)}**"
        )


async def setup(bot):

    await bot.add_cog(
        Games(bot)
    )