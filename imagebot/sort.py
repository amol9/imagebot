from dbmanager import DBManager
import sys
from os.path import join as joinpath
from urllib import unquote


sort_parts = [1, 2, 3]
job = 'default'

if len(sys.argv) >= 3:
	job = sys.argv[1]
	sort_parts = [int(i) for i in sys.argv[2].split(',')]
	#print sort_parts


db = DBManager('../images.db')
db.connect()

result = db.query("SELECT url FROM images WHERE job = '%s' LIMIT 100"%job)

for r in result:
	url = r['url']
	#jobname = r['jobname']
	path = job

	url_parts = [p for p in url.split('/') if p != '']
	del url_parts[0]
	del url_parts[-1]
	#print url_parts

	for i in sort_parts:
		if i < len(url_parts):
				path = joinpath(path, url_parts[i])

	path = unquote(path).replace(' ', '_')
	print url
	print path
	print '-'

db.disconnect()
	
