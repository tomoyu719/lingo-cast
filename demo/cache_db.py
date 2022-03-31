import json
import sqlite3
import os

from sentence_util import SentenceUtil

CACHE_DIR = 'db_cache'
MAX_PROCESS_SENTENCE_NUM = 200


# sqlite3.register_adapter(IntList, lambda l: ';'.join([str(i) for i in l]))
# sqlite3.register_converter("IntList", lambda s: [int(i) for i in s.split(';')])


class CacheDb():
    
    def __init__(self, language_code:str) -> None:
        self.language_code = language_code
        sqlite3.register_adapter(list, lambda l: ';'.join([str(i) for i in l]))
        sqlite3.register_converter('LIST', lambda s: [int(i) for i in s.split(bytes(b';'))])
        self.db_path = self._get_db_path()
        if not os.path.exists(self.db_path):
            self._create_db()
        
    def _get_db_path(self):
        name = self.language_code + '_' + 'cache.db'
        path = os.path.join(CACHE_DIR,  name)
        return path
        
    def _create_db(self):
        con = sqlite3.connect(self.db_path, detect_types=sqlite3.PARSE_DECLTYPES,isolation_level=None)         
        cur = con.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS caches(word TEXT UNIQUE, indices LIST)""")
        con.commit()

    def insert(self, word, ids):
        if self.is_word_exist(word) or len(ids) == 0:
            return
        con = sqlite3.connect(self.db_path, detect_types=sqlite3.PARSE_DECLTYPES,isolation_level=None)         
        cur = con.cursor()
        cur.execute("INSERT INTO caches VALUES (?, ?)", (word, ids))
        con.commit()

    def is_word_exist(self, word):
        con = sqlite3.connect(self.db_path, detect_types=sqlite3.PARSE_DECLTYPES,isolation_level=None)         
        cur = con.cursor()
        cur.execute("SELECT word FROM caches WHERE word=:word", {'word': word})
        return len(cur.fetchall()) > 0

    def fetch_ids_by_word(self, word):
        con = sqlite3.connect(self.db_path, detect_types=sqlite3.PARSE_DECLTYPES,isolation_level=None)         
        cur = con.cursor()
        cur.execute("SELECT indices FROM caches WHERE word=:word", {'word': word})
        ids = cur.fetchall()[0][0]
        return ids
