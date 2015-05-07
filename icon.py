import wiringpi2
import atexit
import cPickle as pickle
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

class Icon:

    def __init__(self, name):
        self.name = name
        try:
            self.bitmap = pygame.image.load(iconPath + '/' + name + '.png')
        except:
            pass
            

            