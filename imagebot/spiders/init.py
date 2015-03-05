#helper module for initializing Imagebot
from os.path import join as joinpath, exists, expanduser, realpath, dirname
from os import mkdir, makedirs, sep
from multiprocessing import Process, Pipe
from scrapy import log
from scrapy.contrib.spiders import Rule
from scrapy.contrib.linkextractors import LinkExtractor
from PIL import Image

from imagebot.common.web.urls import AbsUrl
from imagebot.dbmanager import DBManager
from imagebot.settings import settings
from imagebot.common.web.cdns import cdns
from imagebot.monitor import get_monitor, MonitorException


def process_kwargs(bot, kwargs):
	bot._jobname = 'default'
	bot._inpipe = None

	images_store = kwargs.get('images_store')
	if images_store is not None:
		settings.IMAGES_STORE_FINAL = images_store

	start_urls = kwargs.get('start_urls', None)
	if start_urls:
		urls = [u.strip() for u in start_urls.split(',') if len(u.strip()) > 0]
		
		if any([not u.startswith('http') for u in urls]):
			log.msg('missing url scheme, (http/https)?', log.ERROR)
			return

		kwargs['start_urls'] = urls
		log.msg('start urls: \n' + '\n'.join(urls), log.DEBUG)

		allowed_domains = list(set([AbsUrl(u).domain for u in urls]))
		bot.allowed_domains = allowed_domains
	else:
		log.msg('must provide start url(s)', log.ERROR)
		return

	domains = kwargs.get('domains', None)
	if domains:
		domains = [d.strip() for d in domains.split(',')]
		bot.allowed_domains.extend(domains)
	
	log.msg('allowed domains: \n' + ', '.join(bot.allowed_domains), log.DEBUG)

	bot.allowed_image_domains = bot.allowed_domains
	if not kwargs['no_cdns']:
		bot.allowed_image_domains.extend(cdns)

	log.msg('allowed image domains: \n' + ', '.join(bot.allowed_image_domains), log.DEBUG)

	bot._jobname = bot.allowed_domains[0]

	jobname = kwargs.get('jobname', None)
	if jobname:
		bot._jobname = jobname

	stay_under = kwargs.get('stay_under', None)
	if stay_under:
		bot.rules = ()
		for start_url in kwargs['start_urls']:
			base_url = AbsUrl(start_url)
			def make_abs(url):
				if not url.startswith('http'):
					return base_url.extend(url)
			bot.rules +=((Rule(LinkExtractor(allow=(start_url + '.*',)), callback='parse_item', follow=True),))
		log.msg('staying under: %s'%start_urls, log.DEBUG)

	if kwargs['monitor']:
		try:
			bot._inpipe, outpipe = Pipe()
			mon_start_func = get_monitor()
			monitor_process = Process(target=mon_start_func, args=(outpipe,))
			monitor_process.start()
		except MonitorException:
			log.msg('will not start monitor ui', log.ERROR)

	if kwargs['user_agent']:
		settings.USER_AGENT = kwargs['user_agent']

	if kwargs['minsize']:
		settings.IMAGES_MIN_WIDTH, settings.IMAGES_MIN_HEIGHT = kwargs['minsize']

	if kwargs['no_cache']:
		settings.HTTPCACHE_ENABLED = False

	if kwargs['depth_limit']:
		depth_limit = int(kwargs['depth_limit'])
		'''if depth_limit == 0:
			bot.rules = (Rule(LinkExtractor(allow=(start_url + '.*',), callback='parse_item', follow=False),))
		else:'''
		settings.DEPTH_LIMIT = depth_limit

	if kwargs['url_regex']:
		bot.rules = (Rule(LinkExtractor(allow=kwargs['url_regex'],), callback='parse_item', follow=True),)

	'''if kwargs['download_delay']:
		log.msg('download delay: %s'%kwargs['download_delay'], log.DEBUG)
		settings.DOWNLOAD_DELAY = kwargs['download_delay']'''

	if kwargs['auto_throttle']:
		settings.AUTOTHROTTLE_ENABLED = True

	Image.init()
	bot.image_extensions = Image.EXTENSION.keys()
	
	setup_dirs()
	setup_db()

	final_storepath = joinpath(settings.IMAGES_STORE_FINAL, bot._jobname)
	if not exists(final_storepath):
		mkdir(final_storepath)



def setup_dirs():
	def create_dir(path):
		if not exists(path):
			makedirs(path)

	settings.IMAGES_STORE = expanduser(settings.IMAGES_STORE)
	create_dir(settings.IMAGES_STORE)
	settings.IMAGES_STORE_FINAL = expanduser(settings.IMAGES_STORE_FINAL)	
	create_dir(settings.IMAGES_STORE_FINAL)
	settings.HTTPCACHE_DIR = expanduser(settings.HTTPCACHE_DIR)
	create_dir(settings.HTTPCACHE_DIR)

	
def setup_db():
	settings.IMAGES_DB = expanduser(settings.IMAGES_DB)

	db = DBManager(settings.IMAGES_DB)
	db.connect()
	schema_script = None
	with open(joinpath(dirname(realpath(__file__)).rsplit(sep, 1)[0], 'tables.sql'), 'r') as f:
		schema_script = f.read()
	db.executescript(schema_script)
	db.disconnect()

