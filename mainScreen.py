#! /bin/python

import pygame, time, datetime
import wiringpi2
#import RPi.GPIO as GPIO
from button import Button
from settings import Settings
import threading, os
import globals

GRID_LOCK = threading.Lock()
RUNNING = 0


    
class MainScreen:
    pygame.font.init()

    
    def __init__(self):
        self.myfont = pygame.font.SysFont("monospace", 25)
        
        self.start = Button('start.png', (5,185), "START")
        self.stop = Button('stop.png', (215,185), "STOP")
        self.settings = Button('settings.png', (110,185), "SETTINGS")
        
        self.buttons = (self.start, self.stop, self.settings)
        self.allsprites = pygame.sprite.RenderPlain(self.buttons)
        
    def clicked(self, x, y):
        global RUNNING, GRID_LOCK
        buttonClicked = [sprite for sprite in self.buttons if sprite.rect.collidepoint(x, y)]
        if (len(buttonClicked) > 0):
            if (buttonClicked[0].clicked() == "SETTINGS" and not RUNNING):
                globals.globs["screens"].append(Settings())
            if (buttonClicked[0].clicked() == "START"):
                RUNNING = 1
                self.pictures = Pictures()
                self.pictures.start()
            if (buttonClicked[0].clicked() == "STOP"):
                GRID_LOCK.acquire()
                RUNNING = 0
                globals.globs["SHOT_NUMBER"] = 0
                GRID_LOCK.release()
                
            print (buttonClicked[0].clicked())
        
    def stops(self):
        global RUNNING
        GRID_LOCK.acquire()
        RUNNING = 0
        GRID_LOCK.release()

        
    def update(self):
        #GRID_LOCK.acquire()
        self.allsprites.update()
        
        
        
        globals.globs["TIME_REMAINING"] = int(((globals.globs["shots"] - globals.globs["SHOT_NUMBER"]) * ((globals.globs["wait"]) + (globals.globs["SHUTTER_WAIT"]) + (globals.globs["interval"]))) / 1000)
        
        self.moving_label = self.myfont.render("Moving: " + str(globals.globs["interval"]) + "ms", 1, (0,0,0))
        self.wait_label = self.myfont.render(  "Sleep:  " + str(globals.globs["wait"]) + "ms", 1, (0,0,0))
        self.shots_label = self.myfont.render( "Frames: " + str(globals.globs["SHOT_NUMBER"]) + " of " + str(globals.globs["shots"]), 1, (0,0,0))
        self.time_label = self.myfont.render(  "Remaining: " + str(datetime.timedelta(seconds=globals.globs["TIME_REMAINING"])), 1, (0,0,0))
        
        #GRID_LOCK.release()
        
    def draw(self, screen):
        self.allsprites.draw(screen)
        screen.blit(self.moving_label, (5, 5))
        screen.blit(self.wait_label,   (5, 48))
        screen.blit(self.shots_label,  (5, 93))
        screen.blit(self.time_label,   (5, 140))
        
        
        
class Pictures(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        
        
    def run(self):
        global RUNNING, GRID_LOCK
        
        while True:
            GRID_LOCK.acquire()
            if (not RUNNING):
                GRID_LOCK.release()
                return
                
                
            # Moving
            if ((globals.globs["direction"] == 0 and globals.globs["allow_motion"] <= 0) or (globals.globs["direction"] == 1 and globals.globs["allow_motion"] >= 0)):
                # Start Moving
                time.sleep(globals.globs["interval"] / 1000)
                # Stop Moving
            else:
                time.sleep(globals.globs["interval"] / 1000)
            
            #Turn off backlight
            os.system("echo '0' > /sys/class/gpio/gpio282/value")
            
            # Take Picture
            self.takePic(globals.globs["camera_pins"]["GROUND"], globals.globs["camera_pins"]["FOCUS"], globals.globs["camera_pins"]["SHUTTER"], globals.globs["SHUTTER_WAIT"])
            #os.system('python take_pic.py ' + str(globals.globs["camera_pins"]["GROUND"]) + ' ' + str(globals.globs["camera_pins"]["FOCUS"]) + ' ' + str(globals.globs["camera_pins"]["SHUTTER"]) + ' ' + str(globals.globs["SHUTTER_WAIT"]))
            
            #Turn on backlight
            os.system("echo '1' > /sys/class/gpio/gpio282/value")
            
            # Wait
            time.sleep(globals.globs["wait"] / 1000)
            
            
            
            
            globals.globs["SHOT_NUMBER"] += 1
            
            if (globals.globs["SHOT_NUMBER"] >= globals.globs["shots"]):
                RUNNING = 0
            
            GRID_LOCK.release()
        

    def takePic(self, GROUND, FOCUS, SHUTTER, shutter_speed):
        gpio.digitalWrite(GROUND, gpio.HIGH)
        gpio.digitalWrite(FOCUS, gpio.HIGH)
        gpio.digitalWrite(SHUTTER, gpio.HIGH)

        time.sleep(shutter_speed / 1000)

        gpio.digitalWrite(GROUND, gpio.LOW)
        gpio.digitalWrite(FOCUS, gpio.LOW)
        gpio.digitalWrite(SHUTTER, gpio.LOW)
