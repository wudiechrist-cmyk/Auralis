import discord

from discord import app_commands

from discord.ext import commands


class Moderation(commands.Cog):

    def __init__(self, bot):

        self.bot = bot


    # ========================================================
    # PERMISSION CHECK
    # ========================================================

    async def check_admin(self, interaction):

        if interaction.user.guild_permissions.administrator:

            return True

        await interaction.response.send_message(
            "❌ You need Administrator permission.",
            ephemeral=False
        )

        return False


    # ========================================================
    # KICK
    # ========================================================

    @app_commands.command(
        name="kick",
        description="Kick a member."
    )
    async def kick(
        self,
        interaction: discord.Interaction,
        member: discord.Member,
        reason: str = "No reason provided"
    ):

        if not await self.check_admin(interaction):

            return

        try:

            await member.kick(reason=reason)

            await interaction.response.send_message(
                f"👢 **{member}** was kicked.\n"
                f"Reason: **{reason}**"
            )

        except discord.Forbidden:

            await interaction.response.send_message(
                "❌ I cannot kick that member."
            )


    # ========================================================
    # BAN
    # ========================================================

    @app_commands.command(
        name="ban",
        description="Ban a member."
    )
    async def ban(
        self,
        interaction: discord.Interaction,
        member: discord.Member,
        reason: str = "No reason provided"
    ):

        if not await self.check_admin(interaction):

            return

        try:

            await member.ban(reason=reason)

            await interaction.response.send_message(
                f"🔨 **{member}** was banned.\n"
                f"Reason: **{reason}**"
            )

        except discord.Forbidden:

            await interaction.response.send_message(
                "❌ I cannot ban that member."
            )


    # ========================================================
    # TIMEOUT
    # ========================================================

    @app_commands.command(
        name="timeout",
        description="Timeout a member."
    )
    async def timeout(
        self,
        interaction: discord.Interaction,
        member: discord.Member,
        minutes: int,
        reason: str = "No reason provided"
    ):

        if not await self.check_admin(interaction):

            return

        if minutes <= 0:

            return await interaction.response.send_message(
                "❌ Minutes must be greater than 0."
            )

        duration = discord.utils.utcnow()

        duration += discord.timedelta(
            minutes=minutes
        )

        try:

            await member.timeout(
                duration,
                reason=reason
            )

            await interaction.response.send_message(
                f"⏰ **{member}** was timed out "
                f"for **{minutes} minutes**."
            )

        except discord.Forbidden:

            await interaction.response.send_message(
                "❌ I cannot timeout that member."
            )


    # ========================================================
    # PURGE
    # ========================================================

    @app_commands.command(
        name="purge",
        description="Delete messages."
    )
    async def purge(
        self,
        interaction: discord.Interaction,
        amount: int
    ):

        if not await self.check_admin(interaction):

            return

        if amount < 1 or amount > 100:

            return await interaction.response.send_message(
                "❌ Amount must be between 1 and 100."
            )

        await interaction.response.defer()

        deleted = await interaction.channel.purge(
            limit=amount
        )

        await interaction.followup.send(
            f"🧹 Deleted **{len(deleted)} messages**."
        )


async def setup(bot):

    await bot.add_cog(
        Moderation(bot)
    )