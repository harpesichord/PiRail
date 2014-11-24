#! /bin/python

import pygame, signal, sys
#inport GPIO
from datetime import datetime
from mainScreen import MainScreen


pins = {"GROUND":15, #WHITE
        "FOCUS":11, #YELLOW
        "SHUTTER":13} #RED

pygame.font.init()
screen = pygame.display.set_mode((320, 240), pygame.SRCALPHA)
runs = 1
main = MainScreen(pins)
currentScreen = main

clock = pygame.time.Clock()

def signal_handler(signal, frame):
    global currentScreen, runs
    runs = 0
    #GPIO.cleanup()
    currentScreen.stops()
    sys.exit(0)

def gpio_init():
    pass
    #GPIO.setmode(GPIO.BOARD)
    
    
signal.signal(signal.SIGINT, signal_handler)
gpio_init()

while runs:
    clock.tick(60)
    
    screen.fill((255,255,255))
    
    currentScreen.update()
    currentScreen.draw(screen)

    pygame.display.flip()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            runs = 0
            currentScreen.stops()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            changed = currentScreen.clicked(x, y)
            if (changed != None):
                currentScreen = changed

              
    
    
#GPIO.cleanup()    
print("DONE")
pygame.quit()