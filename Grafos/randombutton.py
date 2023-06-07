import pygame
from button import Button
class randombutton(Button):

    def __init__(self,coords):
        self.coords = coords
        self.x = coords[0]-8
        self.y = coords[1]-8
        self.radius = 16
        self.width = 32
        self.height = 32

    def draw(self, screen):
        pygame.draw.circle(screen,(123,252,48),self.coords,self.radius)
        
            
