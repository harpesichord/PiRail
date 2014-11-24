#! /bin/python

import pygame, time, datetime
#import RPi.GPIO as GPIO
from button import Button
from settings import Settings
import threading, os

GRID_LOCK = threading.Lock()
RUNNING = 0
SHOT_NUMBER = 0
TIME_REMAINING = 0
SHUTTER_WAIT = 200
PINS = {}    
    
class MainScreen:
    pygame.font.init()

    
    def __init__(self, pins_dic):
        global SHOT_NUMBER, PINS
        
        pins = pins_dic
        self.shots = 100
        self.interval = 500 # in ms time the rig moves
        self.wait = 1000 # in ms between moving and taking picture
        self.direction = 1
        
        self.myfont = pygame.font.SysFont("monospace", 25)
        
        #self.shots_label = self.myfont.render("Shots Remaining: " + str(SHOT_NUMBER) + " of " + str(self.shots), 1, (0,0,0))
        #self.interval_label = self.myfont.render("Some text!", 1, (255,255,255))
        #self.time_label = self.myfont.render("", 1, (255,255,255))
        
        self.start = Button('start.png', (5,185), "START")
        self.stop = Button('stop.png', (215,185), "STOP")
        self.settings = Button('settings.png', (110,185), "SETTINGS")
        
        self.buttons = (self.start, self.stop, self.settings)
        self.allsprites = pygame.sprite.RenderPlain(self.buttons)
        
    def clicked(self, x, y):
        global RUNNING, SHOT_NUMBER, GRID_LOCK
        buttonClicked = [sprite for sprite in self.buttons if sprite.rect.collidepoint(x, y)]
        if (len(buttonClicked) > 0):
            if (buttonClicked[0].clicked() == "SETTINGS" and not RUNNING):
                return Settings(self.shots, self.interval, self.wait, self.direction, self)
            if (buttonClicked[0].clicked() == "START"):
                RUNNING = 1
                self.pictures = Pictures(self.shots, self.interval, self.wait, self.direction)
                self.pictures.start()
            if (buttonClicked[0].clicked() == "STOP"):
                GRID_LOCK.acquire()
                RUNNING = 0
                SHOT_NUMBER = 0
                GRID_LOCK.release()
                
            print (buttonClicked[0].clicked())
        
    def stops(self):
        global RUNNING
        GRID_LOCK.acquire()
        RUNNING = 0
        GRID_LOCK.release()

        
    def update(self):
        global SHOT_NUMBER, TIME_REMAINING, SHUTTER_WAIT
        #GRID_LOCK.acquire()
        self.allsprites.update()
        
        
        
        TIME_REMAINING = int(((self.shots - SHOT_NUMBER) * ((self.wait) + (SHUTTER_WAIT) + (self.interval))) / 1000)
        
        self.moving_label = self.myfont.render("Moving: " + str(self.interval) + "ms", 1, (0,0,0))
        self.wait_label = self.myfont.render(  "Sleep:  " + str(self.wait) + "ms", 1, (0,0,0))
        self.shots_label = self.myfont.render( "Frames: " + str(SHOT_NUMBER) + " of " + str(self.shots), 1, (0,0,0))
        self.time_label = self.myfont.render(  "Remaining: " + str(datetime.timedelta(seconds=TIME_REMAINING)), 1, (0,0,0))
        
        #GRID_LOCK.release()
        
    def draw(self, screen):
        self.allsprites.draw(screen)
        screen.blit(self.moving_label, (5, 5))
        screen.blit(self.wait_label,   (5, 48))
        screen.blit(self.shots_label,  (5, 93))
        screen.blit(self.time_label,   (5, 140))
        
        
        
class Pictures(threading.Thread):

    def __init__(self, shots, interval, wait, direction):
        threading.Thread.__init__(self)
        self.shots = shots
        self.interval = interval
        self.wait = wait
        self.direction = direction
        
    def run(self):
        global RUNNING, SHOT_NUMBER, GRID_LOCK, TIME_REMAINING, PINS, SHUTTER_WAIT
        
        while True:
            GRID_LOCK.acquire()
            if (not RUNNING):
                GRID_LOCK.release()
                return
                
                
            # Moving
            # Start Moving
            time.sleep(self.interval / 1000)
            # Stop Moving
            
            # Take Picture
            #os.system('python take_picture.py ' + str(pins["GROUND"]) + ' ' + str(pins["FOCUS"]) + ' ' + str(pins["SHUTTER"]) + ' ' + str(SHUTTER_WAIT))
            
            
            # Wait
            time.sleep(self.wait / 1000)
            
            
            
            
            SHOT_NUMBER += 1
            
            if (SHOT_NUMBER >= self.shots):
                RUNNING = 0
            
            GRID_LOCK.release()
        