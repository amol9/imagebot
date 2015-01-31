========
imagebot
========

A web bot to scrape images from websites.

Features
========

* Supported platform: Linux / Python 2.x.
* Uses scrapy web crawling framework.
* Maintains a database of all downloaded images to avoid duplicate downloads.
* Optionally, it can scrape only under a particular url, e.g. scraping "http://website.com/albums/new" with this option will only download from new album.
* You can specify minimum image size to be downloaded.
* Live monitor window for displaying images as they are scraped.

Usage
=====

#. Scrape images from http://website.com::

	imagebot http://website.com

#. Scrape images from http://website.com while allowing images from a cdn such as amazonaws.com (add multiple domains with comma separated list)::

	imagebot http://website.com -d amazonaws.com

#. Specify minimum size of image to be downloaded (width x height)::

	imagebot http://website.com -s 300x300

#. Stay under http://website.com/albums/new::

	imagebot http://website.com/albums/new -u http://website.com/albums/new

#. Launch monitor windows for live images::

	imagebot http://website.com -m

#. Set user-agent::

	imagebot http://website.com -a "my_imagebot(http://mysite.com)"

#. For more options, get help::

	wallp -h

Dependencies
============

#. python-gi (Python GObject Introspection API)

	On Ubuntu::
	
		apt-get install python-gi

#. scrapy (a powerful web crawling framework)

	It will be automatically installed by pip.

#. Pillow (Python Imaging Library)

	It will be automatically installed by pip.

Download
========

* PyPI: http://pypi.python.org/pypi/imagebot/
* Source: https://bitbucket.org/amol9/imagebot/

