import re
import os
from os.path import join as joinpath, expanduser
from os import remove
from shutil import rmtree
from hashlib import md5
from collections import namedtuple

from mutils.system import *
from mutils.web.urls import AbsUrl

from imagebot.settings import settings
from imagebot.dbmanager import DBManager


FileItem = namedtuple('FileItem', ['path', 'hash', 'dup'])


def remove_dir_contents(dirpath):
	prints('clearing dir: %s..'%dirpath)
	try:
		for root, dirs, files in os.walk(dirpath):
			for d in dirs:
				rmtree(joinpath(root, d))
			for f in files:
				remove(joinpath(root, f))
	except OSError as ose:
		print ose.message
	else:
		print('done')


def clear_cache():
	remove_dir_contents(expanduser(settings.HTTPCACHE_DIR))
	remove_dir_contents(expanduser(settings.IMAGES_STORE))


def clear_db(arg):
	def delete_from_db(condition=None):
		dbm = DBManager(expanduser(settings.IMAGES_DB))
		dbm.connect()
		count = dbm.delete('images', condition)
		dbm.commit()
		dbm.disconnect()
		return count

	count = 0
	if arg == 'ALL':
		input = raw_input('delete all image metadata? Y/n: ')
		if input == 'Y':
			count = delete_from_db()
		else:
			pass
	else:
		domain_regex = re.compile("(http(s)?://)?((((?!-)[A-Za-z0-9-]{1,63}(?<!-)\\.)+[A-Za-z]{2,6})|"
						"((?!-)[A-Za-z0-9-]{1,63}(?<!-)))")
		match = domain_regex.match(arg)
		domain = None

		if match:
			domain = match.groups()[2]
		else:
			domain = arg


		count = delete_from_db('job = \'%s\''%domain)

	print('metadata for %d image%s deleted'%(count, ('' if count == 1 else 's')))


def clear_duplicate_images(arg):
	dbm = DBManager(expanduser(settings.IMAGES_DB))
	dbm.connect()

	jobname = arg
	result = dbm.query('SELECT path FROM images WHERE job = \'%s\' LIMIT 1'%jobname)
	if len(result) == 0:
		print('no such job')

	imagepath = result[0]['path']
	jobpath = imagepath[0:imagepath.rfind(jobname)+len(jobname)]

	print jobpath

	filelist = []
	for root, dirs, files in os.walk(jobpath):
		for filename in files:
			md5hash = md5()
			filepath = joinpath(root, filename)
			with open(filepath, 'rb') as f:
				md5hash.update(f.read())
			filehash = md5hash.hexdigest()
			filelist.append(FileItem(filepath, filehash, False))

	dups_total = 0

	for i in range(0, len(filelist)):
		if filelist[i].dup:
			continue
		hash = filelist[i].hash
		same_files = [(filelist[i].path, os.stat(filelist[i].path).st_mtime)]
		for j in range(i + 1, len(filelist)):
			if filelist[j].hash == hash:
				same_files.append((filelist[j].path, os.stat(filelist[j].path).st_mtime))
				filelist[j] = FileItem(None, None, True)

		if len(same_files) > 1:
			min_mtime = sys.float_info.max
			keep = -1
			for i in range(0, len(same_files)):
				if same_files[i][1] < min_mtime:
					min_mtime = same_files[i][1]
					keep = i

			for i in range(0, len(same_files)):
				if i != keep:
					dups_total += 1
					print('deleting %s'%same_files[i][0])
					try:
						os.remove(same_files[i][0])
					except OSError as e:
						print(e.message)
				
					dbm.query('UPDATE images SET path = \'#duplicate\' WHERE path = \'%s\''%same_files[i][0])

	dbm.commit()
	dbm.disconnect()

	print('%d duplicate images deleted.'%dups_total)		
	
