"""DBHelper, MongoDB"""

from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import ASCENDING


class DB_Helper:
    """Сlass for convenient asynchronous interaction with MongoDB"""

    _instance = None

    def __new__(cls, *_args, **_kwargs):
        if not DB_Helper._instance:
            DB_Helper._instance = super(DB_Helper, cls).__new__(cls)
        return DB_Helper._instance

    def __init__(self):
        self._client = AsyncIOMotorClient()
        self._history_col = self._client.history_db.history_col
        self._history_col.create_index([("chat_id", ASCENDING)], unique=True)

    async def get_all_urls(self, chat_id):
        """Get user's urls by chat_id"""
        res = await self._history_col.find_one({"chat_id": chat_id})
        return res["urls"] if res is not None else None

    async def get_last_url(self, chat_id):
        """Get last url by chat_id"""
        urls = await self.get_all_urls(chat_id)
        return urls[-1] if urls is not None else None

    async def clean_history(self, chat_id):
        """Clean user's history"""
        await self._history_col.delete_one({"chat_id": chat_id})

    async def add_or_update_url(self, chat_id, url):
        """Add first/update user's urls"""
        await self._history_col.update_one(
            {"chat_id": chat_id}, {"$push": {"urls": url}}, upsert=True
        )
