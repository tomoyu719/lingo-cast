import json
import sqlite3
import os
import time
from cache_db import CacheDb

from decode_wiki40b import  decode_wiki40b
from old.process_language_code import LanguageCode
from sentence_util import SentenceUtil

DB_DIR = 'db'
MAX_PROCESS_SENTENCE_NUM = 200
MAX_PROCESS_WIKI_SENTENCE_NUM = 100000


class SentenceDb():
    
    def __init__(self, language_code:str) -> None:
        self.language_code = language_code
        self.db_path = self._get_db_path()
        self.sentence_util = SentenceUtil(language_code)
        if not os.path.exists(self.db_path):
            self._create_db()
            self.insert_from_wiki40b(language_code) 
        self.cache_db =  CacheDb(language_code)

    def _get_db_path(self):
        db_file_name = self.language_code + '.db'
        db_path = os.path.join(DB_DIR, db_file_name)
        return db_path
        
    def _create_db(self ):
        con = sqlite3.connect(self.db_path, isolation_level=None)         
        cur = con.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS wiki_sentences(id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE, sentence TEXT)""")
        con.commit()
        
    def insert_from_wiki40b(self, language_code):
        con = sqlite3.connect(self.db_path, isolation_level=None)
        cur = con.cursor()
        decoder = decode_wiki40b(language_code)
        sentences = []
        for text in decoder:
            sentences += self.sentence_util.split_to_sentences(text)
            if len(sentences) > MAX_PROCESS_WIKI_SENTENCE_NUM:
                records = [(None, sent) for sent in sentences]
                cur.executemany("INSERT INTO wiki_sentences VALUES (?, ?)", records)
                sentences = []
        records = [(None, sent) for sent in sentences]
        cur.executemany("INSERT INTO wiki_sentences VALUES (?, ?)", records)
            
    def _fetch_sentences_by_many_ids(self, ids):
        sentences = []
        for id in ids:
            s = self._fetch_sentences_by_id(id)
            sentences.append(s)
            if len(sentences) > MAX_PROCESS_SENTENCE_NUM:
                break
        return sentences

    def _fetch_sentences_by_id(self, id):
        con = sqlite3.connect(self.db_path, isolation_level=None)
        cur = con.cursor()
        cur.execute('SELECT sentence FROM wiki_sentences WHERE id=:id', {"id": id})
        record = cur.fetchall()
        sentence = record[0][0]
        return sentence

    def fetch_sentences_contain_word(self, word):
        if self.cache_db.is_word_exist(word):
            ids = self.cache_db.fetch_ids_by_word(word)
            sentences = self._fetch_sentences_by_many_ids(ids)
            return sentences
        con = sqlite3.connect(self.db_path, isolation_level=None)
        cur = con.cursor()
        cur.execute("""SELECT * FROM wiki_sentences WHERE sentence LIKE :word""", {'word': '%'+word+'%'})
        records = [(id, sent) for id, sent in cur.fetchall() if word in self.sentence_util.tokenize_sentence(sent)]
        ids = [id for id, _ in records]
        sentences = [sent for _, sent in records]
        self.insert_cache_db(word, ids)
        return sentences[:MAX_PROCESS_SENTENCE_NUM]

    def fetch_ids_contain_word(self, word):
        if self.cache_db.is_word_exist(word):
            ids = self.cache_db.fetch_ids_by_word(word)
            return ids
        con = sqlite3.connect(self.db_path, isolation_level=None)
        cur = con.cursor()
        cur.execute("""SELECT * FROM wiki_sentences WHERE sentence LIKE :word""", {'word': '%'+word+'%'})
        records = [(id, sent) for id, sent in cur.fetchall() if word in self.sentence_util.tokenize_sentence(sent)]
        ids = [id for id, _ in records]
        self.insert_cache_db(word, ids)
        return ids

    def insert_cache_db(self, word, ids):
        self.cache_db.insert(word, ids)
            
    def fetch_sentences_contain_many_words(self, words):
        for i, word in enumerate(words):
            ids = self.fetch_ids_contain_word(word)
            if i == 0:
                ids_set = set(ids)
            else:
                ids_set = ids_set & set(ids)
        ids_contain_words = list(ids_set)
        sentences = self._fetch_sentences_by_many_ids(ids_contain_words)
        return sentences
