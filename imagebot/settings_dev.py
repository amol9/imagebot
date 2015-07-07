from os.path import join as joinpath, expanduser
import logging

BOT_NAME = 'imagebot'
DATA_DIR = '.imagebot'
HOME_DIR = expanduser('~')

SPIDER_MODULES = ['imagebot.spiders']
NEWSPIDER_MODULE = 'imagebot.spiders'

#crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'imagebot'

ITEM_PIPELINES = {
	'imagebot.pipelines.ImagesRefererPipeline': 1,
	'imagebot.pipelines.ImageStorePipeline': 2
}

IMAGES_STORE = joinpath(HOME_DIR, DATA_DIR, 'data')
IMAGES_STORE_FINAL = joinpath(HOME_DIR, 'Pictures/crawled')
IMAGES_DB = joinpath(HOME_DIR, DATA_DIR, 'images.db')

IMAGES_MIN_HEIGHT = 300
IMAGES_MIN_WIDTH = 300

DOWNLOADER_MIDDLEWARES = {
	'imagebot.middleware.ImageStoreMiddleware': 0,
	'imagebot.middleware.DebugMiddleware': 5000
}

LOG_ENABLED = True
LOG_LEVEL = logging.DEBUG

HTTPCACHE_ENABLED = True
HTTPCACHE_POLICY = 'scrapy.extensions.httpcache.RFC2616Policy'
HTTPCACHE_DIR = joinpath(HOME_DIR, DATA_DIR, 'httpcache')

DEPTH_LIMIT = 0

