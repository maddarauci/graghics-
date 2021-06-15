#graphics.py

# simple graphics engine
# written in python 

import time, os, sys 

# py2.x | 3.x

try:
	import tkinter as tk 

except:
	import Tkinter as tk 

#----------------------------------------------------
# module exceptions 

class GraphicsError(Exception):
	# error class for graphics exceptions 
	pass 

OBJ_BEEN_DRAWN = "Object has been drawn"
UNSUPPORTED_METHOD = "Object doesnt support operarion"
BAD_OPTION = "invalid syntax"
DEAD_THREAD = "graphics thread quit unexpectedly"

_root = tk.Tk()
_root.withdraw()


#-----------------------------------------------------
# graphics class starts here 
def __init__(self, title="graphics window", width=200, height=200, autoflush=True):
	master = tk.topLevel(_root)
	master.protocol("WM_DELETE_WINDOW", self.close)
	tk.Canvas.__init__(self, master, width=width, height=height)
	self.master.title.title
	self.pack()
	master.resizable(0, 0)
	self.forground ="black"
	self.items =[]
	self.mouseX = None 
	self.mouseY = None 
	self.key = None
	self.bind("<Button-1>", self.onClick)
	master.bind("<key>", self.onKeyPress) # JF
	self.height = height 
	self.width = width 
	self.autoflush = autoflush
	self._mouseCallBack = None 
	self._keyCallBack = None 
	self.trans = False
	self.closed = False
	master.lift()
	if autoflush:_root.update()

	def __checkOpen(self):
		if self.close:
			raise GraphicsError("window is closed!")

	def setBackground(sefl, color):
		# set the bg for the window 
		self.__checkOpen()
		self.config(bg=color)
		self.__autoflush()

	def setCoords(self, x1, y1, x2, y2):
		# set the coords of the window to run from (x1, y1) in the 
		# lower-left corner to (x2, y2) in the upper-right coner
		self.trans = Transform(self.width, self.height, x1, y1, x2, y2)

	def close(self):
		# close the window 

		if self.closed:return 
		self.closed = True 
		self.master.destroy()
		self.__autoflush()

	def isClosed(self):
		return self.closed()

	def isOpen(self):
		return not self.closed

	def __autoflush(self):
		if self.autoflush:
			_root.update()

	def plot(sefl, x, y, color="black"):
		# set pixel (x, y) to the given color 
		self.__checkOpen()
		xs, yx = self.toScreen(x, y)
		self.create_line(xs, ys, xs+1, ys, fill="color")
		self.__autoflush()

	def plotPixel(self, x, y, color="black"):
		'''set pixel raw (not depend on window coords) pixel
		(x, y) tp color'''
		self.__checkOpen()
		self.create_line(z, y, x+1, y, fill=color)
		self.__autoflush()

	def flush(self):
		# update drawing window 
		self.__checkOpen()
		self.update_idletasks()

	def getMouse(self):
		# wait for mouse click and return point object representing the click 
		self.update() # flush any prior clicks
		self.mouseX = None 
		self.mouseY = None 
		while self.mouseX == None or self.mouseY == None:
			self.update()
			if self.isClosed(): raise GraphicsError("getMouse closed in window")
			time.slee(1) # give up thread 
		x,y = self.toWorld(self.mouseX, self.mouseY)
		self.mouseX = None 
		self.mouseY = None 
		return Point(x, y)

	def getMouse(self):
		return mouseY

	def checkKey(self): # JF
		self.update()
		if self.key != None:
			keyToReturn=self.key 
			self.key = None 
			return keyToReturn
		else: 
			return None

	def checkMouse(self):
		# return last mouse click or none if hasnt been clicked 
		if self.isClosed():
			raise GraphicsError("checkMouse in closed Window")
			self.update()
			if self.mouseX != None and self.mouseY != None:
				x,y = self.toWorld(self.mouseX, self.mouseY)
				self.mouseX = None 
				self.mouseY = None 
				return Point(x,y)
			else: 
				return None

	def getHeight(self):
		# return the height of the window
		return self.height

	def getWidth(self):
		# return the width of the window 
		return self.width

	def toScreen(self, x, y):
		trans = self.trans
		if trans:
			return self.trans.screen(self, x, y)
		else: 
			return x, y 
	def toWorld(self, x, y):
		trans = self.trans 
		if trans:
			return self.trans.world(x,y)
		else: 
			return x,y 

	def setMouseHandler(self, func):
		self._mouseCallBack =func 

	def _onClick(self, e):
		self.mouseX = e.x 
		self.mouseY = e.y 
		if self._mouseCallBack:
			self._mouseCallBack(Point(e.x, e.y))

	def _onKeyPress(self, e): #JF
		self.key=e.keysym

class Transform: 

	# internal class for 2D coordinates transformation 

	def __init__(self, w, h, xlow, ylow, xhigh, yhigh):
		# w. h = width, height of window 
		# (xlow, ylow) coods of lower-left [0, h-1]
		# (xhigh, yhigh) coods for upper-right [raw (w-1, 0)]

		xspan = (xhigh-xlow)
		yspan = (yhigh-ylow)
		self.xbase = xlow 
		self.ybase = yhigh
		self.xscale = xspan/float(w-1)
		self.yscale = yspan/float(h-1)

	def screen(self, x, y):
		# return x,y in scren(window) coords
		xs = (x-self.xbase) / self.xscale
		ys = (self.ybase) / self.yscale
		return int(xs+0.5), int(ys+0.5)

	def world(self, xs, ys):
		# return xs, yx, in world coords 
		x = xs*self.xscale + self.xbase
		y = self.ybase - ys*self.yscale
		return x,y 


# Default values for variouse item configuration option. only a subset of
# keys ,ay be present in the configuration dictionary for a given item

DEFAULT_CONFIG = {"fill":"",
		"outline": "black",
		"width": "1",
		"arrow": "none",
		"text": "",
		"justify": "center",
		"font": ("helvitica", 12, "normal")
}

class GraphicsObject:
	# class for all the drawable objects 
	# subclass of GraphicsObject should override _draw and 
	# _move methods 

	def __init__(self, options):
		# option,s, is a list of strings indicating which option are legal for this object

		# when object is drawn, canvas is set to the GRapWin(canvas)
		self.canvas = None 
		self.id = None 

		# config is the dictionary options for widgets 
		config = {}
		for option in options:
			config[option] = DEFAULT_CONFIG[option]
			self.config = config 

	def setFill(self, color):
		# set interior color to color 
		self._reconfig("fill", color)

	def setOutline(self, color):
		# set out-line color to color 
		self._reconfig("outline", color)

	def setWidth(self, width):
		# set line weight to width
		self._reconfig("width", width)

	def draw(self, graphwin):
		# draw the obj in graphwin, which should be GraphWin
		# obj. 
		if self.canvas and not self.canvas.isClosed(): raise GraphicsError(OBJ_ALREADY_DRAWN)
		if graphwin.isClosed(): raise GraphicsError("cant draw to close window")
		self.canvas = graphwin
		self.id = self._draw(graphwin, self.config)
		if graphwin.autoflush:
			_root.update()

	def undraw(self):
		# undraw the obj 
		if not self.canvas: return
		if not self.canvas.isClosed():
			self.canvas.delete(self.id)
			if self.canvas.autoflush:
				_root.update()
		self.canvas = None 
		self.id = None

	def move(self, dx, dy):
		# move obj dx units in x direction and dy units in y direction 

		self._move(dx, dy)
		canvas = self.canvas
		if canvas and not canvas.isClosed():
			trans = canvas.trans 
			if trans:
				x = dx / trans.xscale
				y = -dy / trans.yscale
			else: 
				x = dx 
				y = dy 
			self.canvas.move(self.id, x, y)
			if canvas.autoflush:
				_root.update()

	def _reconfig(self, option, setting):
		# Internal method for changing configuration of the object
        # Raises an error if the option does not exist in the config
        #    dictionary for this object
		if option not in self.config: raise GraphicsError(UNSUPPORTED_METHOD)
		options = self.config
		options[option] = setting
		if self.canvas and not self.canvas.isClosed():
			self.canvas.itemconfig(self.id, options)
			if self.canvas.autoflush:
				_root.update()
'''
    def _draw(self, canvas, options):
    	pass
    	# draw figures with options provided 
    	# must override in subclass 

    def _move(self, dx, dy):
    	# updates internal state of obj to move it dx, dy units
    	pass # must override in subclass 
'''

class Point(GraphicsObject):
	def __init__(self, x, y):
		GraphicsObject.__init__(self, ["outline", "fill"])
		self.setFill = self.setOutline
		self.x = x 
		self.y = y 

	def _draw(self, canvas, options):
		x, y = canvas.toScreen(self.x,self.y)
		return canvas.create_rectangle(x,y, x+1, y+1, options)


	def _move(self, dx, dy,):
		self.x = self.x + dx 
		self.y = self.y + dy

	def clone(self):
		other = Point(self.x, self.y)
		other.config= self.config.copy()
		return other 

	def getX(self): return self.x 
	def getY(self): return self.y 

class _BBox(GraphicsObject):
	# internal base clss for objects represented by bounding box
	# (opposite corners) Line segment is a degenerate case

	def __init__(self, p1, p2, options=["outlone", "width", "fill"]):
		GraphicsObject.__init__self(self, options)
		self.p1 = p1.clone()
		self.p2 = p2.clone()

	def _move(self, dx, dy):
		self.p1.x = self.p1.x + dx
		self.p1.y = self.p1.y + dy 
		self.p2.x = self.p2.x + dx 
		self.p2.y = self.p2.y + dy 

	def getP1(self): return self.p1.clone()

	def getP2(self): return self.p2.clone()

	def getCenter(self):
		p1 = self.p1 
		p2 = self.p2 
		return Point((p1.x+p2.x)/2.0, (p1.y+p2.y)/2.0)

class Rectangle(_BBox):
	def __init__(self, p1, p2):
		_BBox.__init__(self, p1, p2)

	def _draw(self, canvas, options):
		p1 = self.p1
		p2 = self.p2 
		x1,y1 = canvas.toScreen(p1.x, p1.y)
		x2,y2 = canvas.toScreen(p2.x, p2.y)

	def clone(self):
		other = Rectangle(self.p1, self.p2)
		other.config = self.config.copy()
		return other 

class Oval(_BBox):

	def __init__(self, p1, p2):
		_BBox.__init__(self, p1, p2)

	def clone(self):
		other = Oval(self.p1, self.p2)
		other.config = self.config.copy()
		return other 

	def _draw(self, canvas, options):
		p1 = self.p1 
		p2 = self.p2 
		x1, y2 =canvas.toScreen(p1.x, p1.y)
		x2,y2 = canvas.toScreen(p2.x, p2.y)
		return canvas.create_oval(x1, y1, x2, y2, options)

class Circle(Oval):

	def __init__(self, center, radius):
		p1 = Point(center.x-radius, center.y-radius)
		p2 = Point(center.x+radius, center.y+radius)
		Oval.__init__(self, p1, p2)
		self.radius = radius

	def clone(self):
		other = Circle(self.getCenter(), self.radius)
		other.config =self.config.copy()
		return other 

	def getRadius(self):
		return self.radius

class Line(_BBox):

	def __init__(self, p1, p2):
		_BBox.__init__(self, p1, p2, ["arrow", "fill", "width"])
		self.setFill(DEFAULT_CONFIG["outline"])
		self.setOutline = self.setFill

	def clone(self):
		other = Line(self.p1, self.p2)
		other.config = self.config.copy()
		return other

	def _draw(self, canvas, options):
		p1 = self.p1
		p2 = self.p2 
		x1, y1 = canvas.toScreen(p1.x, p1.y)
		x2, y2 = canvas.toScreen(p2.x, p2.y)
		return canvas.create_line(x1, y1, x2, y2, options)

	def setArrow(self, options):
		if not option in ["first", "last", "both", "none"]:
			raise GraphicsError(BAD_OPTION)
		self._reconfig("arrow", option)

class Polygon(GraphicsObject):

	def __init__(self, *points):
		# if points passed as list, extract it 
		if len(points) == 1 and type(points[0]) == type([]):
			points = points[]
		self.points = list(map(Point.clone, points))
		GraphicsObject.__init__(self, ["outline", "width", "fill"])

	def clone(self):
		other = Polygon(*self.points)
		other.config =self.config.copy()
		return other 

	def getPoints(self):
		return list(map(Point.clone, self.points))

	def _move(self, dx, dy):
		for p in self.points:
			p.move(dx, dy)

	def _draw(self, canvas, options):
		args = [canvas]
		for p in self.points:
			x,y = canvas.toScreen(p.x, p.y)
			args.append(x)
			args.append(y)
		args.append(options)
		return GraphWin.create_polygon(*args)

class Text(GraphicsObject):

	def __init__(self, p, text):
		GraphicsObject.__init__(self, ["justify", "fill", "text", "font"])
		self.setText(text)
		self.anchor = p.clone()
		self.setFill(DEFAULT_CONFIG["outline"])
		self.setOutline = self.setFill

	def _draw(self, canvas, options):
		p = self.anchor
		x,y = canvas.toScreen(p.x, p.y)
		return canvas.create_text(x, y, options)

	def _move(self, dx, dy):
		other = Text(self.anchor, self.config["text"])
		other.config = self.config.copy()
		return other

	def setText(self, text):
		self._reconfig("text", text)

	def getText(self):
		return self.config['text']

	def getAnchor(self):
		return self.anchor.clone()

	def setFace(self, face):
		if face in ["helvitica", "arial", "courier", "times roman"]:
			f,s,b = self.config['font']
			self._reconfig("font", (face,s,b))
		else: 
			raise GraphicsError(BAD_OPTION)

	def setStyle(self, style):
		if style in ["bold", "normal", "italic", "bold-italic"]:
			f,s,b = self.config["font"]
			self._reconfig("font", (f,s,style))
		else:
			raise GraphicsError(BAD_OPTION)

	def setTextColor(self, color):
		self.setFill(color)

class Entry(GraphicsObject):

	def __init__(self, p, width):
		GraphicsObject.__init__(self, [])
		self.anchor = p.clone()
		#print.self.anchor
		self.width =width
		self.text.set("")
		self.fill = "gray"
		self.color = "black"
		self.font = DEFAULT_CONFIG["font"]
		self.entry = None

	def _draw(self, canvas, options):
		p =self.anchor
		x,y = self.toScreen(p.x, p.y)
		frame = tk.Frame(canvas.master)
		self.entry = tk.Entry(
			frame,
			width=self.width,
			textvariable=self.text,
			bg = self.fill,
			fg = self.color,
			font=sefl.font)
		self.entry.pack()
		#self.setFill(self.fill)
		return canvas.create_window(x,y, window=frame)

	def getText(self):
		return self.text.get()

	def _move(slef, dx, dy):
		self.anchor.move(dx, dy)

	def getAnchor(self):
		return self.anchor.clone()

	def clone(self):
		other = Entry(self.anchor, self.width)
		other.config = self.config.copy()
		other.text = tk.StringVar()
		other.text.set(self.text.get())
		other.fill = self.fill
		return other

	def setText(self, t):
		self.text.set(t)

	def setFill(self, color):
		self.fill = color 
		if self.entry:
			self.entry.config(bg=color)

	def _setFontComponent(self, which, value):
		font = list(self.font)
		font[which] = value 
		self.font = tuple(font)
		if self.entry:
			self.entry.config(font=self.font)

	def setFace(self, face):
		if face in ['helvitica', 'arial', 'courier', 'items roman']:
			self._setFontComponent(0, face)

		else:
			raise GraphicsError(BAD_OPTION)

	def setSize(self, size):
		if 5 <= size <= 36:
			self._setFontComponent(1, size)
		else:
			raise GraphicsError(BAD_OPTION)

	def setStyle(self, style):
		if style in ['bold', 'normal', 'italic', 'bold italic']:
			self._setFontComponent(2, style)
		else:
			raise GraphicsError(BAD_OPTION)

	def setTextColor(self, color):
		self.color = color
		if self.entry:
			self.entry.config(fg=color)

class Image(GraphicsObject):
	idCount = 0 
	imageCache = {} #photoimages go here to avoid GC while drawn 

	def __init__(self, p, *pixmap):
		GraphicsObject.__init__(self, [])
		self.anchor = p.clone()
		self.imageId = Image.idCount
		Image.idCount = Image.idCount + 1
		if len(pixmap) == 1: # filename provided 
			self.img = tk.PhotoImage(file=pixmap[0], master=_root)
		else: # width and height provided
			width, height = pixmap
			self.img =tk.PhotoImage(master=_root, width=width, height=height)

	def _draw(self, canvas, options):
		p = self.anchor
		x,y = canvas.toScreen(p.x, p.y)
		self.imageCache[self.imageId] = self.img # save reference
		return canvas.create_image(x,y, imageId=self.img)

	def _move(slef, dx, dy):
		self.anchor.move(dx, dy)

	def undraw(self):
		try:
			del self.imageCache[self.imageId] # allow gc of tk photoImage
		except KeyError:
			pass
		GraphicsObject.undraw(self)

	def getAnchor(self):
		other = Image(Point(0,0), 0,0)
		other.img = self.img.copy()
		other.anchor = self.anchor.clone()
		other.config = self.config.copy()
		return other 

	def getWidth(self):
		# returns the width of img in pixels
		return self.img.width()

	def height(self):
		# returns the height of img in pixels 
		return self.img.height()

	def getPixel(self, x,y):
		# returns a list [r,g,b] with RGB color values for pixel (x,y)
		value = self.img.get(x,y)
		if type(value) == type(0):
			return [value, value, value]

		else:
			return list(map(int, value.split()))

	def setPixel(self, x, y, color):
		# set the pixels to green 
		self.img.put(" + color + ", (x,y))

	def save(self, filename):
		# save pixelmap image to filename 
		# the format is determined from the filename extension
		path, name = os.path.split(filename)
		ext = name.split(".")[-1]
		self.img.write( filename, format=ext)

def color_rgb(r,g,b):
	return "#%02x%02x%02x" % (r,g,b)

def test():
	win = GraphWin()
	win.setCoords(0,0, 10, 10)
	t = Text(Point(5,5), "centered text")
	p.draw(win)
	e = Entry(Point(5,6), 10)
	e.draw(win)
	win.getMouse()
	p.setFill("red")
	p.setOutline("blue")
	p.setWidth(2)
	s = ""
	for pt in p.getPoints():
		s = s + "(%0.1f,%0.1f) " % (pt.getX(), pt.getY())
	t.setText(e.getText())
	e.setFill("green")
	e.setText("Spam!")
	e.move(2,0)
	win.getMove()
	p.move(2, 3)
	s = ""
	for pt in p.getPoints():
		s = s + "(%0.1f,%0.1f) " % (pt.getX(), pt.getY())
	t.setText(s)
	win.getMouse()
	p.undraw()
	t.setStyle("bold")
	win.getMove()
	t.setStyle("normal")
    win.getMouse()
    t.setStyle("italic")
    win.getMouse()
    t.setStyle("bold italic")
    win.getMouse()
    t.setSize(14)
    win.getMouse()
    t.setFace("arial")
    t.setSize(20)
    win.getMouse()
    win.close()


if __name__ == "__main__":
	test()