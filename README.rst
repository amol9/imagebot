========
imagebot
========

This bot crawls a given website or url(s) and downloads all the images.

Features
========

* Supported platforms: Linux / Windows / Python 2.7.
* Uses scrapy web crawling framework.
* Maintains a database of all downloaded images to avoid duplicate downloads.
* Optionally, it can scrape only under a particular url, e.g. scraping *\http://website.com/albums/new* with this option will only download from new album.
* Scrapes through javascript popup links.
* Live monitor window for displaying images as they are scraped.

Usage
=====

**crawl command:**

* Scrape images from *\http://website.com*::

	imagebot crawl http://website.com

* Options for crawl command:

	*-d, --domains*

	Scrape images while allowing images to be downloaded from other domain(s) (add multiple domains with comma separated list). The domain in the start url(s) is(are) allowed by default.

	``imagebot crawl http://website.com -d otherwebsite.com,anotherwebsite.com``
					
	*-is, --images-store*
				
	Specify image store location.

	``imagebot crawl http://website.com -is /home/images``
	
	*-s, --min-size*

	Specify minimum size of image to be downloaded (width x height).

	``imagebot crawl http://website.com -s 300x300``

	*-u, --stay-under*

	Stay under the start url. Only those urls that have the start url as prefix will be crawled. Useful, for example, to crawl an album or a subsection on a website.

	``imagebot crawl http://website.com/albums/new -u``

	*-m, --monitor*

	Launch monitor window for displaying images as they are scraped.

	``imagebot crawl http://website.com -m``

	*-a, --user-agent*

	Set user-agent string. Default: imagebot. It is recommended to change it to yidentify your bot as a matter of responsible crawling.

	``imagebot crawl http://website.com -a "my_imagebot(http://mysite.com)"``

	*-r, --url-regex*

	Specify regex for urls. Only those urls matching the regex will be crawled. It does not apply to start url(s).

	``imagebot crawl http://website.com -r .*gallery.*``

	*-dl, --depth-limit*

	Specify depth limit for crawling. 

	``imagebot crawl http://website.com -dl 2``

	*--no-cdns*

	A list of well known cdn's is included and enabled by default for image downloads. Use this option to disable it.

	*-at, --auto-throttle*

	Enable auto throttle feature of scrapy. (`details in scrapy docs <http://doc.scrapy.org/en/latest/topics/autothrottle.html#std:setting-AUTOTHROTTLE_ENABLED>`_).

	*-j, --jobname*

	Specify a job name. This will be used to store image meta data in the database. By default, domain name of the start url is used as the job name.

	*-nc, --no-cache*

	Disable http caching.

	*-l, --log-level*

	Specify log level.
	Supported levels: info, silent, critical, error, debug, warning. Default: error.

	``imagebot crawl http://website.com -l debug``

	*-h, --help*

	Get help on crawl command options.

**clear command:**

* This command is useful for various kinds of cleanup.

* Options for clear command:	

	*--cache*

	Clear http cache.
	
	*--db*

	Remove image metadata for a job from the database.

	``imagebot clear --db website.com``

	*--duplicate-images*

	Multiple copies of same image may be downloaded due to different urls. Use this option to delete duplucate images for a job.

	``imagebot clear --duplicate-images website.com``

	*-h, --help*

	Get help on clear command options.

Dependencies
============

#. pywin32 (http://sourceforge.net/projects/pywin32/)

	Needed on Windows.

#. python-gi (Python GObject Introspection API)

	Needed on Linux if using monitor UI.
	On Ubuntu: ``apt-get install python-gi``

#. scrapy (web crawling framework)

	It will be automatically installed by pip.

#. Pillow (Python Imaging Library)

	It will be automatically installed by pip.

Download
========

* PyPI: http://pypi.python.org/pypi/imagebot/
* Source: https://github.com/amol9/imagebot/ [Use git clone flag "--recursive" to pull submodule sources as well.]
