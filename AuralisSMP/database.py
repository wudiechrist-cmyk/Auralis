import aiosqlite

DB_FILE = "auralis.db"


async def init_database():

    async with aiosqlite.connect(DB_FILE) as db:

        # =========================
        # USERS
        # =========================

        await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER NOT NULL,
                guild_id INTEGER NOT NULL,

                balance INTEGER DEFAULT 500,
                bank INTEGER DEFAULT 0,

                xp INTEGER DEFAULT 0,
                level INTEGER DEFAULT 1,

                daily_streak INTEGER DEFAULT 0,
                last_daily INTEGER DEFAULT 0,

                fish INTEGER DEFAULT 0,

                PRIMARY KEY (user_id, guild_id)
            )
        """)

        # =========================
        # INVENTORY
        # =========================

        await db.execute("""
            CREATE TABLE IF NOT EXISTS inventory (
                user_id INTEGER NOT NULL,
                guild_id INTEGER NOT NULL,

                item TEXT NOT NULL,
                amount INTEGER DEFAULT 0,

                PRIMARY KEY (user_id, guild_id, item)
            )
        """)

        # =========================
        # WARNINGS
        # =========================

        await db.execute("""
            CREATE TABLE IF NOT EXISTS warnings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,

                user_id INTEGER NOT NULL,
                guild_id INTEGER NOT NULL,

                moderator_id INTEGER NOT NULL,

                reason TEXT,
                timestamp INTEGER
            )
        """)

        await db.commit()


# ============================================================
# USER
# ============================================================

async def get_user(user_id, guild_id):

    async with aiosqlite.connect(DB_FILE) as db:

        cursor = await db.execute("""
            SELECT *
            FROM users
            WHERE user_id = ?
            AND guild_id = ?
        """, (
            user_id,
            guild_id
        ))

        user = await cursor.fetchone()

        if user is None:

            await db.execute("""
                INSERT INTO users
                (user_id, guild_id)
                VALUES (?, ?)
            """, (
                user_id,
                guild_id
            ))

            await db.commit()

            cursor = await db.execute("""
                SELECT *
                FROM users
                WHERE user_id = ?
                AND guild_id = ?
            """, (
                user_id,
                guild_id
            ))

            user = await cursor.fetchone()

        return user


# ============================================================
# MONEY
# ============================================================

async def get_balance(user_id, guild_id):

    user = await get_user(
        user_id,
        guild_id
    )

    return user[2]


async def update_money(user_id, guild_id, amount):

    await get_user(
        user_id,
        guild_id
    )

    async with aiosqlite.connect(DB_FILE) as db:

        await db.execute("""
            UPDATE users

            SET balance = balance + ?

            WHERE user_id = ?
            AND guild_id = ?
        """, (
            amount,
            user_id,
            guild_id
        ))

        await db.commit()


# ============================================================
# XP
# ============================================================

async def add_xp(user_id, guild_id, amount):

    user = await get_user(
        user_id,
        guild_id
    )

    xp = user[4]
    level = user[5]

    xp += amount

    levelups = 0

    while xp >= level * 500:

        xp -= level * 500

        level += 1

        levelups += 1

    async with aiosqlite.connect(DB_FILE) as db:

        await db.execute("""
            UPDATE users

            SET xp = ?,
                level = ?

            WHERE user_id = ?
            AND guild_id = ?
        """, (
            xp,
            level,
            user_id,
            guild_id
        ))

        await db.commit()

    return levelups, level


# ============================================================
# INVENTORY
# ============================================================

async def add_item(
    user_id,
    guild_id,
    item,
    amount=1
):

    await get_user(
        user_id,
        guild_id
    )

    async with aiosqlite.connect(DB_FILE) as db:

        await db.execute("""
            INSERT INTO inventory
            (user_id, guild_id, item, amount)

            VALUES (?, ?, ?, ?)

            ON CONFLICT(user_id, guild_id, item)

            DO UPDATE SET
            amount = amount + excluded.amount
        """, (
            user_id,
            guild_id,
            item,
            amount
        ))

        await db.commit()


async def get_inventory(
    user_id,
    guild_id
):

    await get_user(
        user_id,
        guild_id
    )

    async with aiosqlite.connect(DB_FILE) as db:

        cursor = await db.execute("""
            SELECT item, amount

            FROM inventory

            WHERE user_id = ?
            AND guild_id = ?

            AND amount > 0

            ORDER BY amount DESC
        """, (
            user_id,
            guild_id
        ))

        return await cursor.fetchall()