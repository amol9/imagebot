import os
from os.path import join as joinpath, exists
import pickle
import sys
from scrapy import Request
from time import time, sleep
from scrapy.pipelines.images import ImagesPipeline
import logging as log

from imagebot.items import ImageItem
from imagebot.settings import settings
from imagebot.dbmanager import DBManager


#referermiddleware is a spider middleware, for requests generated from image pipeline, it does not set the referer
#so, we set it here
class ImagesRefererPipeline(ImagesPipeline):
	def get_media_requests(self, item, info):
		for image_url in item['image_urls']:
			yield Request(image_url, headers={'Referer': item['referer']})


class ImageStorePipeline(object):
	def __init__(self):
		if exists(settings.IMAGES_DB):
			self._dbm = DBManager(settings.IMAGES_DB)
			self._dbm.connect()
			self._nodb = False
			log.debug('opened db: %s'%settings.IMAGES_DB)
		else:
			self._nodb = True
			log.debug('could not open db: %s'%settings.IMAGES_DB)


	def process_item(self, item, spider):
		if isinstance(item, ImageItem):
			images = item.get('images', None)
			final_storepath = joinpath(settings.IMAGES_STORE_FINAL, spider.jobname)

			if images:
				for d in item['images']:
					ext = d['path'][d['path'].rfind('.')+1:]
					filebasename, ext = self.get_filename(d['url'])
					final_path = joinpath(final_storepath, filebasename + '.' + ext)
					i = 0
					while exists(final_path):
						log.debug(final_path + ' exists')
						final_path = joinpath(final_storepath, filebasename + '_%02d'%i + '.' + ext)
						i += 1

					try:
						os.rename(joinpath(settings.IMAGES_STORE, d['path']), final_path)
						log.debug('moved to: ' + final_path)
						spider.update_monitor(final_path)
						if not self._nodb:
							self._dbm.insert('images', (d['url'], final_path, spider.jobname, int(time())))
					except OSError as e:
						log.error(e)


		if not self._nodb:
			self._dbm.commit()
		return item


	def get_filename(self, url):
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
			pwords = [w for w in pwords if (len(w) > 0 and len(w) <= 2) or (len(w) > 2 and (len([c for c in w if (ord(c)>=48 and ord(c)<=57)]) < len(w)/2))]
			words = pwords + words

		
		final = ''
		if len(words) > 0:
			for w in words:
				final += w + '_'
			final = final.rstrip('_')
		else:
			final = 'image.'

		return final, ext

	
	def __del__(self):
		self._dbm.disconnect()


if __name__ == '__main__':
	isp = ImageStorePipeline()
	print(isp.get_filename(sys.argv[1]))
	
