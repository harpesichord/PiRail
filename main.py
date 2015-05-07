#! /bin/python

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
from screen import Screen, Button, Text

# Icon is a very simple bitmap class, just associates a name and a pygame
# image (PNG loaded from icons directory) for each.
# There isn't a globally-declared fixed list of Icons.  Instead, the list
# is populated at runtime from the contents of the 'icons' directory.

class Icon:

	def __init__(self, name):
	  self.name = name
	  try:
	    self.bitmap = pygame.image.load(iconPath + '/' + name + '.png')
	  except:
	    pass
        
        


def createScreens():
    global screens
    mainScreen = Screen()
    screens["main"] = mainScreen

def createButtons():
    global screens
    
    screens["main"].addButtons({
        "start": Button((5,185,100,50), cb=mainScreenTouch, value = 1, bg='start'),
        "stop": Button((215,185,100,50), cb=mainScreenTouch, value = 2, bg='stop'),
        "settings": Button((110,185,100,50), cb=mainScreenTouch, value = 3, bg='settings')
    })
    
def createText():
    global screens
    
    screens["main"].addTexts({
        "moving": Text("",(5, 5)),
        "sleep": Text("",(5, 48)),
        "frames": Text("",(5, 93)),
        "remaining": Text("",(5, 140))
    })

def updateText(screen):
    global interval, wait, shotNumber, timeRemaining
    
    if screen == "main":
        screens["main"].setText("moving", "Moving: " + str(interval) + "ms")
        screens["main"].setText("sleep", "Sleep: " + str(wait) + "ms")
        screens["main"].setText("frames", "Frames: " + str(shotNumber) + " of " + str(shots))
        screens["main"].setText("remaining", "Remaining: " + str(timedelta(seconds=timeRemaining)))
        
def mainScreenTouch(n):
    print(str(n))
    

pins = {"GROUND"    : 15, #White
        "FOCUS"     : 11, #Yellow
        "SHUTTER"   : 13, #RED
        "motorA"    : 0,
        "motorB"    : 0,
        "leftTrig"  : 0,
        "rightTrig" : 0}
        
shotNumber = 0
timeRemaining = 0
shutterSpeed = 200 # in ms time shutter is open (maybe this number might not actually matter)
shots = 100
interval = 500 # in ms time the rig moves
wait = 1000 # in ms between moving and taking picture
direction = 1
screens = {}
motorRunning = False
allowMotion = 0
iconPath        = 'images'
icons = [] # This list gets populated at startup
currentScreen = "main"

def signal_handler(signal, frame):
    global runs
    runs = 0
    #gpioCleanup()
    #GPIO.cleanup()
    #while (len(globals.globs["screens"]) > 0):
    #    globals.globs["screens"].pop().stops()
        
    sys.exit(0)
    
# def gpioCleanup():
    # gpio.digitalWrite(globals.globs["motor_pins"]["A"],gpio.LOW)
    # gpio.digitalWrite(globals.globs["motor_pins"]["B"],gpio.LOW)
    
    # os.system("echo 'out' > /sys/class/gpio/gpio508/direction")
    # gpio.pinMode(globals.globs["motor_pins"]["A"],0)
    # gpio.pinMode(globals.globs["motor_pins"]["B"],0)
    # gpio.pinMode(globals.globs["trigger_pins"]["LEFT"],0)
    # gpio.pinMode(globals.globs["trigger_pins"]["RIGHT"],0)
    # gpio.pinMode(globals.globs["camera_pins"]["GROUND"],0)
    # gpio.pinMode(globals.globs["camera_pins"]["FOCUS"],0)
    # gpio.pinMode(globals.globs["camera_pins"]["SHUTTER"],0)

# def gpio_init():
    # print("INITINT GPIO")
    # gpio = wiringpi2.GPIO(wiringpi2.GPIO.WPI_MODE_GPIO)  
    #GPIO.setmode(GPIO.BOARD)
    
    
    # # os.system("echo 252 > /sys/class/gpio/export")
    # # os.system("echo 'out' > /sys/class/gpio/gpio252/direction")
    # # os.system("echo '1' > /sys/class/gpio/gpio252/value")
    
    # # gpio.pinMode(globals.globs["motor_pins"]["A"],gpio.OUTPUT)
    # # gpio.pinMode(globals.globs["motor_pins"]["B"],gpio.OUTPUT)
    # # gpio.pinMode(globals.globs["trigger_pins"]["LEFT"],gpio.INPUT)
    # # gpio.pinMode(globals.globs["trigger_pins"]["RIGHT"],gpio.INPUT)
    
    
    # gpio.pinMode(globals.globs["camera_pins"]["GROUND"],gpio.OUTPUT)
    # gpio.pinMode(globals.globs["camera_pins"]["FOCUS"],gpio.OUTPUT)
    # gpio.pinMode(globals.globs["camera_pins"]["SHUTTER"],gpio.OUTPUT)

    
def triggering():
    while (runs):
        pass
        #if left side triggers set var to 1
        #if right side triggers set var to -1
        #if neither trigger set var to 0
        #if anyside triggers stop motion.
        

#os.putenv('SDL_VIDEODRIVER', 'fbcon')
#os.putenv('SDL_FBDEV'      , '/dev/fb1')
#os.putenv('SDL_MOUSEDRV'   , 'TSLIB')
#os.putenv('SDL_MOUSEDEV'   , '/dev/input/touchscreen')

print("Initting...")
pygame.init()
print("Setting Mouse invisible...")
#pygame.mouse.set_visible(False)
print("Setting fullscreen...")
screen = pygame.display.set_mode((320, 240), pygame.SRCALPHA)
runs = 1

print("LOAD Everything")
createScreens()
createButtons()
createText()

print("Loading Icons...")
# Load all icons at startup.
for file in os.listdir(iconPath):
    if fnmatch.fnmatch(file, '*.png'):
        icons.append(Icon(file.split('.')[0]))
# Assign Icons to Buttons, now that they're loaded
print("Assigning Buttons")
for s in screens.values():        # For each screenful of buttons...
    for b in s.buttons.values():            #  For each button on screen...
        for i in icons:      #   For each icon...
            if b.bg == i.name: #    Compare names; match?
                b.iconBg = i     #     Assign Icon to Button
                b.bg     = None  #     Name no longer used; allow garbage collection
            if b.fg == i.name:
                b.iconFg = i
                b.fg     = None

clock = pygame.time.Clock()


print("Showing")

t = threading.Thread(target=triggering)
t.start()
    
signal.signal(signal.SIGINT, signal_handler)
pygame.display.update()

print("mainloop..")
while runs:
    clock.tick(60)
    
    #screen.fill((224,224,224))
    updateText(currentScreen)
    screens[currentScreen].update()
    screens[currentScreen].draw(screen)
    

    pygame.display.flip()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            runs = 0
    #        while (len(globals.globs["screens"]) > 0):
    #            globals.globs["screens"].pop().stops()
    #    elif event.type == pygame.MOUSEBUTTONDOWN:
    #        x, y = event.pos
    #        globals.globs["screens"][-1].clicked(x, y)
    #    elif event.type == pygame.MOUSEBUTTONUP:      
    #        if (globals.globs["motor_running"]):
    #            globals.globs["motor_running"] = False
    #            # Stop Motor
    #            gpio.digitalWrite(globals.globs["motor_pins"]["A"],gpio.LOW)
    #            gpio.digitalWrite(globals.globs["motor_pins"]["B"],gpio.LOW)
                
                
#gpioCleanup    
#GPIO.cleanup()    
print("DONE")
pygame.quit()
