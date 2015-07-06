import logging as log
import imp


class MonitorException(Exception):
	pass


def start_tk_monitor(outpipe):
	from imagebot.monitor_tk import Monitor	 #Tkinter will have to be imported in its own process for Tk to work
	mon = Monitor(outpipe)
	mon.start()


def start_gtk_monitor(outpipe):
	from imagebot.monitor_gtk import Monitor
	mon = Monitor(outpipe)
	mon.start()


def get_monitor():
	try:
		imp.find_module('gi')
		return start_gtk_monitor
	except ImportError as e:
		log.error(e.message)

	try:
		imp.find_module('Tkinter')
		return start_tk_monitor
	except ImportError as e:
		log.error(e.message)
		
	raise MonitorException()

