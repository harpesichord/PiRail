#! /bin/python

import pygame, os, sys
from pygame.locals import *

class Button(pygame.sprite.Sprite):

    def __init__(self, image, position, text):
        pygame.sprite.Sprite.__init__(self) #call Sprite intializer
        self.image, self.rect = self.load_image(image, 255)
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.rect.topleft = position
        self.text = text
        
    def update(self):
        t = 1
        
    def clicked(self):
        #if (self.rect.colliderect(pos)):
        return self.text
            
    def load_image(self, name, colorkey=None):
        fullname = os.path.join('images', name)
        try:
            image = pygame.image.load(fullname)
        except pygame.error:
            print ('Cannot load image:', name)
            raise SystemExit
        image = image.convert()
        if colorkey is not None:
            if colorkey is -1:
                colorkey = image.get_at((0,0))
            image.set_colorkey(colorkey, RLEACCEL)
        return image, image.get_rect()
