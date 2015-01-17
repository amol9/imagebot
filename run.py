#! /usr/bin/python

from twisted.internet import reactor
from scrapy.crawler import Crawler
from scrapy import log, signals
from scrapy.utils.project import get_project_settings
from argparse import ArgumentParser

from imagebot.spiders.bot import ImageSpider


def parse_arguments():
	argparser = ArgumentParser()
	argparser.add_argument('-d', '--domains', help='list of comma separated allowed domains')
	argparser.add_argument('-j', '--jobname', help='job name')
	argparser.add_argument('-u', '--stay-under', help='stay under a url')
	argparser.add_argument('-a', '--user-agent', help='user agent string')
	argparser.add_argument('-s', '--min-size', help='minimum image size, WIDTHxHEIGHT')
	argparser.add_argument('-l', '--log-level', choices=['critical', 'error', 'warning', 'info', 'debug'], default='error',
				help='logging level')
	argparser.add_argument('-m', '--monitor', action='store_true', help='monitor crawled images in a window')
	argparser.add_argument('-nc', '--no-cache', action='store_true', help='disable caching')
	argparser.add_argument('start_url', help='start url')

	args = argparser.parse_args()

	if args.min_size:
		args.min_size = tuple(int(i) for i in args.min_size.split('x'))
	return args


def start_spider(args):
	spider = ImageSpider(domains=args.domains, start_url=args.start_url, jobname=args.jobname, stay_under=args.stay_under,
				monitor=args.monitor, user_agent=args.user_agent, minsize=args.min_size, no_cache=args.no_cache)

	settings = get_project_settings()
	crawler = Crawler(settings)
	crawler.signals.connect(reactor.stop, signal=signals.spider_closed)
	crawler.configure()
	crawler.crawl(spider)
	crawler.start()

	log.start(loglevel=dict((v, k) for (k, v) in log.level_names.iteritems())[args.log_level.upper()])

	reactor.run()


if __name__ == '__main__':
	#import pdb; pdb.set_trace()
	args = parse_arguments()
	start_spider(args)
