import aiosqlite

class Users:
    async def add_user(self, user_id, lang):
        async with aiosqlite.connect('database/users.db') as connection:
            async with connection.cursor() as cursor:
                await cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
                data = await cursor.fetchone()

                if data is None:
                    await cursor.execute("INSERT INTO users (user_id, lang) VALUES (?, ?)", (user_id, lang,))
                    await connection.commit()
                    return True

                await cursor.execute("UPDATE users SET lang = ? WHERE user_id = ?", (lang, user_id,))
                await connection.commit()
                return False

    async def get_language(self, user_id):
        async with aiosqlite.connect('database/users.db') as connection:
            async with connection.cursor() as cursor:
                await cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
                data = await cursor.fetchone()
                
                if data is None:
                    return None
                
                return data[2]

class UserWallet:
    async def set_wallet(self, user_id, address, private):
        async with aiosqlite.connect('database/users.db') as connection:
            async with connection.cursor() as cursor:
                await cursor.execute("SELECT * FROM wallets WHERE user_id = ?", (user_id,))
                data = await cursor.fetchone()

                if data is None:
                    await cursor.execute("INSERT INTO wallets (user_id, address, private) VALUES (?, ?, ?)", (user_id, address, private,))
                    await connection.commit()
                    return True

                return False

    async def get_address(self, user_id):
        async with aiosqlite.connect('database/users.db') as connection:
            async with connection.cursor() as cursor:
                await cursor.execute("SELECT address FROM wallets WHERE user_id = ?", (user_id,))
                data = await cursor.fetchone()
                
                if data is None:
                    return None
                
                return data[0]

    async def get_private(self, user_id):
        async with aiosqlite.connect('database/users.db') as connection:
            async with connection.cursor() as cursor:
                await cursor.execute("SELECT private FROM wallets WHERE user_id = ?", (user_id,))
                data = await cursor.fetchone()
                
                if data is None:
                    return None
                
                return data[0]