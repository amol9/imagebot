import ez_setup
ez_setup.use_setuptools()

from setuptools import setup, find_packages
import platform
import imp

install_requires = ['scrapy']

try:
	imp.find_module('PIL')
except ImportError:
	install_requires.append('Pillow')

entry_points = {}
entry_points['console_scripts'] = ['imagebot=imagebot.main:main']

setup(	name='imagebot',
	version='1.0.2',
	description='A web bot to scrape images from websites.',
	author='Amol Umrale',
	author_email='babaiscool@gmail.com',
	url='http://pypi.python.org/pypi/imagebot/',
	packages=['imagebot', 'imagebot.spiders'],
	package_data={'imagebot': ['tables.sql']},
	scripts=['ez_setup.py'],
	entry_points=entry_points,
	install_requires=install_requires
)

