from scrapy.exceptions import IgnoreRequest
from os.path import exists
import pickle
import logging as log

from imagebot.settings import settings
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
		#self._db.disconnect()
		pass


class DebugMiddleware(object):
	def process_request(self, request, spider):
		log.debug('reqdump-start')
		log.debug('url: %s'%request.url)
		log.debug(str(request.headers))
		log.debug('reqdump-end')
		return None
