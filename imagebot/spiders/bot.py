import scrapy
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.http import Request
from scrapy import log
import re

from imagebot.items import ImageItem
import imagebot.spiders.init as init
from imagebot.common.web.urls import AbsUrl


class ImageSpider(CrawlSpider):
	name = 'imagebot'
	allowed_domains = []
	start_urls = []

	rules = (
		Rule(LinkExtractor(allow=('.*', )), callback='parse_item', follow=True),
	)


	def __init__(self, **kwargs):
		init.process_kwargs(self, kwargs)
		ImageSpider.allowed_domains = self.allowed_domains

		super(ImageSpider, self).__init__(**kwargs)
	
	
	def parse_start_url(self, response):
		return self.parse_item(response)
		

	def parse_item(self, response):
		images = ImageItem()
		image_urls = []
		base_url = AbsUrl(response.url)
		

		anchors = response.xpath('//a')

		for anchor in anchors:
			url = anchor.xpath('@href').extract()
			if len(url) > 0:
				ext = url[0][url[0].rfind('.'):]
				if ext.lower() in self.image_extensions: 
					image_urls.append(url[0])

		imgs = response.xpath('//img')

		for img in imgs:
			url = img.xpath('@src').extract()
			if len(url) > 0:
				image_urls.append(url[0])
		
		#remove duplicates
		image_urls = list(set(image_urls))

		for i in range(len(image_urls)):
			url = image_urls[i]

			if not url.startswith('http') and not url.startswith('//'):
					image_urls[i] = base_url.extend(url)
					log.msg('abs url: %s'%url, log.DEBUG)
			else:
				if url.startswith('//'):
					url = base_url.extend(url)

				if not any([(AbsUrl(url).domain == ad) for ad in self.allowed_image_domains]):
					image_urls[i] = ''
					log.msg('blocked image url: %s'%url, log.DEBUG)
				else:
					image_urls[i] = url

		images['image_urls'] = [url for url in image_urls if url != '']
		images['referer'] = response.url

		requests = self.parse_js_links(response)

		return [images] + requests


	def parse_js_links(self, response):
		requests = []
		base_url = AbsUrl(response.url)

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

					if url == '':
						continue						
					if not url.startswith('http'):
						url = base_url.extend(url)
					requests.append(Request(url, meta={'js_link': True}, headers={'Referer': response.url}))
					log.msg('adding js url: %s'%url, log.DEBUG)

		return requests

	
	def get_jobname(self):
		return self._jobname


	def update_monitor(self, image_path):
		if self._inpipe is not None:
			self._inpipe.send(image_path)	


	jobname = property(get_jobname)
