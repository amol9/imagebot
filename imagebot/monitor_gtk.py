from gi.repository import Gtk, GObject, GLib
from gi.repository.GdkPixbuf import Pixbuf, InterpType
from gi.repository import Gdk
import sys
import os
from time import sleep


GObject.signal_new('change_image', Gtk.Window, GObject.SIGNAL_RUN_FIRST, GObject.TYPE_NONE, (GObject.TYPE_STRING,))


class MyWindow(Gtk.Window):

	def __init__(self, outpipe, title='imagebot'):
		Gtk.Window.__init__(self, title=title)
		Gtk.Window.set_default_size(self, 800, 600)

		self.connect("key_press_event", self.on_key_pressed)
		self.connect("change_image", self.on_change_image)
		self.image = Gtk.Image()
		
		self._outpipe = outpipe
		

	def on_key_pressed(self, event, data):
		(b, k) = data.get_keyval()
		key = Gdk.keyval_name(k)
		

	def on_change_image(self, event, data):
		pass


	def update_image(self):
		image_path = None
		if self._outpipe.poll():
			image_path = self._outpipe.recv()
			self.set_image(image_path)
		
		sleep(0.2)
		return True

	def set_image(self, filename, event=None):
		Gtk.Window.set_title(self, filename)
		self.remove(self.image)

		pb = Pixbuf.new_from_file(filename)

		iw = Pixbuf.get_width(pb)
		ih = Pixbuf.get_height(pb)
		ar = (float)(iw) / ih
		
		(w, h) = Gtk.Window.get_size(self)
		if (iw > ih):
			nw = w
			nh = (int)(nw / ar)
		else:
			nh = h
			nw = (int)(nh * ar)

		pb2 = Pixbuf.scale_simple(pb, nw, nh, InterpType.BILINEAR)

		self.image.set_from_pixbuf(pb2)
		self.add(self.image)

		self.image.show_all()


class Monitor():
	def __init__(self, outpipe):
		self._outpipe = outpipe


	def start(self):
		win = MyWindow(self._outpipe)
		win.connect("delete-event", Gtk.main_quit)

		win.show_all()
		GLib.idle_add(win.update_image)
		Gtk.main()

