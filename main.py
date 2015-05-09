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
#import callbacks

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
       
       
#pictures handles the code to take the picture.
class Pictures(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        
        
    def run(self):
        global takingPics, GRID_LOCK, shotNumber, values
        
        while True:
            GRID_LOCK.acquire()
            if (not takingPics):
                GRID_LOCK.release()
                return
                
                
            # Start Moving
            controlMotor(True)
            sleep(float(values["pulse"]) / 1000)
            # Stop Moving
            controlMotor(False)
           
            #settling Time
            sleep(float(values["settling"]) / 1000)
            
            #Turn off backlight
            #os.system("echo '0' > /sys/class/gpio/gpio252/value")
            
            # Take Picture
            takePic()
            
            #Turn on backlight
            #os.system("echo '1' > /sys/class/gpio/gpio252/value")
            
            # Interval
            if (values["interval"] > values["shutterSpeed"]):
                sleep(float(values["interval"] - values["shutterSpeed"]) / 1000)
            
            shotNumber += 1
            
            if (shotNumber >= values["shots"]):
                takingPics = False
            
            GRID_LOCK.release()       


def createScreens():
    global screens
    screens["main"] = Screen()
    screens["settings1"] = Screen()
    screens["settings2"] = Screen()
    screens["numberEdit"] = Screen()
    
def createButtons():
    global screens
    
    screens["main"].addButtons({
        "start": Button((5,185,100,50), cb=startTouch, value = 1, bg='start'),
        "stop": Button((215,185,100,50), cb=startTouch, value = 0, bg='stop'),
        "settings": Button((110,185,100,50), cb=changePageTouch, value = 1, bg='settings')
    })
    
    screens["settings1"].addButtons({
        "edit1": Button((265,5,50,50), cb=numberEdit, value = 1, bg='edit'),
        "edit2": Button((265,60,50,50), cb=numberEdit, value = 2, bg='edit'),
        "edit3": Button((265,115,50,50), cb=numberEdit, value = 3, bg='edit'),
        "goback": Button((5,185,100,50), cb=changePageTouch, value = 0, bg='go_back'),
        "next": Button((265,185,50,50), cb=changePageTouch, value = 2, bg='right')
    })
    
    screens["numberEdit"].addButtons({
        "0": Button((197,115,50,50), cb=numberEnter, value = 0, bg='0'),
        "1": Button((32,60,50,50), cb=numberEnter, value = 1, bg='1'),
        "2": Button((87,60,50,50), cb=numberEnter, value = 2, bg='2'),
        "3": Button((142,60,50,50), cb=numberEnter, value = 3, bg='3'),
        "4": Button((32,115,50,50), cb=numberEnter, value = 4, bg='4'),
        "5": Button((87,115,50,50), cb=numberEnter, value = 5, bg='5'),
        "6": Button((142,115,50,50), cb=numberEnter, value = 6, bg='6'),
        "7": Button((32,170,50,50), cb=numberEnter, value = 7, bg='7'),
        "8": Button((87,170,50,50), cb=numberEnter, value = 8, bg='8'),
        "9": Button((142,170,50,50), cb=numberEnter, value = 9, bg='9'),
        "backspace": Button((247,115,50,50), cb=numberEnter, value = 10, bg='backspace'),
        "enter": Button((197,60,100,50), cb=numberEnter, value = 11, bg='enter'),        
        "cancel": Button((197,170,100,50), cb=numberEnter, value = 12, bg='cancel'),
        "textbox": Button((0,0,320,50), bg='textbox')
    })
    
def createText():
    global screens
    
    screens["main"].addTexts({
        "moving": Text("",(5, 5)),
        "sleep": Text("",(5, 48)),
        "frames": Text("",(5, 93)),
        "remaining": Text("",(5, 140))
    })
    
    screens["settings1"].addTexts({
        "shots": Text("",(5, 20)),
        "pulse": Text("",(5, 70)),
        "interval": Text("",(5, 125))
        #"settling": Text("",(5, 110)),
        #"shutterSpeed": Text("",(5, 145))
    })
    
    screens["numberEdit"].addTexts({
        "value": Text("",(5, 10))
    })

def updateText(screen):
    global shotNumber, timeRemaining, values
    
    if screen == "main":
        screens["main"].setText("moving", "Moving: " + str(values["pulse"]) + "ms")
        screens["main"].setText("sleep", "Interval: " + str(values["interval"]) + "ms")
        screens["main"].setText("frames", "Frames: " + str(shotNumber) + " of " + str(values["shots"]))
        screens["main"].setText("remaining", "Remaining: " + str(timedelta(seconds=timeRemaining)))
    elif screen == "settings1":
        screens["settings1"].setText("shots",        "Shots   : " + str(values["shots"]))
        screens["settings1"].setText("pulse",        "Pulse   : " + str(values["pulse"]) + "ms")
        screens["settings1"].setText("interval",     "Interval: " + str(values["interval"]) + "ms")
        #screens["settings1"].setText("settling",     "Settling      : " + str(values["settling"]) + "ms")
        #screens["settings1"].setText("shutterSpeed", "Shutter Speed : " + str(values["shutterSpeed"]) + "ms")
    elif screen == "numberEdit":
        screens["numberEdit"].setText("value", str(numberString))
 

def controlMotor(moving):
    global pins, motorRunning, allowMotion
    
    motorRunning = moving
    print("Moving: " + str(moving))
    
    if moving:
        if ((direction == 0 and allowMotion <= 0)):
            #gpio.digitalWrite(pins["motorA"],gpio.HIGH)
            pass
        elif (direction == 1 and allowMotion >= 0):
            #gpio.digitalWrite(pins["motorB"],gpio.HIGH)
            pass
    else:
        #gpio.digitalWrite(pins["motorA"],gpio.LOW)
        #gpio.digitalWrite(pins["motorB"],gpio.LOW)
        pass
        
def takePic():
    global pins, values
    
    print("Take Pic")
    
    #gpio.digitalWrite(pins["GROUND"], gpio.HIGH)
    #gpio.digitalWrite(pins["FOCUS"], gpio.HIGH)
    #gpio.digitalWrite(pins["SHUTTER"], gpio.HIGH)
    
    sleep(float(values["shutterSpeed"]) / 1000)
    
    #gpio.digitalWrite(pins["GROUND"], gpio.LOW)
    #gpio.digitalWrite(pins["FOCUS"], gpio.LOW)
    #gpio.digitalWrite(pins["SHUTTER"], gpio.LOW)

        
def startTouch(n):
    global takingPics, GRID_LOCK, shotNumber
    if n == 1 and not takingPics:
        #Start
        print("Start Pics")
        takingPics = True
        pictures = Pictures()
        pictures.start()
    elif n == 0:
        #Stop
        print("Stop Pics")
        takingPics = False
        GRID_LOCK.acquire()
        shotNumber = 0;
        GRID_LOCK.release()
        
def changePageTouch(n):
    global currentScreen, takingPics, returnScreen
    if n == 0:
        currentScreen = "main"
    elif n == 1 and not takingPics:
        currentScreen = "settings1"
    elif n == 2:
        currentScreen = "settings2"
        
def editEnd(n):
    global currentScreen, returnScreen
    currentScreen = returnScreen
    
def numberEnter(n):
    global currentScreen, returnScreen
    global numberString
    
    if n < 10:
        if (len(str(numberString)) > 5):
            return
        temp = ""
        if (numberString != 0):
            temp = str(numberString)
        numberString = int((temp + str(n)))
    elif n == 10:
        temp = str(numberString)[:-1]
        if (temp == ""):
            temp = 0
        numberString = int(temp)
    elif n == 11:
        currentScreen = returnScreen
        values[currentEdit] = numberString
    elif n == 12:
        currentScreen = returnScreen
        
    
def numberEdit(n):
    global currentScreen, returnScreen, numberString, values, currentEdit
    
    returnScreen = currentScreen
    currentScreen = "numberEdit"
    if n == 1:
        currentEdit = "shots"
    elif n == 2:
        currentEdit = "pulse"
    elif n == 3:
        currentEdit = "interval"

    numberString = values[currentEdit]
    
pins = {"GROUND"    : 15, #White
        "FOCUS"     : 11, #Yellow
        "SHUTTER"   : 13, #RED
        "motorA"    : 0,
        "motorB"    : 0,
        "leftTrig"  : 0,
        "rightTrig" : 0}

values = {"shots"        :  100,
          "shutterSpeed" :  200, # in ms time shutter is open (maybe this number might not actually matter and is only used because it needs to be open at least this long)
          "pulse"        :  500, # in ms time the rig moves
          "interval"     : 1000, # in ms between next move and picture
          "settling"     :  200 # in ms time between stop moving and taking pic
          }
currentEdit = ""
shotNumber = 0
timeRemaining = 0
direction = 1
screens = {}
motorRunning = False
allowMotion = 0
iconPath        = 'images'
icons = [] # This list gets populated at startup
currentScreen = "main"
returnScreen = ""
GRID_LOCK = threading.Lock()
takingPics = False
runs = 1
numberString = 0

def signal_handler(signal, frame):
    global runs, takingPics, GRID_LOCK
    GRID_LOCK.acquire()
    runs = 0
    takingPics = False
    GRID_LOCK.release()
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
    
    timeRemaining = int(((values["shots"] - shotNumber) * (values["settling"] + values["pulse"] + values["shutterSpeed"] + ((values["interval"] - values["shutterSpeed"]) if values["interval"] > values["shutterSpeed"] else 0))) / 1000)
    
    updateText(currentScreen)
    screens[currentScreen].update()
    screens[currentScreen].draw(screen)
    

    pygame.display.flip()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            GRID_LOCK.acquire()
            runs = 0
            takingPics = False
            GRID_LOCK.release()
        elif(event.type is MOUSEBUTTONDOWN):
            pos = pygame.mouse.get_pos()
            for b in screens[currentScreen].buttons.values():
                if b.selected(pos): break
        elif(event.type is MOUSEBUTTONUP):
            motorRunning = False
        
        
        
        
        #gpio.digitalWrite(motorpinA,gpio.LOW)
        #gpio.digitalWrite(motorpinB,gpio.LOW)
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
