import ez_setup
ez_setup.use_setuptools()

from setuptools import setup, find_packages
import platform
import imp
from imagebot.version import version

with open('imagebot/env.py', 'w') as f:
	f.write('env = \'release\'\n')


install_requires = ['scrapy']

try:
	imp.find_module('PIL')
except ImportError:
	install_requires.append('Pillow')

entry_points = {}
entry_points['console_scripts'] = ['imagebot=imagebot.main:main']

setup(	name='imagebot',
	description='A web bot to crawl websites and scrape images.',
	version=version,
	author='Amol Umrale',
	author_email='babaiscool@gmail.com',
	url='http://pypi.python.org/pypi/imagebot/',
	packages=['imagebot', 'imagebot.spiders', 'imagebot.common', 'imagebot.common.web'],
	package_data={'imagebot': ['tables.sql']},
	scripts=['ez_setup.py'],
	entry_points=entry_points,
	install_requires=install_requires,
	classifiers=[
		'Development Status :: 4 - Beta',
		'Environment :: Console',
		'Framework :: Scrapy',
		'Framework :: Twisted',
		'License :: OSI Approved :: MIT License',
		'Natural Language :: English',
		'Operating System :: POSIX :: Linux',
		'Operating System :: Microsoft :: Windows',
		'Programming Language :: Python :: 2.7',
		'Topic :: Internet :: WWW/HTTP :: Indexing/Search'
	]		
)

with open('imagebot/env.py', 'w') as f:
	f.write('env = \'dev\'\n')
