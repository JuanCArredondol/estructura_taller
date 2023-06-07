import pygame

class Button:

    def __init__(self, coords, font, text):
        self.selected = False
        self.x = coords[0]
        self.y = coords[1]
        self.width = 250
        self.height = 40
        self.text = text
        self.font = font
        self.text_render = self.font.render(self.text,True,(25,25,25))
        

    def is_click(self, mouse_position):
        return (mouse_position[0] > self.x and 
                mouse_position[1] > self.y and 
                mouse_position[0] < self.x + self.width and 
                mouse_position[1] < self.y + self.height)
    
    def draw(self, screen):
        pygame.draw.rect(screen,(100,150,240), pygame.Rect(self.x, self.y, self.width, self.height))
        screen.blit(self.text_render,(self.x + 5, self.y + 7))
            

    