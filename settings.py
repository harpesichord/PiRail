#! /bin/python

import pygame
from button import Button
import globals
#import RPi.GPIO as GPIO
import threading, os

pygame.font.init()

class Settings:
    running = 0
    
    def __init__(self):
        self.myfont = pygame.font.SysFont("monospace", 25)
        
        # PAGE 1 buttons
        self.edit_shots = Button('edit.png', (265,5), "EDIT_SHOTS")
        self.edit_interval = Button('edit.png', (265,60), "EDIT_INTERVAL")
        self.edit_wait = Button('edit.png', (265,115), "EDIT_WAIT")
        self.go_back = Button('go_back.png', (5,185), "GO_BACK")
        self.next = Button('right.png', (265,185), "NEXT_PAGE")
        
        # PAGE 2 buttons
        self.direction_btn = Button('edit.png', (265,5), "DIRECTION")
        self.move_platform = Button('edit.png', (265,60), "MOVE_PLATFORM")
        #self.edit_wait = Button('edit.png', (265,115), "EDIT_WAIT")
        self.go_back = Button('go_back.png', (5,185), "GO_BACK")
        self.previous = Button('left.png', (210,185), "PREVIOUS_PAGE")
        
        self.page_1()
        
        
    def page_1(self):
        self.buttons = (self.edit_shots, self.edit_interval, self.edit_wait, self.go_back, self.next)
        self.allsprites = pygame.sprite.RenderPlain(self.buttons)
        self.page = 1
        
    def page_2(self):
        self.buttons = (self.direction_btn, self.move_platform, self.go_back, self.previous)
        self.allsprites = pygame.sprite.RenderPlain(self.buttons)
        self.page = 2
        
    def clicked(self, x, y):
        buttonClicked = [sprite for sprite in self.buttons if sprite.rect.collidepoint(x, y)]
        if (len(buttonClicked) > 0):
            if (buttonClicked[0].clicked() == "NEXT_PAGE"):
                if (self.page == 1):
                    self.page_2()
            elif (buttonClicked[0].clicked() == "PREVIOUS_PAGE"):
                if (self.page == 2):
                    self.page_1()
            elif (buttonClicked[0].clicked() == "GO_BACK"):
                globals.globs["screens"].pop()
            elif (buttonClicked[0].clicked() == "EDIT_SHOTS"):
                globals.globs["screens"].append(Edit("EDIT_SHOTS", globals.globs["shots"], "shots"))
            elif (buttonClicked[0].clicked() == "EDIT_INTERVAL"):
                globals.globs["screens"].append(Edit("EDIT_INTERVAL", globals.globs["interval"], "interval"))
            elif (buttonClicked[0].clicked() == "EDIT_WAIT"):
                globals.globs["screens"].append(Edit("EDIT_WAIT", globals.globs["wait"], "wait"))
            elif (buttonClicked[0].clicked() == "DIRECTION"):
                globals.globs["screens"].append(Edit("DIRECTION", globals.globs["direction"], "direction"))
            elif (buttonClicked[0].clicked() == "MOVE_PLATFORM"):
                globals.globs["screens"].append(Edit("MOVE_PLATFORM", None, None))
                
            print (buttonClicked[0].clicked())
        
    
    def update(self):
        self.allsprites.update()
        
        self.shots_label = self.myfont.render(  "Shots:    " + str(globals.globs["shots"]), 1, (0,0,0))
        self.moving_label = self.myfont.render( "Interval: " + str(globals.globs["interval"]) + "ms", 1, (0,0,0))
        self.waiting_label = self.myfont.render("Waiting:  " + str(globals.globs["wait"]) + "ms", 1, (0,0,0))
        
        self.direction_label = self.myfont.render("Direction:  " + ("Left" if globals.globs["direction"] == 0 else "Right"), 1, (0,0,0))
        self.move_platform_label = self.myfont.render("Move Platform", 1, (0,0,0))
        
        
    def stops(self):
        pass
        
    def draw(self, screen):
        self.allsprites.draw(screen)
        
        if (self.page == 1):
            screen.blit(self.shots_label, (5, 20))
            screen.blit(self.moving_label, (5, 70))
            screen.blit(self.waiting_label, (5, 125))
        elif (self.page == 2):
            screen.blit(self.direction_label, (5, 20))
            screen.blit(self.move_platform_label, (5, 70))
            
            
class Edit:


    def __init__(self, type, value, old_val):
        self.type = type
        self.old_val = old_val
        self.value = value
        self.myfont = pygame.font.SysFont("monospace", 25)
        self.setButtons()
        self.motor = False
        self.GRID_LOCK = threading.Lock()
        
    def setButtons(self):
        if (self.type == "EDIT_SHOTS" or self.type == "EDIT_INTERVAL" or self.type == "EDIT_WAIT"):
            self.num0 = Button('0.png', (197,115), "0")
            self.num1 = Button('1.png', (32,60), "1")
            self.num2 = Button('2.png', (87,60), "2")
            self.num3 = Button('3.png', (142,60), "3")
            self.num4 = Button('4.png', (32,115), "4")
            self.num5 = Button('5.png', (87,115), "5")
            self.num6 = Button('6.png', (142,115), "6")
            self.num7 = Button('7.png', (32,170), "7")
            self.num8 = Button('8.png', (87,170), "8")
            self.num9 = Button('9.png', (142,170), "9")
            self.enter = Button('enter.png', (197,60), "ENTER")
            self.backspace = Button('backspace.png', (247,115), "BACKSPACE")
            self.cancel = Button('cancel.png', (197,170), "CANCEL")
            self.textbox = Button('textbox.png', (0,0), "TEXT")
            
            self.buttons = (self.num0, self.num1, self.num2, self.num3, self.num4, self.num5, self.num6, self.num7, self.num8, self.num9, self.enter, self.backspace, self.cancel, self.textbox)
            self.allsprites = pygame.sprite.RenderPlain(self.buttons)
            
        if (self.type == "DIRECTION"):
            self.left_dir = Button('left_dir.png', (73,40), "LEFT_DIR")
            self.right_dir = Button('right_dir.png', (197,40), "RIGHT_DIR")
            self.enter = Button('enter.png', (5,185), "ENTER")
            self.cancel = Button('cancel.png', (110,185), "CANCEL")
            
            self.buttons = (self.enter, self.cancel, self.left_dir, self.right_dir)
            self.allsprites = pygame.sprite.RenderPlain(self.buttons)
            
        if (self.type == "MOVE_PLATFORM"):
            self.rewind = Button('rewind.png', (80,37), "REWIND")
            self.fastforward = Button('fastforward.png', (190,37), "FAST_FORWARD")
            self.left = Button('left.png', (80,92), "MOVE_LEFT")
            self.right = Button('right.png', (190,92), "MOVE_RIGHT")
            self.cancel = Button('enter.png', (5,185), "CANCEL")
            self.stop = Button('stop.png', (110,185), "STOP")
            
            self.buttons = (self.cancel, self.rewind, self.fastforward, self.left, self.right, self.stop)
            self.allsprites = pygame.sprite.RenderPlain(self.buttons)
            
            
    def clicked(self, x, y):    
        buttonClicked = [sprite for sprite in self.buttons if sprite.rect.collidepoint(x, y)]
        
        if (len(buttonClicked) > 0):
            if (buttonClicked[0].clicked().isdigit()):
                if (len(str(self.value)) > 10):
                    return
                
                temp = ""
                if (self.value != 0):
                    temp = str(self.value)
                self.value = int((temp + buttonClicked[0].clicked()))
            elif (buttonClicked[0].clicked() == "BACKSPACE"):
                temp = str(self.value)[:-1]
                if (temp == ""):
                    temp = 0
                self.value = int(temp)
            elif (buttonClicked[0].clicked() == "ENTER"):
                self.stops()
                self.goBack()
                globals.globs["screens"].pop()
            elif (buttonClicked[0].clicked() == "CANCEL"):
                self.stops()
                globals.globs["screens"].pop()  
            elif (buttonClicked[0].clicked() == "LEFT_DIR"):
                self.value = 0
            elif (buttonClicked[0].clicked() == "RIGHT_DIR"):
                self.value = 1
            elif (buttonClicked[0].clicked() == "MOVE_LEFT"):
                if (globals.globs["allow_motion"] <= 0):
                    globals.globs["motor_running"] = True
                    #gpio.digitalWrite(globals.globs["motor_pins"]["A"],gpio.HIGH)
            elif (buttonClicked[0].clicked() == "MOVE_RIGHT"):
                if (globals.globs["allow_motion"] >= 0):
                    globals.globs["motor_running"] = True
                    #gpio.digitalWrite(globals.globs["motor_pins"]["B"],gpio.HIGH)
            elif (buttonClicked[0].clicked() == "FAST_FORWARD"):
                self.GRID_LOCK.acquire()
                if (not self.motor and globals.globs["allow_motion"] >= 0):
                    self.value = 1
                    self.motor = True
                    self.t = threading.Thread(target=self.moving)
                    self.t.start()
                self.GRID_LOCK.release()
            elif (buttonClicked[0].clicked() == "REWIND"):
                self.GRID_LOCK.acquire()
                if (not self.motor and globals.globs["allow_motion"] <= 0):
                    self.value = -1
                    self.motor = True
                    self.t = threading.Thread(target=self.moving)
                    self.t.start()
                self.GRID_LOCK.release()
            elif (buttonClicked[0].clicked() == "STOP"):
                self.GRID_LOCK.acquire()
                self.motor = False
                self.GRID_LOCK.release()
                
    def goBack(self):
        if (self.type != None):
                globals.globs[self.old_val] = self.value
        
            
    def update(self):
        self.allsprites.update()   

        if (self.type == "EDIT_SHOTS" or self.type == "EDIT_INTERVAL" or self.type == "EDIT_WAIT"):
            self.value_label = self.myfont.render(str(self.value), 1, (0,0,0))
        
    def stops(self):
        self.GRID_LOCK.acquire()
        self.motor = False
        self.GRID_LOCK.release()
        
    def draw(self, screen):
        self.allsprites.draw(screen)
        
        if (self.type == "EDIT_SHOTS" or self.type == "EDIT_INTERVAL" or self.type == "EDIT_WAIT"):
            screen.blit(self.value_label, (5, 10))
        if (self.type == "DIRECTION"):
            if (self.value == 0):
                pygame.draw.rect(screen, (0,0,0), pygame.Rect((58,25), (80, 130)), 5)
            elif (self.value == 1):
                pygame.draw.rect(screen, (0,0,0), pygame.Rect((182,25), (80, 130)), 5)
                
                
    def moving(self):
        if (self.value == -1):
            pass
            #gpio.digitalWrite(globals.globs["motor_pins"]["A"],gpio.HIGH)
        elif (self.value == 1):
            pass
            #gpio.digitalWrite(globals.globs["motor_pins"]["B"],gpio.HIGH)
        
        while (True):
            self.GRID_LOCK.acquire()
            if (not self.motor or (self.value == -1 and globals.globs["allow_motion"] > 0) or (self.value == 1 and globals.globs["allow_motion"] < 0)):
                self.GRID_LOCK.release()
                break
            #just loops through and keeps checking if the wall switch is activated then stop motor
            
            self.GRID_LOCK.release()
            
        #gpio.digitalWrite(globals.globs["motor_pins"]["A"],gpio.LOW)    
        #gpio.digitalWrite(globals.globs["motor_pins"]["B"],gpio.LOW)    
            