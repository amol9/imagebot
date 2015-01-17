# -*- coding: utf-8 -*-

# Scrapy settings for image project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'imagebot'

SPIDER_MODULES = ['imagebot.spiders']
NEWSPIDER_MODULE = 'imagebot.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'imagebot'

ITEM_PIPELINES = {
	'imagebot.pipelines.ImagesRefererPipeline': 1,
	'imagebot.pipelines.ImageStorePipeline': 2
}

IMAGES_STORE = '/home/amol/projects/imagebot/data'
IMAGES_STORE_FINAL = '/home/amol/Pictures/crawled'
IMAGES_DB = 'images.db'

IMAGES_MIN_HEIGHT = 300
IMAGES_MIN_WIDTH = 300

DOWNLOADER_MIDDLEWARES = {
	'imagebot.middleware.ImageStoreMiddleware': 0,
	'imagebot.middleware.DebugMiddleware': 5000
}

LOG_ENABLED = True


HTTPCACHE_ENABLED = False
HTTPCACHE_POLICY = 'scrapy.contrib.httpcache.RFC2616Policy'

#DEPTH_LIMIT = 1
