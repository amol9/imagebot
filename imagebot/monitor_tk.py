from Tkinter import Tk, Label, Frame
from PIL import Image, ImageTk


class AppWindow(Frame):
	def __init__(self, master, outpipe, title="imagebot"):
		Frame.__init__(self, master)
		self.pack()
		self._outpipe = outpipe
		self._image = None
		self.master.wm_title(title)
		self.master.after(200, self.updateImage)

	
	def updateImage(self):
		image_path = None
		if self._outpipe.poll():
			image_path = self._outpipe.recv()
			image = Image.open(image_path)
			
			iw, ih = image.size
			ar = (float)(iw) / ih
		
			w = self.master.winfo_width()
			h = self.master.winfo_height()
			if (iw > ih):
				nw = w
				nh = (int)(nw / ar)
			else:
				nh = h
				nw = (int)(nh * ar)

			rimage = image.resize((nw, nh))
			self._pimage = ImageTk.PhotoImage(rimage)

			if self._image is not None:
				self._image.destroy()
			self._image = Label(self, image=self._pimage)
			self._image.pack(side='bottom', fill='both', expand='yes')

		self.master.after(200, self.updateImage)


class Monitor():
	def __init__(self, outpipe):
		self._outpipe = outpipe

	
	def start(self):
		root = Tk()
		root.geometry('800x600')
		appwindow = AppWindow(root, self._outpipe)
		appwindow.mainloop()
