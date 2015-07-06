from twisted.internet import reactor
from scrapy.crawler import Crawler
from scrapy import signals
from scrapy.utils.project import get_project_settings
from scrapy.settings import Settings
from argparse import ArgumentParser
import logging

from imagebot.spiders.bot import ImageSpider
from imagebot.settings import settings
from imagebot.clear import clear_cache, clear_db, clear_duplicate_images
from imagebot.version import version


def parse_arguments():
	log_level_lookup = dict([(k.lower(), v) for (k, v) in logging._levelNames.items() if type(k) == str])

	argparser = ArgumentParser()

	argparser.add_argument('-v', '--version', action='version', version=version, help='print version')

	subparsers = argparser.add_subparsers(dest='subcommand')

	crawl_parser = subparsers.add_parser('crawl')

	crawl_parser.add_argument('-d', '--domains', help='list of comma separated allowed domains')
	crawl_parser.add_argument('-j', '--jobname', help='job name')
	crawl_parser.add_argument('-u', '--stay-under', action='store_true', help='stay under a url')
	crawl_parser.add_argument('-a', '--user-agent', help='user agent string')
	crawl_parser.add_argument('-s', '--min-size', help='minimum image size, WIDTHxHEIGHT')
	crawl_parser.add_argument('-r', '--url-regex', help='regex filter for urls to be followed')
	crawl_parser.add_argument('-is', '--images-store', help='image store location, default: %s'%settings.IMAGES_STORE_FINAL)
	crawl_parser.add_argument('-dl', '--depth-limit', help='depth limit, default: no limit')
	#crawl_parser.add_argument('-dd', '--download-delay', help='download delay between requests')
	crawl_parser.add_argument('-at', '--auto-throttle', action='store_true', help='enable auto throttle')
	crawl_parser.add_argument('-l', '--log-level', choices=list(log_level_lookup.keys()), default='error',
					help='logging level')
	crawl_parser.add_argument('-m', '--monitor', action='store_true', help='monitor crawled images in a window')
	crawl_parser.add_argument('-nc', '--no-cache', action='store_true', help='disable caching')
	crawl_parser.add_argument('--no-cdns', action='store_true', help='disallow default cdns')
	crawl_parser.add_argument('start_urls', help='start url(s)')

	clear_parser = subparsers.add_parser('clear')
	
	clear_parser.add_argument('--cache', dest='clear_cache', action='store_true', help='clear cache')
	clear_parser.add_argument('--db', dest='clear_db',
					help='clear image metadata from db(url / domain name / job name / ALL to clear entire db)')
	clear_parser.add_argument('--duplicate-images', dest='clear_duplicate_images',
					help='delete duplicate images by job / domain name')

	args = argparser.parse_args()

	#if args.version:
		#return args, 'version'

	if args.subcommand == 'clear':
		return args, 'clear'

	if args.min_size:
		args.min_size = tuple(int(i) for i in args.min_size.split('x'))

	args.log_level = log_level_lookup[args.log_level]

	return args, 'crawl'


def start_spider(args):
	#log.start(loglevel=args.log_level)

	'''spider = ImageSpider(domains=args.domains, start_urls=args.start_urls, jobname=args.jobname, stay_under=args.stay_under,
				monitor=args.monitor, user_agent=args.user_agent, minsize=args.min_size, no_cache=args.no_cache,
				images_store=args.images_store, depth_limit=args.depth_limit, url_regex=args.url_regex,
				no_cdns=args.no_cdns, auto_throttle=args.auto_throttle)'''

	project_settings = Settings()
	project_settings.setmodule(settings)
	crawler = Crawler(ImageSpider, project_settings)
	crawler.signals.connect(reactor.stop, signal=signals.spider_closed)
	#crawler.configure()
	#crawler.crawl(spider)
	crawler.crawl(domains=args.domains, start_urls=args.start_urls, jobname=args.jobname, stay_under=args.stay_under,
			monitor=args.monitor, user_agent=args.user_agent, minsize=args.min_size, no_cache=args.no_cache,
			images_store=args.images_store, depth_limit=args.depth_limit, url_regex=args.url_regex,
			no_cdns=args.no_cdns, auto_throttle=args.auto_throttle)

	#crawler.start()
	reactor.run()


def clear(args):
	if args.clear_cache:
		clear_cache()

	if args.clear_db is not None:
		clear_db(args.clear_db)

	if args.clear_duplicate_images is not None:
		clear_duplicate_images(args.clear_duplicate_images)	


def main():
	args, subcommand = parse_arguments()
	if subcommand == 'version':
		print(version)
	elif subcommand == 'clear':
		clear(args)
	elif subcommand == 'crawl':
		start_spider(args)
	else:
		print('invalid command')


if __name__ == '__main__':
	main()

