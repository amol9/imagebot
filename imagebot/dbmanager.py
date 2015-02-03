import sqlite3
from sqlite3 import OperationalError, IntegrityError


class DBManager():
	
	def __init__(self, db_filename):
		self.conn = None
		self.db_filename = db_filename

	
	def connect(self):
		success = False
	
		try:
			#add: a check if file exists
			self.conn = sqlite3.connect(self.db_filename)
			success = True
			self.conn.row_factory = sqlite3.Row
		except:
			print('error connecting to db')

		return success


	def disconnect(self):
		self.conn.close()
		return


	def query(self, query_string):
		r = None
		try:
			c = self.conn.cursor()
			r = c.execute(query_string)
		except OperationalError as oe:
			print('Error: ', oe.message)
		return c.fetchall()


	def insert(self, tablename, values):
		try:
			c = self.conn.cursor()

			col_count = len(values)
			param_string = '?'
			for i in range(1, col_count):
				param_string += ',?'
			
			r = c.execute('INSERT INTO ' + tablename + ' VALUES (' + param_string + ')', values)
		except OperationalError as oe:
			print('Error: %s'%oe.message)	
		except IntegrityError as ie:
			print('Error: %s'%ie.message)
		return 


	def update(self, tablename, values, cond=None):
		try:
			c = self.conn.cursor()

			query = 'UPDATE ' + tablename + ' SET '
			cols = 0
			for col, _ in list(values.items()):
				query += ', ' if cols > 0 else ''
				query += col + ' = ?'
				cols += 1
			query += ' WHERE ' + cond if cond != None else ''
			r = c.execute(query, list(values.values()))
		except OperationalError as oe:
			print('Error: ', oe.message)
		return

	
	def delete(self, tablename, cond):
		r = None
		try:
			c = self.conn.cursor()
			r = c.execute('DELETE FROM %s %s'%(tablename, ('WHERE %s'%cond if cond is not None else '')))
		except OperationalError as oe:
			print('Error: ', oe.message)
		return r.rowcount


	def execute(self, query):
		try:
			c = self.conn.cursor()
			r = c.execute(query)
		except OperationalError as oe:
			print('Error: ', oe.message)
		except IntegrityError as ie:
			print('Error: ', ie.message)
			raise ie
		self.commit()
		return


	def executescript(self, script):
		try:
			c = self.conn.cursor()
			r = c.executescript(script)
		except OperationalError as oe:
			print('Error: ', oe.message)
		except IntegrityError as ie:
			print('Error: ', ie.message)
		self.commit()
		return


	def commit(self):
		try:
			self.conn.commit()
		except:
			print('Commit Error')

		return

