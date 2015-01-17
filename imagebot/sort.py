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


class SortManager():
	def __init__(self):
		pass


	def generate_path(self, url)
		url_parts = [p for p in url.split('/') if p != '']
		del url_parts[0]
		del url_parts[-1]

		path = ''
		for i in sort_parts:
			if i < len(url_parts):
					path = joinpath(path, url_parts[i])

		path = unquote(path).replace(' ', '_')

		return path

	
	def generate_filename(url):
		url_parts = url.split('/')
		del url_parts[0:2]

		filename = url_parts.pop()
		ext = filename[filename.rfind('.')+1:]
		filename = filename[0:filename.rfind('.')]
		url_parts.append(filename)

		part = filename
		words = []
		while not any([len(w)>2 for w in words]) and len(url_parts) > 0:
			part = url_parts.pop()
			part = part.replace('-', '_').replace('.', '_').replace('+', '_')
			pwords = part.split('_')
			pwords = [w for w in pwords if (len(w) > 0 and len(w) <= 2) or \
					(len(w) > 2 and (len([c for c in w if (ord(c)>=48 and ord(c)<=57)]) < len(w)/2))]
			words = pwords + words

		
		final = ''
		if len(words) > 0:
			for w in words:
				final += w + '_'
			final = final.rstrip('_')
		else:
			final = 'image.'

		return final, ext



if __name__ == '__main__':
	#intelligent / parts
	
