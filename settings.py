#! /bin/python

import pygame
from button import Button

pygame.font.init()

class Settings:
    running = 0
    
    def __init__(self, shots, interval, wait, direction, previous_screen):
        self.shots = shots
        self.interval = interval # in ms
        self.wait = wait # in ms
        self.direction = direction
        self.myfont = pygame.font.SysFont("monospace", 25)
        self.previous_screen = previous_screen
        
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
            if (buttonClicked[0].clicked() == "PREVIOUS_PAGE"):
                if (self.page == 2):
                    self.page_1()
            if (buttonClicked[0].clicked() == "GO_BACK"):
                self.goBack()
                return self.previous_screen
            if (buttonClicked[0].clicked() == "EDIT_SHOTS"):
                return Edit("EDIT_SHOTS", self.shots, self)
            if (buttonClicked[0].clicked() == "EDIT_INTERVAL"):
                return Edit("EDIT_INTERVAL", self.interval, self)
            if (buttonClicked[0].clicked() == "EDIT_WAIT"):
                return Edit("EDIT_WAIT", self.wait, self)
            if (buttonClicked[0].clicked() == "DIRECTION"):
                return Edit("DIRECTION", self.direction, self)
            if (buttonClicked[0].clicked() == "MOVE_PLATFORM"):
                return Edit("MOVE_PLATFORM", None, self)
                
            print (buttonClicked[0].clicked())
        
        
    def goBack(self):
        self.previous_screen.shots = self.shots
        self.previous_screen.interval = self.interval
        self.previous_screen.wait = self.wait
    
    def update(self):
        self.allsprites.update()
        
        self.shots_label = self.myfont.render(  "Shots:    " + str(self.shots), 1, (0,0,0))
        self.moving_label = self.myfont.render( "Interval: " + str(self.interval) + "ms", 1, (0,0,0))
        self.waiting_label = self.myfont.render("Waiting:  " + str(self.wait) + "ms", 1, (0,0,0))
        
        self.direction_label = self.myfont.render("Direction:  " + ("Left" if self.direction == 0 else "Right"), 1, (0,0,0))
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


    def __init__(self, type, value, settings_page):
        self.type = type
        self.value = value
        self.settings_page = settings_page
        self.myfont = pygame.font.SysFont("monospace", 25)
        self.setButtons()
        
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
            self.rewind = Button('rewind.png', (32,60), "REWIND")
            self.fastforward = Button('fastforward.png', (142,60), "FAST_FORWARD")
            self.left = Button('left.png', (32,115), "MOVE_LEFT")
            self.right = Button('right.png', (142,115), "MOVE_RIGHT")
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
                self.goBack()
                return self.settings_page
            elif (buttonClicked[0].clicked() == "CANCEL"):
                return self.settings_page    
            elif (buttonClicked[0].clicked() == "LEFT_DIR"):
                self.value = 0
            elif (buttonClicked[0].clicked() == "RIGHT_DIR"):
                self.value = 1
                
                
    def goBack(self):
        if (self.type == "EDIT_SHOTS"):
            if (self.value > 0):
                self.settings_page.shots = self.value
        if (self.type == "EDIT_INTERVAL"):
            if (self.value > 0):
                self.settings_page.interval = self.value
        if (self.type == "EDIT_WAIT"):
            if (self.value > 0):
                self.settings_page.wait = self.value
        if (self.type == "DIRECTION"):
            self.settings_page.direction = self.value
            
            
    def update(self):
        self.allsprites.update()   

        if (self.type == "EDIT_SHOTS" or self.type == "EDIT_INTERVAL" or self.type == "EDIT_WAIT"):
            self.value_label = self.myfont.render(str(self.value), 1, (0,0,0))
        
    def stops(self):
        pass    
    
    def draw(self, screen):
        self.allsprites.draw(screen)
        
        if (self.type == "EDIT_SHOTS" or self.type == "EDIT_INTERVAL" or self.type == "EDIT_WAIT"):
            screen.blit(self.value_label, (5, 10))
        