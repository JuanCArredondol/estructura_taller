import pygame

class text_field:

    def __init__(self,coords,font):
        self.selected = False
        self.x = coords[0]
        self.y = coords[1]
        self.width = 250
        self.height = 50
        self.text = "0"
        self.font = font
        self.text_render = self.font.render(self.text,True,(50,50,50))
    
    def toggle_selected(self, mouse_position):
        self.selected = (mouse_position[0] > self.x and 
            mouse_position[1] > self.y and 
            mouse_position[0] < self.x + self.width and 
            mouse_position[1] < self.y + self.height)
            
    def write_char(self, character):
        if self.selected:
            self.text = self.text + character
            self.text_render = self.font.render(self.text,True,(50,50,50))

    def delete_char(self):
        if self.selected:
            self.text = self.text[:len(self.text)-1]
            self.text_render = self.font.render(self.text,True,(50,50,50))

    def draw(self, screen):
        pygame.draw.rect(screen,(150,150,150),pygame.Rect(self.x,self.y,self.width,self.height))
        screen.blit(self.text_render,(self.x+10,self.y+10))
