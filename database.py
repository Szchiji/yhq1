import aiosqlite

DB_PATH = "bot_data.db"

class Database:
    def __init__(self):
        self.db = None

    async def connect(self):
        self.db = await aiosqlite.connect(DB_PATH)
        await self.create_tables()

    async def create_tables(self):
        await self.db.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                chat_id INTEGER NOT NULL,
                type TEXT NOT NULL,
                content TEXT,
                media_file_id TEXT,
                buttons TEXT,
                interval INTEGER,
                start_time TEXT,
                end_time TEXT
            )
        """)
        await self.db.commit()

    async def add_task(self, task_data: dict):
        query = """INSERT INTO tasks (chat_id, type, content, media_file_id, buttons, interval, start_time, end_time)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?)"""
        await self.db.execute(query, (
            task_data["chat_id"],
            task_data["type"],
            task_data.get("content"),
            task_data.get("media_file_id"),
            task_data.get("buttons"),
            task_data.get("interval"),
            task_data.get("start_time"),
            task_data.get("end_time"),
        ))
        await self.db.commit()

    async def get_tasks(self, chat_id: int):
        cursor = await self.db.execute("SELECT * FROM tasks WHERE chat_id = ?", (chat_id,))
        rows = await cursor.fetchall()
        return rows

    async def delete_task(self, task_id: int):
        await self.db.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        await self.db.commit()

    async def close(self):
        await self.db.close()

db = Database()
