#! /bin/python

import pygame, signal, sys
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

print("STARTED")
pygame.font.init()
screen = pygame.display.set_mode((320, 240), pygame.SRCALPHA)
runs = 1
main = MainScreen()
globals.globs["screens"].append(main)

clock = pygame.time.Clock()

def signal_handler(signal, frame):
    global runs
    runs = 0
    #GPIO.cleanup()
    while (len(globals.globs["screens"]) > 0):
        globals.globs["screens"].pop().stops()
        
    sys.exit(0)

def gpio_init():
    pass
    #GPIO.setmode(GPIO.BOARD)
    
def triggering():
    while (runs):
        pass
        #if left side triggers set var to 1
        #if right side triggers set var to -1
        #if neither trigger set var to 0
        #if anyside triggers stop motion.
        

print("Showing")
t = threading.Thread(target=triggering)
t.start()
    
signal.signal(signal.SIGINT, signal_handler)
gpio_init()

while runs:
    clock.tick(60)
    
    screen.fill((255,255,255))
    
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
                #gpio.digitalWrite(globals.globs["motor_pins"]["A"],gpio.LOW)
                #gpio.digitalWrite(globals.globs["motor_pins"]["B"],gpio.LOW)
                
                
    
#GPIO.cleanup()    
print("DONE")
pygame.quit()
