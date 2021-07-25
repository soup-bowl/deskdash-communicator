import os
import tempfile
import sqlite3
from sqlite3 import Error

class Store(object):
	def __init__(self):
		self.dbf = os.path.join( tempfile.gettempdir(), 'deskdash-store.sqlite' )
		self.con = None
		self.cur = None

		self.new_connection()
		self.init_db()

	def __enter__(self):
		return self

	def __exit__(self, ext_type, exc_value, traceback):
		self.close_connection(self, exc_value)

	def new_connection(self):
		self.con = sqlite3.connect(self.dbf)
		self.cur = self.con.cursor()

	def close_connection(self, exc_value = None, blank = None):
		self.cur.close()
		if isinstance(exc_value, Exception):
			self.con.rollback()
		else:
			self.con.commit()
		self.con.close()	

	def init_db(self):
		self.cur.execute('''CREATE TABLE IF NOT EXISTS meta(id integer PRIMARY KEY, \
			key text,
			value text)''')
		
		return self.cur.fetchall()
	
	def get_metas(self, limit = 10):
		self.cur.execute("SELECT id, key, value FROM meta ORDER BY id DESC LIMIT ?", limit)

	def insert_meta(self, key, value):
		self.cur.execute("INSERT INTO meta VALUES (?, ?)", (key, value))

		return self.cur.lastrowid
	
	def insert_meta_bulk(self, dict):
		self.cur.executemany("INSERT INTO meta VALUES (?, ?)", dict)
