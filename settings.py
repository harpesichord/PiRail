#! /bin/python

import pygame
from button import Button

class Settings:
    running = 0
    
    def __init__(self, shots, interval, wait, previous_screen):
        self.shots = shots
        self.interval = interval # in ms
        self.wait = wait # in ms
        
        self.previous_screen = previous_screen
        
        # PAGE 1 buttons
        self.edit_shots = Button('edit.png', (265,5), "EDIT_SHOTS")
        self.edit_interval = Button('edit.png', (265,60), "EDIT_INTERVAL")
        self.edit_wait = Button('edit.png', (265,115), "EDIT_WAIT")
        self.go_back = Button('go_back.png', (5,185), "GO_BACK")
        self.next = Button('left.png', (265,185), "NEXT_PAGE")
        
        # PAGE 2 buttons
        self.night_mode = Button('edit.png', (265,5), "NIGHT_MODE")
        #self.edit_interval = Button('edit.png', (265,60), "EDIT_INTERVAL")
        #self.edit_wait = Button('edit.png', (265,115), "EDIT_WAIT")
        self.go_back = Button('go_back.png', (5,185), "GO_BACK")
        self.previous = Button('left.png', (210,185), "PREVIOUS_PAGE")
        
        self.page_1()
        
        
    def page_1(self):
        self.buttons = (self.edit_shots, self.edit_interval, self.edit_wait, self.go_back, self.next)
        self.allsprites = pygame.sprite.RenderPlain(self.buttons)
        self.page = 1
        
    def page_2(self):
        self.buttons = (self.night_mode, self.go_back, self.previous)
        self.allsprites = pygame.sprite.RenderPlain(self.buttons)
        self.page = 2
        
    def clicked(self, x, y):
        buttonClicked = [sprite for sprite in self.buttons if sprite.rect.collidepoint(x, y)]
        if (len(buttonClicked) > 0):
            if (buttonClicked[0].clicked() == "NEXT_PAGE"):
                if (self.page == 1):
                    self.page_2()
            if (buttonClicked[0].clicked() == "PREVIOUS_PAGE"):
                if (self.page == 2):
                    self.page_1()
            if (buttonClicked[0].clicked() == "GO_BACK"):
                return self.previous_screen
                
            print (buttonClicked[0].clicked())
        
        
    def update(self):
        self.allsprites.update()
        
    def stops(self):
        pass
        
    def draw(self, screen):
        self.allsprites.draw(screen)