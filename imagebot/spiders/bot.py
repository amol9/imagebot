import scrapy
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.http import Request
from os.path import join as joinpath, exists
from os import mkdir
from multiprocessing import Process
from scrapy import log
import re

from imagebot.items import ImageItem
import imagebot.settings as settings
from imagebot.monitor import Monitor


class ImageSpider(CrawlSpider):
	name = 'imagebot'
	allowed_domains = []
	start_urls = []

	rules = (
		Rule(LinkExtractor(allow=('.*', )), callback='parse_item', follow=True),
	)


	def __init__(self, **kwargs):
		self._jobname = 'default'

		start_url = kwargs.get('start_url', None)
		if start_url:
			if not start_url.startswith('http'):
				log.msg('missing url scheme, (http/https)?', log.ERROR)
				return

			ImageSpider.start_urls = [start_url]
			ImageSpider.allowed_domains = [start_url.split('/')[2]]
		else:
			log.msg('must provide start url', log.ERROR)
			return

		domains = kwargs.get('domains', None)
		if domains:
			domains = [d.strip() for d in domains.split(',')]
			ImageSpider.allowed_domains.extend(domains)

		self._jobname = ImageSpider.allowed_domains[0]

		jobname = kwargs.get('jobname', None)
		if jobname:
			self._jobname = jobname

		final_storepath = joinpath(settings.IMAGES_STORE_FINAL, self._jobname)
		if not exists(final_storepath):
			mkdir(final_storepath)

		stay_under = kwargs.get('stay_under', None)
		if stay_under:
			ImageSpider.rules = (Rule(LinkExtractor(allow=(stay_under + '.*', )), callback='parse_item', follow=True),)

		if kwargs['monitor']:
			mon = Monitor(self._jobname)
			monitor = Process(target=mon.start)
			monitor.start()

		if kwargs['user_agent']:
			settings.USER_AGENT = kwargs['user_agent']

		if kwargs['minsize']:
			settings.IMAGES_MIN_WIDTH, settings.IMAGES_MIN_HEIGHT = kwargs['minsize']
	
		if kwargs['no_cache']:
			settings.HTTPCACHE_ENABLED = False

		super(ImageSpider, self).__init__(**kwargs)

	
	def parse_start_url(self, response):
		return self.parse_item(response)
		

	def parse_item(self, response):
		item = ImageItem()
		urls = []
		
		if not response.meta.get('js_link'):
			imgs = response.xpath('set:difference(//img, //a/img)')
		else:
			imgs = response.xpath('//img')

		for img in imgs:
			url = img.xpath('@src').extract()
			urls.extend(url)

		for i in range(len(urls)):
			url = urls[i]
			#remove duplicatesres
			if url != '':
				for j in range(i + 1, len(urls)):
					if urls[j] == url:
						urls[j] = ''

			if url != '' and not url.startswith('http'):
					url = self.make_abs_url(response.url, url)
					urls[i] = url
			else:
				if not any([url.find(ad) != -1 for ad in ImageSpider.allowed_domains]):
					urls[i] = ''

		item['image_urls'] = [u for u in urls if u != '']
		item['referer'] = response.url

		requests = self.parse_js_links(response)

		return [item] + requests


	def make_abs_url(self, page_url, rel_url):
		abs_url = None
		rfslash = page_url.rfind('/')
		if rfslash < 8:
			abs_url = page_url + '/' + rel_url
		else:
			abs_url = page_url[0:rfslash+1] + rel_url
		return abs_url


	def parse_js_links(self, response):
		requests = []

		jscall_regex = re.compile("\S+\((.*?)\)", re.M | re.S)
		for a in response.xpath('//a'):
			href = a.xpath('@href').extract()
			if href is not None and len(href) > 0:
				href = href[0]
			else:
				continue
			if href.find('javascript') != -1:
				onclick = a.xpath('@onclick').extract()
				if onclick is not  None and len(onclick) > 0:
					onclick = onclick[0]
				else:
					continue
				matches = jscall_regex.findall(onclick)
				if matches:
					jscall = matches[0]
					jscall_args = jscall.split(',')
					url = jscall_args[0].strip('\'').strip('\"')
					if url != '' and not url.startswith('http'):
						url = self.make_abs_url(response.url, url)
					requests.append(Request(url, meta={'js_link': True}, headers={'Referer': response.url}))
					log.msg('adding js url: %s'%url, log.DEBUG)

		return requests

	
	def get_jobname(self):
		return self._jobname


	jobname = property(get_jobname)
