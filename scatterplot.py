###############################################################################
#                                                                             #
# This code was originally consisted of the following files:                  #
#     drawingpanel.py  (author: Marty Stepp)                                  #
#     scatterplot.py   (author: William Mitchell)                             #
# They were integrated into a single file by Saumya Debray for programming    #
# simplicity.                                                                 #
#                                                                             #
###############################################################################

import atexit
import sys
import time

# python3.0 uses "tkinter," python2.x uses "Tkinter."
# detect version info and import appropriate graphics
# code added by TA Steve Geluso
if (sys.version_info >= (3,0)):
    from tkinter import *
else:
    from Tkinter import *

'''
A DrawingPanel object represents a simple interface for creating
graphical windows in Python.

Author : Marty Stepp (stepp AT cs.washington)
Version: 2009/10/21
'''
class DrawingPanel(Tk):
    '''
    Constructs a panel of a given width, height, and optional background color.
    
    Keyword arguments:
    width -- width of the DrawingPanel in pixels (default 500)
    height -- height of the DrawingPanel in pixels (default 500)
    background -- background color of the DrawingPanel (default "white")
    '''
    def __init__(self, width=500, height=500, background="white"):
        Tk.__init__(self)
        self.width = width
        self.height = height
        self.title("DrawingPanel")
        self.canvas = Canvas(self, width = width + 1, height = height + 1)
        self.canvas["bg"] = background
        self.canvas.pack({"side": "top"})
        self.wm_resizable(0, 0)
        self.update()
    
        # hack - runs mainloop on exit if not interactive
        if not hasattr(sys, 'ps1'):
            self.install_mainloop_hack()

    def install_mainloop_hack(self):
        # for everything but idle
        atexit.register(self.mainloop)

        # hack just for idle:
        # flush_stdout is called immediately after code execution - intercept
        # this call, and use it to call mainloop
        try:
            import idlelib.run
            def mainloop_wrap(orig_func):
                def newfunc(*a, **kw):
                    self.mainloop()
                    idlelib.run.flush_stdout = orig_func
                    return orig_func(*a, **kw)
                return newfunc
            idlelib.run.flush_stdout = mainloop_wrap(idlelib.run.flush_stdout)
        except ImportError:
            pass

    '''
    Erases all shapes from the panel and fills it with its background color.
    '''
    def clear(self):
        self.canvas.create_rectangle(0, 0, self.width + 2, self.height + 2, \
                outline=self.canvas["bg"], fill=self.canvas["bg"])
    
    '''
    Sets the panel's background color to be the given color.

    Keyword arguments:
    color -- the color to set, as a string such as "yellow" or "black"
    '''
    def set_background(self, color):
        self.canvas["bg"] = color
    
    '''
    Causes the DrawingPanel to pause for the given number of milliseconds.
    Useful for creating simple animations.
    
    Keyword arguments:
    ms -- number of milliseconds to pause
    '''
    def sleep(self, ms):
        try:
            self.update()
            time.sleep(ms / 1000.0)
            self.update()
        except Exception:
            pass



###############################################################################
#                                                                             #
# scatterplot.py                                                              #
# Author: William Mitchell                                                    #
#                                                                             #
###############################################################################

class View:
    """A View represents an area on a DrawingPanel"""
    def __init__(_, panel, x, y, width, height):
        _.panel = panel
        _.x = x
        _.y = y
        _.width = width
        _.height = height

    def line(_, x1, y1, x2, y2, **kw):
        #print("View.line: ", x1, y1, x2, y2, kw)
        _.panel.canvas.create_line(_.x+x1, _.y+y1, _.x+x2, _.y+y2, **kw)

    def text(_, x1, y1, **kw):
        #print("View.text: ", x1, y1, kw)
        _.panel.canvas.create_text(_.x+x1, _.y+y1, **kw)

class ScatterPlot:
    """
    ScatterPlot's constructor plots the values in xy_pairs, assumed to be int two-tuples.
    The plot's X- and Y-axis are scaled based on largest x and y values.

    """
    def __init__(_, view, xy_pairs, fill="black", mark="x"):
        xscale = _.scale(map(lambda t: t[0], xy_pairs), view.width)
        yscale = _.scale(map(lambda t: t[1], xy_pairs), view.height)
        #print("x,y scales:", xscale, yscale)

        view.line(0, 0, view.width, 0)                          # top
        view.line(0, view.height, view.width, view.height)      # bottom
        view.line(0, 0, 0, view.height)                         # left
        view.line(view.width, 0, view.width, view.height)       # right
    
        for (x,y) in xy_pairs:
            view.text(x*xscale,view.height-y*yscale,text=mark,fill=fill)

    def scale(_, values, size):
        """returns factor to multiply values by to produce a coordinate in range [0,size)"""
    
        values = list(values)
        #print(values,size)
    
        return size / (max(values) - min(values))

def translate(L):
    xs = [x for (x,y) in L]
    ys = [y for (x,y) in L]
    min_x = min(xs)
    min_y = min(ys)

    return [(x-min_x, y-min_y) for (x,y) in L]

def draw_scatterplot(data_list,fillcolor, markstring):
        panel = DrawingPanel(1450,920)
        view = View(panel,10,10,1450,920)
        list1 = translate(data_list)
        ScatterPlot(view, list1, fill=fillcolor, mark=markstring)
