import asyncio

import aiomysql


class AsyncMySQLConnector:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.pool = None

    async def connect(self):
        self.pool = await aiomysql.create_pool(
            host=self.host,
            user=self.user,
            password=self.password,
            db=self.database,
            autocommit=True
        )

    async def disconnect(self):
        if self.pool:
            self.pool.close()
            await self.pool.wait_closed()

    async def insert_data(self, table, data):
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                placeholders = ', '.join(['%s'] * len(data))
                columns = ', '.join(data.keys())
                sql = f'INSERT INTO `{table}` ({columns}) VALUES ({placeholders});'
                await cursor.execute(sql, list(data.values()))

    async def select_data(self, table, columns=None, where=None):
        async with self.pool.acquire() as conn:
            async with conn.cursor(aiomysql.DictCursor) as cursor:
                if columns:
                    columns = ', '.join(columns)
                else:
                    columns = '*'
                sql = f"SELECT {columns} FROM {table}"
                if where:
                    conditions = ' AND '.join([f'{k}=%s' for k in where.keys()])
                    sql += f' WHERE {conditions}'
                    await cursor.execute(sql, list(where.values()))
                else:
                    await cursor.execute(sql)
                rows = await cursor.fetchall()
                return rows


async def main():
    connector = AsyncMySQLConnector(host='localhost', user='root', password='ubuntu', database='bot')
    await connector.connect()
    print("connect")

    data = {'group_id': 1, 'group_name': 'name', }
    await connector.insert_data('Groups', data)
    print("data")

    await connector.disconnect()

# asyncio.run(main())
