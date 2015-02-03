import re
import os
from os.path import join as joinpath, expanduser
from os import remove
from shutil import rmtree 

import imagebot.settings as settings
from imagebot.dbmanager import DBManager
from imagebot.system import *


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

