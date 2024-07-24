import os
from loguru import logger
from tortoise import Tortoise


class Database:
    DB_URL = "sqlite://settings/database/bot.db"
    DB_MODEL = {"models": [os.path.join("src.utils")]}

    async def database_connect(self):
        try:
            await Tortoise.init(db_url=self.DB_URL, modules=self.DB_MODEL)
            await Tortoise.generate_schemas()
            logger.info("Database connected")

        except Exception as e:
            logger.error(f"Ошибка подключение к базе данных\n╰─> Ошибка: {e}")

    async def database_close(self):
        await Tortoise.close_connections()
        logger.error("Database disconnected")
