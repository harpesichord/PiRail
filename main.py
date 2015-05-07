#! /bin/python

import os, io, pygame, signal, sys
import wiringpi2
#import RPi.GPIO as GPIO
from datetime import datetime
from mainScreen import MainScreen
import globals, threading

globals.init()


globals.globs["camera_pins"] = {"GROUND":15, #WHITE
        "FOCUS":11, #YELLOW
        "SHUTTER":13} #RED
globals.globs["motor_pins"] = {"A":0, "B":0}        
globals.globs["trigger_pins"] = {"LEFT":0, "RIGHT":0}    
globals.globs["SHOT_NUMBER"] = 0
globals.globs["TIME_REMAINING"] = 0
globals.globs["SHUTTER_WAIT"] = 200
globals.globs["shots"] = 100
globals.globs["interval"] = 500 # in ms time the rig moves
globals.globs["wait"] = 1000 # in ms between moving and taking picture
globals.globs["direction"] = 1
globals.globs["screens"] = []
globals.globs["motor_running"] = False
globals.globs["allow_motion"] = 0


def signal_handler(signal, frame):
    global runs
    runs = 0
    gpioCleanup()
    #GPIO.cleanup()
    while (len(globals.globs["screens"]) > 0):
        globals.globs["screens"].pop().stops()
        
    sys.exit(0)
    
def gpioCleanup():
    gpio.digitalWrite(globals.globs["motor_pins"]["A"],gpio.LOW)
    gpio.digitalWrite(globals.globs["motor_pins"]["B"],gpio.LOW)
    
    os.system("echo 'out' > /sys/class/gpio/gpio508/direction")
    gpio.pinMode(globals.globs["motor_pins"]["A"],0)
    gpio.pinMode(globals.globs["motor_pins"]["B"],0)
    gpio.pinMode(globals.globs["trigger_pins"]["LEFT"],0)
    gpio.pinMode(globals.globs["trigger_pins"]["RIGHT"],0)
    gpio.pinMode(globals.globs["camera_pins"]["GROUND"],0)
    gpio.pinMode(globals.globs["camera_pins"]["FOCUS"],0)
    gpio.pinMode(globals.globs["camera_pins"]["SHUTTER"],0)

def gpio_init():
    print("INITINT GPIO")
    gpio = wiringpi2.GPIO(wiringpi2.GPIO.WPI_MODE_GPIO)  
    ##GPIO.setmode(GPIO.BOARD)
    #os.system("echo 252 > /sys/class/gpio/export")
    #os.system("echo 'out' > /sys/class/gpio/gpio252/direction")
    #os.system("echo '1' > /sys/class/gpio/gpio252/value")
    
    #gpio.pinMode(globals.globs["motor_pins"]["A"],gpio.OUTPUT)
    #gpio.pinMode(globals.globs["motor_pins"]["B"],gpio.OUTPUT)
    #gpio.pinMode(globals.globs["trigger_pins"]["LEFT"],gpio.INPUT)
    #gpio.pinMode(globals.globs["trigger_pins"]["RIGHT"],gpio.INPUT)
    gpio.pinMode(globals.globs["camera_pins"]["GROUND"],gpio.OUTPUT)
    gpio.pinMode(globals.globs["camera_pins"]["FOCUS"],gpio.OUTPUT)
    gpio.pinMode(globals.globs["camera_pins"]["SHUTTER"],gpio.OUTPUT)

    
def triggering():
    while (runs):
        pass
        #if left side triggers set var to 1
        #if right side triggers set var to -1
        #if neither trigger set var to 0
        #if anyside triggers stop motion.
        

os.putenv('SDL_VIDEODRIVER', 'fbcon')
os.putenv('SDL_FBDEV'      , '/dev/fb1')
os.putenv('SDL_MOUSEDRV'   , 'TSLIB')
os.putenv('SDL_MOUSEDEV'   , '/dev/input/touchscreen')

print("STARTED")
gpio_init()
pygame.init()
pygame.font.init()
pygame.mouse.set_visible(False)
modes = pygame.display.list_modes(16)
#screen = pygame.display.set_mode(modes[0], FULLSCREEN, 16)

screen = pygame.display.set_mode((320, 240), pygame.SRCALPHA)
runs = 1
main = MainScreen()
globals.globs["screens"].append(main)

clock = pygame.time.Clock()


print("Showing")

t = threading.Thread(target=triggering)
t.start()
    
signal.signal(signal.SIGINT, signal_handler)

while runs:
    clock.tick(30)
    
    #screen.fill((224,224,224))
    img    = pygame.image.load("images/background.jpg")
    screen.blit(img,
    ((320 - img.get_width() ) / 2,
     (240 - img.get_height()) / 2))
    
    
    globals.globs["screens"][-1].update()
    globals.globs["screens"][-1].draw(screen)

    pygame.display.flip()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            runs = 0
            while (len(globals.globs["screens"]) > 0):
                globals.globs["screens"].pop().stops()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            globals.globs["screens"][-1].clicked(x, y)
        elif event.type == pygame.MOUSEBUTTONUP:      
            if (globals.globs["motor_running"]):
                globals.globs["motor_running"] = False
                # Stop Motor
                gpio.digitalWrite(globals.globs["motor_pins"]["A"],gpio.LOW)
                gpio.digitalWrite(globals.globs["motor_pins"]["B"],gpio.LOW)
                
                
gpioCleanup    
#GPIO.cleanup()    
print("DONE")
pygame.quit()
