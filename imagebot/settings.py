from imagebot.env import env

settings = None

if env == 'release':
	import imagebot.settings_release as settings_release
	settings = settings_release
elif env == 'dev':
	import imagebot.settings_dev as settings_dev
	settings = settings_dev
else:
	print('unsupported env value')

