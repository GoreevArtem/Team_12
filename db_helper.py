import pymongo


class DB_Helper:
    _instance = None

    def __new__(cls, *_args, **_kwargs):
        if not DB_Helper._instance:
            DB_Helper._instance = super(DB_Helper, cls).__new__(cls)
        return DB_Helper._instance

    def __init__(self):
        self._client = pymongo.MongoClient()
        self._history_col = self._client.history_db.history_col
        self._history_col.create_index([('chat_id', pymongo.ASCENDING)],
                                       unique=True)

    def get_all_urls(self, chat_id):
        res = self._history_col.find_one({'chat_id': chat_id})
        return res['urls'] if res is not None else None

    def get_last_url(self, chat_id):
        urls = self.get_all_urls(chat_id)
        return urls[-1] if urls is not None else None

    def clean_history(self, chat_id):
        self._history_col.delete_one({'chat_id': chat_id})

    def add_or_update_url(self, chat_id, url):
        self._history_col.update_one({'chat_id': chat_id},
                                     {'$push': {'urls': url}}, upsert=True)
