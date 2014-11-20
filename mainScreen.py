#! /bin/python

import pygame, time, datetime
from button import Button
from settings import Settings
import threading

GRID_LOCK = threading.Lock()
RUNNING = 0
SHOT_NUMBER = 0
TIME_REMAINING = 0
    
class MainScreen:
    pygame.font.init()

    
    def __init__(self):
        global SHOT_NUMBER
        self.shots = 20
        self.interval = 100 # in ms
        self.wait = 500 # in ms
        
        self.myfont = pygame.font.SysFont("monospace", 15)
        
        #self.shots_label = self.myfont.render("Shots Remaining: " + str(SHOT_NUMBER) + " of " + str(self.shots), 1, (0,0,0))
        #self.interval_label = self.myfont.render("Some text!", 1, (255,255,255))
        #self.time_label = self.myfont.render("", 1, (255,255,255))
        
        self.start = Button('start.png', (5,185), "START")
        self.stop = Button('stop.png', (215,185), "STOP")
        self.settings = Button('stop.png', (110,185), "SETTINGS")
        
        self.buttons = (self.start, self.stop, self.settings)
        self.allsprites = pygame.sprite.RenderPlain(self.buttons)
        
    def clicked(self, x, y):
        global RUNNING, SHOT_NUMBER, GRID_LOCK
        buttonClicked = [sprite for sprite in self.buttons if sprite.rect.collidepoint(x, y)]
        if (len(buttonClicked) > 0):
            if (buttonClicked[0].clicked() == "SETTINGS"):
                return Settings(self.shots, self.interval, self.wait, self)
            if (buttonClicked[0].clicked() == "START"):
                RUNNING = 1
                self.pictures = Pictures(self.shots, self.interval, self.wait)
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
        global SHOT_NUMBER, TIME_REMAINING
        self.allsprites.update()
        
        TIME_REMAINING = (self.shots - SHOT_NUMBER) * (self.wait / 1000)
        
        self.shots_label = self.myfont.render("Shots Remaining: " + str(SHOT_NUMBER) + " of " + str(self.shots), 1, (0,0,0))
        self.time_label = self.myfont.render( "Time Remaining : " + str(datetime.timedelta(seconds=TIME_REMAINING)), 1, (0,0,0))
        
        
    def draw(self, screen):
        self.allsprites.draw(screen)
        screen.blit(self.shots_label, (5, 5))
        screen.blit(self.time_label, (5, 30))
        
        
        
class Pictures(threading.Thread):

    def __init__(self, shots, interval, wait):
        threading.Thread.__init__(self)
        self.shots = shots
        self.interval = interval
        self.wait = wait
        
    def run(self):
        global RUNNING, SHOT_NUMBER, GRID_LOCK, TIME_REMAINING
        
        while True:
            GRID_LOCK.acquire()
            if (not RUNNING):
                GRID_LOCK.release()
                return
                
            
                
            time.sleep(self.wait / 1000)
            
            
            SHOT_NUMBER += 1
            
            if (SHOT_NUMBER >= self.shots):
                RUNNING = 0
            
            GRID_LOCK.release()
        