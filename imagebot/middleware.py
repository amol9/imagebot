#from scrapy.contrib.downloadermiddleware import DownloaderMiddleware
from scrapy.exceptions import IgnoreRequest
import anydbm
from os.path import exists
import pickle

import imagebot.settings as settings
from imagebot.dbmanager import DBManager


class ImageStoreMiddleware(object):
	def __init__(self):
		if exists(settings.IMAGES_DB):
			self._dbm = DBManager(settings.IMAGES_DB)
			self._dbm.connect()
			self._nodb = False
		else:
			self._nodb = True


	def find_url(self, url):
		result = self._dbm.query("SELECT * FROM images WHERE url = '%s'"%url)
		if len(result) > 0:
			return True
		return False


	def process_request(self, request, spider):
		if self._nodb:
			return None

		if self.find_url(request.url):
			raise IgnoreRequest

		return None


	def __del__(self):
		self._db.disconnect()	

