import sqlite3
from sqlite3 import OperationalError, IntegrityError
import pprint

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
			print 'error connecting to db'

		return success


	def disconnect(self):
		self.conn.close()
		return


	def query(self, query_string):
		r = None
		try:
			c = self.conn.cursor()
			r = c.execute(query_string)
		except OperationalError, oe:
			print 'Error: ', oe.message
		return c.fetchall()


	def insert(self, tablename, values):
		try:
			c = self.conn.cursor()

			col_count = len(values)
			param_string = '?'
			for i in range(1, col_count):
				param_string += ',?'
			
			r = c.execute('INSERT INTO ' + tablename + ' VALUES (' + param_string + ')', values)
		except OperationalError, oe:
			print 'Error: ', oe.message	
		except IntegrityError, ie:
			print 'x',
		return 


	def update(self, tablename, values, cond=None):
		try:
			c = self.conn.cursor()

			query = 'UPDATE ' + tablename + ' SET '
			cols = 0
			for col, _ in values.items():
				query += ', ' if cols > 0 else ''
				query += col + ' = ?'
				cols += 1
			query += ' WHERE ' + cond if cond != None else ''
			r = c.execute(query, values.values())
		except OperationalError, oe:
			print 'Error: ', oe.message
		return

	
	def delete(self, tablename, cond):
		return


	def execute(self, query):
		try:
			c = self.conn.cursor()
			r = c.execute(query)
		except OperationalError, oe:
			print 'Error: ', oe.message
		except IntegrityError, ie:
			print 'Error: ', ie.message
			raise ie
		self.commit()
		return


	def executescript(self, script):
		try:
			c = self.conn.cursor()
			r = c.executescript(script)
		except OperationalError, oe:
			print 'Error: ', oe.message
		except IntegrityError, ie:
			print 'Error: ', ie.message
		self.commit()
		return


	def commit(self):
		try:
			self.conn.commit()
		except:
			print 'Commit Error'

		return


if __name__ == '__main__':
	dbm = DBManager('../db/db1.sqlite')
	dbm.connect()

	try:
		#vals = ('e11', 'Nick M', 'NY')
		#pprint.pprint(vals)
		#dbm.insert('Employee', vals)
		dbm.update('Employee', {'name': 'ASAC Hank S', 'deleted': 1}, "id = \'e03\'")
		dbm.commit()
	except IntegrityError, ie:
		print 'Insert error'
	
	for row in dbm.query('SELECT * FROM Employee'):
		print row[1]
		
	dbm.disconnect()
