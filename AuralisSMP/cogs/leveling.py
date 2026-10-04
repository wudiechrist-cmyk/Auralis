import random

import discord

from discord.ext import commands

from database import get_user, add_xp


class Leveling(commands.Cog):

    def __init__(self, bot):

        self.bot = bot

        self.cooldowns = {}


    @commands.Cog.listener()
    async def on_message(self, message):

        if message.author.bot:
            return

        if message.guild is None:
            return

        key = (
            message.guild.id,
            message.author.id
        )

        now = discord.utils.utcnow().timestamp()

        if key in self.cooldowns:

            if now - self.cooldowns[key] < 30:

                return

        self.cooldowns[key] = now

        xp = random.randint(10, 25)

        levelups, level = await add_xp(
            message.author.id,
            message.guild.id,
            xp
        )

        if levelups:

            await message.channel.send(
                f"🎉 {message.author.mention} "
                f"reached **Level {level}**! 🚀"
            )


    @commands.hybrid_command(
        name="rank",
        description="Check your level."
    )
    async def rank(self, ctx):

        user = await get_user(
            ctx.author.id,
            ctx.guild.id
        )

        level = user[5]
        xp = user[4]

        required = level * 500

        await ctx.send(
            f"📈 **{ctx.author.display_name}**\n\n"
            f"⭐ Level: **{level}**\n"
            f"✨ XP: **{xp:,} / {required:,}**"
        )


async def setup(bot):

    await bot.add_cog(
        Leveling(bot)
    )