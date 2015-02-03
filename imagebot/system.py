import platform
from os.path import expanduser, join as joinpath, exists
import sys


def is_linux():
	return platform.system() == 'Linux'


def is_windows():
	return platform.system() == 'Windows'


def is_py3():
	version = platform.python_version()
	return version[0] == '3'


def get_pictures_dir():
	path = joinpath(expanduser('~'), 'Pictures')
	if not exists(path):
		mkdir(path)
	return path


def prints(msg):
	if is_py3():
		if sys.stdout is not None:
			sys.stdout.write(msg + ' ')
			sys.stdout.flush()
	else:
		if sys.stdout is not None:
			print(msg),
			sys.stdout.flush()
	
