import discord
from discord.ext import commands
from datetime import datetime, timezone
import random
import time
import math


# ============================================================
# AURALIS SMP - UTILITY COG
# ============================================================

UTILITY_COMMANDS = [
    "help",
    "ping",
    "about",
    "botinfo",
    "uptime",
    "stats",
    "serverinfo",
    "members",
    "channels",
    "roles",
    "emojis",
    "stickers",
    "boosts",
    "userinfo",
    "avatar",
    "roleinfo",
    "channelinfo",
    "random",
    "choose",
    "coinflip",
    "roll",
    "8ball",
    "ship",
    "rate",
    "reverse",
    "length",
    "count",
    "calculate",
    "percentage",
    "time",
    "timestamp",
    "snowflake",
    "autorespond",
    "removeautorespond",
    "autoresponds",
]


class Utility(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.auto_responses = {}

    # ========================================================
    # HELP
    # ========================================================

    @commands.hybrid_command(
        name="help",
        description="Show Auralis SMP commands."
    )
    async def help(self, ctx):

        embed = discord.Embed(
            title="🌌 Auralis SMP",
            description="**Command Center**",
            color=discord.Color.blurple()
        )

        embed.add_field(
            name="🏓 Basic",
            value=(
                "`/ping`\n"
                "`/help`\n"
                "`/about`\n"
                "`/botinfo`\n"
                "`/uptime`\n"
                "`/stats`"
            ),
            inline=True
        )

        embed.add_field(
            name="🏠 Server",
            value=(
                "`/serverinfo`\n"
                "`/members`\n"
                "`/channels`\n"
                "`/roles`\n"
                "`/emojis`\n"
                "`/stickers`\n"
                "`/boosts`"
            ),
            inline=True
        )

        embed.add_field(
            name="👤 Users",
            value=(
                "`/userinfo`\n"
                "`/avatar`\n"
                "`/roleinfo`\n"
                "`/channelinfo`"
            ),
            inline=True
        )

        embed.add_field(
            name="🎲 Fun",
            value=(
                "`/random`\n"
                "`/choose`\n"
                "`/coinflip`\n"
                "`/roll`\n"
                "`/8ball`\n"
                "`/ship`\n"
                "`/rate`"
            ),
            inline=True
        )

        embed.add_field(
            name="🧮 Tools",
            value=(
                "`/calculate`\n"
                "`/percentage`\n"
                "`/reverse`\n"
                "`/length`\n"
                "`/count`\n"
                "`/time`\n"
                "`/timestamp`\n"
                "`/snowflake`"
            ),
            inline=True
        )

        embed.add_field(
            name="🤖 Auto Responses",
            value=(
                "`/autorespond`\n"
                "`/removeautorespond`\n"
                "`/autoresponds`"
            ),
            inline=True
        )

        embed.set_footer(
            text="Auralis SMP • Utility System"
        )

        await ctx.send(embed=embed)

    # ========================================================
    # BASIC
    # ========================================================

    @commands.hybrid_command(
        name="ping",
        description="Check bot latency."
    )
    async def ping(self, ctx):

        ms = round(self.bot.latency * 1000)

        await ctx.send(
            f"🏓 **Pong!** `{ms}ms`"
        )

    @commands.hybrid_command(
        name="about",
        description="About Auralis SMP."
    )
    async def about(self, ctx):

        embed = discord.Embed(
            title="🌌 Auralis SMP",
            description=(
                "A custom Discord management and "
                "utility bot."
            ),
            color=discord.Color.blurple()
        )

        embed.add_field(
            name="⚙️ Language",
            value="Python"
        )

        embed.add_field(
            name="📚 Library",
            value="discord.py"
        )

        embed.add_field(
            name="⌨️ Prefix",
            value="`!`"
        )

        embed.add_field(
            name="⚡ Commands",
            value="Prefix + Slash"
        )

        await ctx.send(embed=embed)

    @commands.hybrid_command(
        name="botinfo",
        description="Show Auralis bot information."
    )
    async def botinfo(self, ctx):

        embed = discord.Embed(
            title="🤖 Auralis Information",
            color=discord.Color.blurple()
        )

        embed.add_field(
            name="Servers",
            value=f"`{len(self.bot.guilds)}`",
            inline=True
        )

        embed.add_field(
            name="Users",
            value=f"`{len(self.bot.users)}`",
            inline=True
        )

        embed.add_field(
            name="Latency",
            value=f"`{round(self.bot.latency * 1000)}ms`",
            inline=True
        )

        await ctx.send(embed=embed)

    @commands.hybrid_command(
        name="uptime",
        description="Show bot uptime."
    )
    async def uptime(self, ctx):

        now = time.time()

        started = getattr(
            self.bot,
            "start_time",
            now
        )

        seconds = int(now - started)

        days, seconds = divmod(
            seconds,
            86400
        )

        hours, seconds = divmod(
            seconds,
            3600
        )

        minutes, seconds = divmod(
            seconds,
            60
        )

        await ctx.send(
            f"⏱️ **Uptime:** "
            f"`{days}d {hours}h {minutes}m {seconds}s`"
        )

    @commands.hybrid_command(
        name="stats",
        description="Show bot statistics."
    )
    async def stats(self, ctx):

        total_members = sum(
            guild.member_count or 0
            for guild in self.bot.guilds
        )

        embed = discord.Embed(
            title="📊 Auralis Statistics",
            color=discord.Color.blurple()
        )

        embed.add_field(
            name="🏠 Servers",
            value=f"`{len(self.bot.guilds)}`"
        )

        embed.add_field(
            name="👥 Members",
            value=f"`{total_members}`"
        )

        embed.add_field(
            name="⚡ Ping",
            value=f"`{round(self.bot.latency * 1000)}ms`"
        )

        await ctx.send(embed=embed)

    # ========================================================
    # SERVER
    # ========================================================

    @commands.hybrid_command(
        name="serverinfo",
        description="Show server information."
    )
    async def serverinfo(self, ctx):

        guild = ctx.guild

        if guild is None:
            return await ctx.send(
                "❌ This command can only be used in a server."
            )

        embed = discord.Embed(
            title=f"🏠 {guild.name}",
            color=discord.Color.blurple()
        )

        if guild.icon:
            embed.set_thumbnail(
                url=guild.icon.url
            )

        embed.add_field(
            name="🆔 ID",
            value=f"`{guild.id}`",
            inline=False
        )

        embed.add_field(
            name="👑 Owner",
            value=f"<@{guild.owner_id}>",
            inline=True
        )

        embed.add_field(
            name="👥 Members",
            value=f"`{guild.member_count}`",
            inline=True
        )

        embed.add_field(
            name="💬 Channels",
            value=f"`{len(guild.channels)}`",
            inline=True
        )

        embed.add_field(
            name="🎭 Roles",
            value=f"`{len(guild.roles)}`",
            inline=True
        )

        embed.add_field(
            name="😀 Emojis",
            value=f"`{len(guild.emojis)}`",
            inline=True
        )

        embed.add_field(
            name="🚀 Boosts",
            value=f"`{guild.premium_subscription_count}`",
            inline=True
        )

        await ctx.send(embed=embed)

    @commands.hybrid_command(
        name="members",
        description="Show server member statistics."
    )
    async def members(self, ctx):

        guild = ctx.guild

        humans = sum(
            1
            for member in guild.members
            if not member.bot
        )

        bots = sum(
            1
            for member in guild.members
            if member.bot
        )

        await ctx.send(
            f"👥 **Total:** `{guild.member_count}`\n"
            f"👤 **Humans:** `{humans}`\n"
            f"🤖 **Bots:** `{bots}`"
        )

    @commands.hybrid_command(
        name="channels",
        description="List server channels."
    )
    async def channels(self, ctx):

        guild = ctx.guild

        channels = [
            channel.mention
            for channel in guild.text_channels
        ]

        if not channels:
            return await ctx.send(
                "❌ No text channels found."
            )

        await ctx.send(
            embed=discord.Embed(
                title="💬 Server Channels",
                description="\n".join(channels[:50]),
                color=discord.Color.blurple()
            )
        )

    @commands.hybrid_command(
        name="roles",
        description="List server roles."
    )
    async def roles(self, ctx):

        guild = ctx.guild

        roles = [
            role.mention
            for role in reversed(guild.roles)
            if role != guild.default_role
        ]

        if not roles:
            return await ctx.send(
                "❌ No roles found."
            )

        await ctx.send(
            embed=discord.Embed(
                title="🎭 Server Roles",
                description="\n".join(roles[:50]),
                color=discord.Color.blurple()
            )
        )

    @commands.hybrid_command(
        name="emojis",
        description="List server emojis."
    )
    async def emojis(self, ctx):

        guild = ctx.guild

        if not guild.emojis:
            return await ctx.send(
                "😀 This server has no custom emojis."
            )

        await ctx.send(
            "😀 " + " ".join(
                str(emoji)
                for emoji in guild.emojis[:100]
            )
        )

    @commands.hybrid_command(
        name="stickers",
        description="List server stickers."
    )
    async def stickers(self, ctx):

        guild = ctx.guild

        if not guild.stickers:
            return await ctx.send(
                "🏷️ No stickers found."
            )

        text = "\n".join(
            f"• `{sticker.name}`"
            for sticker in guild.stickers
        )

        await ctx.send(
            embed=discord.Embed(
                title="🏷️ Server Stickers",
                description=text,
                color=discord.Color.blurple()
            )
        )

    @commands.hybrid_command(
        name="boosts",
        description="Show server boost information."
    )
    async def boosts(self, ctx):

        guild = ctx.guild

        await ctx.send(
            f"🚀 **Boosts:** `{guild.premium_subscription_count}`\n"
            f"⭐ **Level:** `{guild.premium_tier}`"
        )

    # ========================================================
    # USER
    # ========================================================

    @commands.hybrid_command(
        name="userinfo",
        description="Show information about a member."
    )
    async def userinfo(
        self,
        ctx,
        member: discord.Member = None
    ):

        member = member or ctx.author

        embed = discord.Embed(
            title=f"👤 {member}",
            color=discord.Color.blurple()
        )

        embed.set_thumbnail(
            url=member.display_avatar.url
        )

        embed.add_field(
            name="🆔 ID",
            value=f"`{member.id}`",
            inline=False
        )

        embed.add_field(
            name="🤖 Bot",
            value="Yes" if member.bot else "No"
        )

        embed.add_field(
            name="🎭 Roles",
            value=f"`{max(0, len(member.roles) - 1)}`"
        )

        embed.add_field(
            name="📅 Account Created",
            value=discord.utils.format_dt(
                member.created_at,
                style="F"
            ),
            inline=False
        )

        if member.joined_at:
            embed.add_field(
                name="📥 Joined Server",
                value=discord.utils.format_dt(
                    member.joined_at,
                    style="F"
                ),
                inline=False
            )

        await ctx.send(embed=embed)

    @commands.hybrid_command(
        name="avatar",
        description="Show a member's avatar."
    )
    async def avatar(
        self,
        ctx,
        member: discord.Member = None
    ):

        member = member or ctx.author

        embed = discord.Embed(
            title=f"🖼️ {member.display_name}'s Avatar",
            color=discord.Color.blurple()
        )

        embed.set_image(
            url=member.display_avatar.url
        )

        await ctx.send(embed=embed)

    @commands.hybrid_command(
        name="roleinfo",
        description="Show role information."
    )
    async def roleinfo(
        self,
        ctx,
        role: discord.Role
    ):

        embed = discord.Embed(
            title=f"🎭 {role.name}",
            color=role.color
        )

        embed.add_field(
            name="🆔 ID",
            value=f"`{role.id}`"
        )

        embed.add_field(
            name="👥 Members",
            value=f"`{len(role.members)}`"
        )

        embed.add_field(
            name="📊 Position",
            value=f"`{role.position}`"
        )

        await ctx.send(embed=embed)

    @commands.hybrid_command(
        name="channelinfo",
        description="Show channel information."
    )
    async def channelinfo(
        self,
        ctx,
        channel: discord.TextChannel = None
    ):

        channel = channel or ctx.channel

        embed = discord.Embed(
            title=f"💬 #{channel.name}",
            color=discord.Color.blurple()
        )

        embed.add_field(
            name="🆔 ID",
            value=f"`{channel.id}`"
        )

        embed.add_field(
            name="📁 Type",
            value=str(channel.type)
        )

        embed.add_field(
            name="📊 Position",
            value=f"`{channel.position}`"
        )

        await ctx.send(embed=embed)

    # ========================================================
    # FUN
    # ========================================================

    @commands.hybrid_command(
        name="random",
        description="Generate a random number."
    )
    async def random_number(
        self,
        ctx,
        minimum: int = 1,
        maximum: int = 100
    ):

        if minimum > maximum:
            minimum, maximum = maximum, minimum

        result = random.randint(
            minimum,
            maximum
        )

        await ctx.send(
            f"🎲 **{result}**"
        )

    @commands.hybrid_command(
        name="choose",
        description="Choose between multiple options."
    )
    async def choose(
        self,
        ctx,
        *,
        options: str
    ):

        choices = [
            x.strip()
            for x in options.split("|")
            if x.strip()
        ]

        if len(choices) < 2:
            return await ctx.send(
                "❌ Example: `!choose pizza | burger | noodles`"
            )

        await ctx.send(
            f"🎯 I choose **{random.choice(choices)}**!"
        )

    @commands.hybrid_command(
        name="coinflip",
        description="Flip a coin."
    )
    async def coinflip(self, ctx):

        result = random.choice(
            ["Heads", "Tails"]
        )

        await ctx.send(
            f"🪙 **{result}!**"
        )

    @commands.hybrid_command(
        name="roll",
        description="Roll a dice."
    )
    async def roll(
        self,
        ctx,
        sides: int = 6
    ):

        if sides < 2:
            return await ctx.send(
                "❌ Minimum is 2."
            )

        if sides > 1000000:
            return await ctx.send(
                "❌ Maximum is 1,000,000."
            )

        result = random.randint(
            1,
            sides
        )

        await ctx.send(
            f"🎲 You rolled **{result}** on a d{sides}!"
        )

    @commands.hybrid_command(
        name="8ball",
        description="Ask the magic 8-ball."
    )
    async def eightball(
        self,
        ctx,
        *,
        question: str
    ):

        answers = [
            "Yes.",
            "No.",
            "Definitely.",
            "Absolutely not.",
            "Probably.",
            "Probably not.",
            "Maybe.",
            "Ask again later.",
            "The stars say yes.",
            "The stars say no.",
            "I wouldn't count on it.",
            "Without a doubt.",
            "Very unlikely."
        ]

        await ctx.send(
            f"🎱 **{question}**\n"
            f"➡️ {random.choice(answers)}"
        )

    @commands.hybrid_command(
        name="ship",
        description="Calculate compatibility."
    )
    async def ship(
        self,
        ctx,
        member1: discord.Member,
        member2: discord.Member
    ):

        seed = (
            min(member1.id, member2.id),
            max(member1.id, member2.id)
        )

        rng = random.Random(seed)

        percentage = rng.randint(
            0,
            100
        )

        await ctx.send(
            f"💘 **{member1.display_name} + "
            f"{member2.display_name}**\n"
            f"❤️ **{percentage}% compatible**"
        )

    @commands.hybrid_command(
        name="rate",
        description="Rate something."
    )
    async def rate(
        self,
        ctx,
        *,
        thing: str
    ):

        rating = random.randint(
            0,
            100
        )

        await ctx.send(
            f"⭐ **{thing}** gets **{rating}/100**!"
        )

    # ========================================================
    # TEXT TOOLS
    # ========================================================

    @commands.hybrid_command(
        name="reverse",
        description="Reverse text."
    )
    async def reverse(
        self,
        ctx,
        *,
        text: str
    ):

        await ctx.send(
            f"🔄 `{text[::-1]}`"
        )

    @commands.hybrid_command(
        name="length",
        description="Count characters."
    )
    async def length(
        self,
        ctx,
        *,
        text: str
    ):

        await ctx.send(
            f"📏 **{len(text)} characters**"
        )

    @commands.hybrid_command(
        name="count",
        description="Count a word in text."
    )
    async def count(
        self,
        ctx,
        word: str,
        *,
        text: str
    ):

        amount = text.lower().count(
            word.lower()
        )

        await ctx.send(
            f"🔢 `{word}` appears "
            f"**{amount}** time(s)."
        )

    # ========================================================
    # MATH
    # ========================================================

    @commands.hybrid_command(
        name="calculate",
        description="Calculate a mathematical expression."
    )
    async def calculate(
        self,
        ctx,
        *,
        expression: str
    ):

        expression = expression.replace(
            "^",
            "**"
        )

        allowed = (
            "0123456789"
            "+-*/().% "
        )

        if any(
            char not in allowed
            for char in expression
        ):
            return await ctx.send(
                "❌ Invalid characters."
            )

        if len(expression) > 100:
            return await ctx.send(
                "❌ Expression is too long."
            )

        try:

            result = eval(
                expression,
                {
                    "__builtins__": {}
                },
                {}
            )

            if not isinstance(
                result,
                (int, float)
            ):
                return await ctx.send(
                    "❌ Invalid result."
                )

            if not math.isfinite(
                float(result)
            ):
                return await ctx.send(
                    "❌ Result isn't finite."
                )

            await ctx.send(
                f"🧮 **Result:** `{result}`"
            )

        except Exception:

            await ctx.send(
                "❌ Couldn't calculate that."
            )

    @commands.hybrid_command(
        name="percentage",
        description="Calculate a percentage."
    )
    async def percentage(
        self,
        ctx,
        number: float,
        percent: float
    ):

        result = number * (
            percent / 100
        )

        await ctx.send(
            f"🧮 **{percent}% of {number} = {result}**"
        )

    # ========================================================
    # TIME / DISCORD
    # ========================================================

    @commands.hybrid_command(
        name="time",
        description="Show current UTC time."
    )
    async def current_time(self, ctx):

        now = datetime.now(
            timezone.utc
        )

        await ctx.send(
            f"🕐 **UTC:** "
            f"`{now.strftime('%Y-%m-%d %H:%M:%S')}`"
        )

    @commands.hybrid_command(
        name="timestamp",
        description="Create a Discord timestamp."
    )
    async def timestamp(
        self,
        ctx,
        timestamp: int = None
    ):

        if timestamp is None:
            timestamp = int(
                time.time()
            )

        await ctx.send(
            f"🕐 `<t:{timestamp}:F>`\n"
            f"Preview: <t:{timestamp}:F>"
        )

    @commands.hybrid_command(
        name="snowflake",
        description="Decode a Discord snowflake."
    )
    async def snowflake(
        self,
        ctx,
        snowflake_id: int
    ):

        try:

            discord_epoch = 1420070400000

            timestamp_ms = (
                (snowflake_id >> 22)
                + discord_epoch
            )

            created = datetime.fromtimestamp(
                timestamp_ms / 1000,
                timezone.utc
            )

            await ctx.send(
                f"❄️ **ID:** `{snowflake_id}`\n"
                f"📅 **Created:** "
                f"{discord.utils.format_dt(created, style='F')}"
            )

        except Exception:

            await ctx.send(
                "❌ Invalid snowflake."
            )

    # ========================================================
    # AUTO RESPONSES
    # ========================================================

    @commands.hybrid_command(
        name="autorespond",
        description="Create an automatic response."
    )
    @commands.has_permissions(
        administrator=True
    )
    async def autorespond(
        self,
        ctx,
        message: str,
        *,
        response: str
    ):

        trigger = message.lower().strip()

        if not trigger:
            return await ctx.send(
                "❌ Trigger cannot be empty."
            )

        self.auto_responses[
            trigger
        ] = response

        await ctx.send(
            f"🤖 **Auto-response created!**\n"
            f"Trigger: `{trigger}`\n"
            f"Response: `{response}`"
        )

    @commands.hybrid_command(
        name="removeautorespond",
        description="Remove an automatic response."
    )
    @commands.has_permissions(
        administrator=True
    )
    async def removeautorespond(
        self,
        ctx,
        *,
        message: str
    ):

        trigger = message.lower().strip()

        if trigger not in self.auto_responses:
            return await ctx.send(
                "❌ That response doesn't exist."
            )

        del self.auto_responses[
            trigger
        ]

        await ctx.send(
            f"🗑️ Removed auto-response `{trigger}`."
        )

    @commands.hybrid_command(
        name="autoresponds",
        description="List automatic responses."
    )
    @commands.has_permissions(
        administrator=True
    )
    async def autoresponds(self, ctx):

        if not self.auto_responses:
            return await ctx.send(
                "🤖 No auto-responses configured."
            )

        lines = []

        for trigger, response in self.auto_responses.items():

            lines.append(
                f"• `{trigger}` → `{response}`"
            )

        embed = discord.Embed(
            title="🤖 Auto Responses",
            description="\n".join(lines),
            color=discord.Color.blurple()
        )

        await ctx.send(embed=embed)

    # ========================================================
    # MESSAGE LISTENER
    # ========================================================

    @commands.Cog.listener()
    async def on_message(self, message):

        if message.author.bot:
            return

        trigger = message.content.lower().strip()

        if trigger in self.auto_responses:

            try:

                await message.channel.send(
                    self.auto_responses[trigger]
                )

            except discord.Forbidden:
                pass

    # ========================================================
    # ERROR HANDLER
    # ========================================================

    @commands.Cog.listener()
    async def on_command_error(
        self,
        ctx,
        error
    ):

        if isinstance(
            error,
            commands.CommandNotFound
        ):
            return

        if isinstance(
            error,
            commands.MissingPermissions
        ):
            await ctx.send(
                "🔒 You need Administrator permission."
            )
            return

        if isinstance(
            error,
            commands.MissingRequiredArgument
        ):
            await ctx.send(
                f"❌ Missing argument: "
                f"`{error.param.name}`"
            )
            return

        if isinstance(
            error,
            commands.BadArgument
        ):
            await ctx.send(
                "❌ Invalid argument."
            )
            return

        if isinstance(
            error,
            commands.CommandInvokeError
        ):

            print(
                "[COMMAND ERROR]",
                error.original
            )

            await ctx.send(
                "❌ Something went wrong."
            )

            return

        print(
            "[UNHANDLED ERROR]",
            type(error).__name__,
            error
        )


# ============================================================
# SETUP
# ============================================================

async def setup(bot):

    # --------------------------------------------------------
    # Remove conflicting commands BEFORE loading this cog.
    # This prevents CommandAlreadyRegistered.
    # --------------------------------------------------------

    for command_name in UTILITY_COMMANDS:

        # Remove normal/prefix command
        existing = bot.get_command(
            command_name
        )

        if existing is not None:

            try:
                bot.remove_command(
                    command_name
                )

                print(
                    f"[UTILITY] Removed existing prefix "
                    f"command: {command_name}"
                )

            except Exception as error:

                print(
                    f"[UTILITY] Could not remove prefix "
                    f"{command_name}: {error}"
                )

        # Remove existing slash command
        try:

            removed = bot.tree.remove_command(
                command_name,
                type=discord.AppCommandType.chat_input
            )

            if removed is not None:

                print(
                    f"[UTILITY] Removed existing slash "
                    f"command: {command_name}"
                )

        except Exception as error:

            print(
                f"[UTILITY] Slash cleanup failed "
                f"for {command_name}: {error}"
            )

    await bot.add_cog(
        Utility(bot)
    )

    print(
        "[LOADED] cogs.utility"
    )