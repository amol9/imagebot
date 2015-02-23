========
imagebot
========

A web bot to crawl websites and scrape images.

Features
========

* Supported platforms: Linux / Python 2.7.
* Uses scrapy web crawling framework.
* Maintains a database of all downloaded images to avoid duplicate downloads.
* Optionally, it can scrape only under a particular url, e.g. scraping *\http://website.com/albums/new* with this option will only download from new album.
* Scrapes through javascript popup links.
* Live monitor window for displaying images as they are scraped.

Usage
=====

**crawl commands:**

* Scrape images from *\http://website.com*::

	imagebot crawl http://website.com

* Scrape images from *\http://website.com* while allowing images from a cdn such as amazonaws.com (add multiple domains with comma separated list)::

	imagebot crawl http://website.com -d amazonaws.com

* Specify image store location::

	imagebot crawl http://website.com -is /home/images

* Specify minimum size of image to be downloaded (width x height)::

	imagebot crawl http://website.com -s 300x300

* Stay under *\http://website.com/albums/new*::

	imagebot crawl http://website.com/albums/new -u

* Launch monitor windows for live images::

	imagebot crawl http://website.com -m

* Set user-agent::

	imagebot crawl http://website.com -a "my_imagebot(http://mysite.com)"

* Specify regex for urls (does not apply to start url(s))::

	imagebot crawl http://website.com -r .*gallery.*

* Specify depth limit::

	imagebot crawl http://website.com -dl 2

* A list of well known cdn's is included and enabled by default for image downloads. To disable it::

	imagebot crawl http://website.com --no-cdns

* Enable auto throttle (details: http://doc.scrapy.org/en/latest/topics/autothrottle.html#std:setting-AUTOTHROTTLE_ENABLED)::

	imagebot crawl http://website.com -at

* For more options, get help::

	imagebot crawl -h

**clear commands:**

* Clear cache::
	
	imagebot clear --cache

* Remove image metadata from database::

	imagebot clear --db website.com

* Multiple copies of same image may be downloaded due to different urls. Clean up duplicate images::

	iamgebot clear --duplicate-images website.com

* Get help::

	imagebot clear -h

Dependencies
============

#. python-gi (Python GObject Introspection API) (if using monitor UI)

	On Ubuntu::
	
		apt-get install python-gi

#. scrapy (a powerful web crawling framework)

	It will be automatically installed by pip.

#. Pillow (Python Imaging Library)

	It will be automatically installed by pip.

Download
========

* PyPI: http://pypi.python.org/pypi/imagebot/
* Source: https://github.com/amol9/imagebot/ [Use git clone flag "--recursive" to pull submodule sources as well.]
