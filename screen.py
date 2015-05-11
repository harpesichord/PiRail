#import wiringpi2
#import atexit
#import cPickle as pickle
import errno
import fnmatch
import io
import os
import pygame
import threading
import signal
import sys

from pygame.locals import *
from subprocess import call  
from time import sleep
from datetime import datetime, timedelta

pygame.font.init()
myfont = None

# Screen is a screen for the game that will display buttons and text.  Each has:
#  - optional font type to use
#  - optional font size to use
#  - optional background image or color tuple
class Screen:
    
    buttons = {}
    texts = {}
    shapes = {}
    
    def __init__(self, **kwargs):
        global myfont
        fontType = "monospace"
        fontSize = 25
        self.background = (255,255,255)
        
        for key, value in kwargs.items():
            if   key == 'fonttype'   : fontType    = value
            elif key == 'fontsize'   : fontSize    = value
            elif key == 'background' : self.background = value
            
        myfont = pygame.font.SysFont(fontType, fontSize)
    
    def addButtons(self, buttons):
        self.buttons = buttons
            
    def addTexts(self, texts):
        self.texts = texts
        
    def addShapes(self, shapes):
        self.shapes = shapes
            
    def addButton(self, key, button):
        self.buttons[key] = button
        
    def addText(self, key, text):
        self.texts[key] = text
    
    def addShape(self, key, shape):
        self.shapes[key] = shape
        
    def setBackground(self, background):
        self.background = background
        
    def setText(self, text, value):
        self.texts[text].setText(value)
        
    def draw(self, screen):
        if isinstance(self.background, tuple): # Letterbox, clear background
            screen.fill(self.background)
        else:
            screen.blit(self.background,
                ((320 - self.background.get_width() ) / 2,
                (240 - self.background.get_height()) / 2))
        
        for i,b in enumerate(self.buttons.values()):
            b.draw(screen)
        for i,t in enumerate(self.texts.values()):
            t.draw(screen)
        for i,s in enumerate(self.shapes.values()):
            s.draw(screen)
        
    def update(self):
        for i,t in enumerate(self.texts.values()):
            t.update()
    
    
    
    
    
class Shapes:
    def __init__(self, rect, **kwargs):
        self.rect = rect # Bounds
        self.color    = (0,0,0) # Background fill color, if any
        self.width = 0
        for key, value in kwargs.items():
            if   key == 'color': self.color    = value
            elif key == 'width': self.width    = value

    def setPosition(self, rect):
        self.rect = rect
        
    def setColor(self, color):
        self.color = color
        
    def setWidth(self, width):
        self.width = width
        
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect, self.width)
    
    
    
# Text is text that is written to the screen.  Each has:
#  - text to display rect ((X,Y,W,H) in pixels)
#  - location to display the text ((X,Y) in pixels)
#  - optional color for the text
class Text:

    def __init__(self, text, location, **kwargs):
        global myfont
        self.location = location # Bounds
        self.color    = (0,0,0) # Background fill color, if any
        self.text     = text
        self.surface  = None
        for key, value in kwargs.items():
            if   key == 'color': self.color    = value
            
        self.surface = myfont.render(text, 1, self.color)
    
    def setText(self, text):
        self.text = text
        
    def setLocation(self, location):
        self.location = location
        
    def update(self):
        global myfont 
        self.surface = myfont.render(self.text, 1, self.color)
        
    def draw(self, screen):
        screen.blit(self.surface, self.location)
    
    
    
# Button is a simple tappable screen region.  Each has:
#  - bounding rect ((X,Y,W,H) in pixels)
#  - optional background color and/or Icon (or None), always centered
#  - optional foreground Icon, always centered
#  - optional single callback function
#  - optional single value passed to callback
# Occasionally Buttons are used as a convenience for positioning Icons
# but the taps are ignored.  Stacking order is important; when Buttons
# overlap, lowest/first Button in list takes precedence when processing
# input, and highest/last Button is drawn atop prior Button(s).  This is
# used, for example, to center an Icon by creating a passive Button the
# width of the full screen, but with other buttons left or right that
# may take input precedence (e.g. the Effect labels & buttons).
# After Icons are loaded at runtime, a pass is made through the global
# buttons[] list to assign the Icon objects (from names) to each Button.   
class Button:

    def __init__(self, rect, **kwargs):
        self.rect     = rect # Bounds
        self.color    = None # Background fill color, if any
        self.iconBg   = None # Background Icon (atop color fill)
        self.iconFg   = None # Foreground Icon (atop background)
        self.bg       = None # Background Icon name
        self.fg       = None # Foreground Icon name
        self.callback = None # Callback function
        self.value    = None # Value passed to callback
        for key, value in kwargs.items():
            if   key == 'color': self.color    = value
            elif key == 'bg'   : self.bg       = value
            elif key == 'fg'   : self.fg       = value
            elif key == 'cb'   : self.callback = value
            elif key == 'value': self.value    = value

    def selected(self, pos):
        x1 = self.rect[0]
        y1 = self.rect[1]
        x2 = x1 + self.rect[2] - 1
        y2 = y1 + self.rect[3] - 1
        if ((pos[0] >= x1) and (pos[0] <= x2) and
          (pos[1] >= y1) and (pos[1] <= y2)):
            if self.callback:
                if self.value is None: self.callback()
                else:                  self.callback(self.value)
                return True
            return False

    def draw(self, screen):
        if self.color:
            screen.fill(self.color, self.rect)
        if self.iconBg:
            screen.blit(self.iconBg.bitmap,
              (self.rect[0]+(self.rect[2]-self.iconBg.bitmap.get_width())/2,
              self.rect[1]+(self.rect[3]-self.iconBg.bitmap.get_height())/2))
        if self.iconFg:
            screen.blit(self.iconFg.bitmap,
                (self.rect[0]+(self.rect[2]-self.iconFg.bitmap.get_width())/2,
                self.rect[1]+(self.rect[3]-self.iconFg.bitmap.get_height())/2))

    def setBg(self, name):
        if name is None:
            self.iconBg = None
        else:
            for i in icons:
                if name == i.name:
                    self.iconBg = i
                break