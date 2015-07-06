#helper module for initializing Imagebot

from os.path import join as joinpath, exists, expanduser, realpath, dirname
from os import mkdir, makedirs, sep
from multiprocessing import Process, Pipe
import logging as log
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from PIL import Image

from mutils.web.urls import AbsUrl
from mutils.web.cdns import cdns

from imagebot.dbmanager import DBManager
from imagebot.settings import settings
from imagebot.monitor import get_monitor, MonitorException


def process_kwargs(bot, kwargs):
	bot._jobname = 'default'
	bot._inpipe = None
	bot._start_url_only = False

	images_store = kwargs.get('images_store')
	if images_store is not None:
		settings.IMAGES_STORE_FINAL = images_store

	start_urls = kwargs.get('start_urls', None)
	if start_urls:
		urls = [u.strip() for u in start_urls.split(',') if len(u.strip()) > 0]
		
		if any([not u.startswith('http') for u in urls]):
			log.error('missing url scheme, (http/https)?')
			return

		kwargs['start_urls'] = urls
		log.debug('start urls: \n' + '\n'.join(urls))

		allowed_domains = list(set([AbsUrl(u).domain for u in urls]))
		bot.allowed_domains = allowed_domains
	else:
		log.error('must provide start url(s)')
		return

	domains = kwargs.get('domains', None)
	if domains:
		domains = [d.strip() for d in domains.split(',')]
		bot.allowed_domains.extend(domains)
	
	log.debug('allowed domains: \n' + ', '.join(bot.allowed_domains))

	bot.allowed_image_domains = bot.allowed_domains
	if not kwargs['no_cdns']:
		bot.allowed_image_domains.extend(cdns)

	log.debug('allowed image domains: \n' + ', '.join(bot.allowed_image_domains))

	bot._jobname = bot.allowed_domains[0]

	jobname = kwargs.get('jobname', None)
	if jobname:
		bot._jobname = jobname

	stay_under = kwargs.get('stay_under', None)
	if stay_under:
		bot.rules = ()
		for start_url in kwargs['start_urls']:
			bot.rules += (Rule(LinkExtractor(allow=(start_url + '.*',)), callback='parse_item', follow=True),)
		log.debug('staying under: %s'%start_urls)

	if kwargs['url_regex']:
		regex_rule = (Rule(LinkExtractor(allow=kwargs['url_regex'],), callback='parse_item', follow=True),)
		if stay_under:
			bot.rules += regex_rule
		else:
			bot.rules = regex_rule

	if kwargs['monitor']:
		try:
			bot._inpipe, outpipe = Pipe()
			mon_start_func = get_monitor()
			monitor_process = Process(target=mon_start_func, args=(outpipe,))
			monitor_process.start()
		except MonitorException:
			log.error('will not start monitor ui')

	if kwargs['user_agent']:
		settings.USER_AGENT = kwargs['user_agent']

	if kwargs['minsize']:
		settings.IMAGES_MIN_WIDTH, settings.IMAGES_MIN_HEIGHT = kwargs['minsize']

	if kwargs['no_cache']:
		settings.HTTPCACHE_ENABLED = False

	if kwargs['depth_limit']:
		depth_limit = abs(int(kwargs['depth_limit']))
		if depth_limit == 0:
			bot._start_url_only = True
		else:
			settings.DEPTH_LIMIT = depth_limit


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

