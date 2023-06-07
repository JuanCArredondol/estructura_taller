from text_field import text_field
import pygame

class number_text_field(text_field):

    def write_char(self, character):
        if self.selected:
            self.text = character
            self.text_render = self.font.render(self.text,True,(50,50,50))

    def draw(self, screen):
        pygame.draw.rect(screen,(150,150,150),pygame.Rect(self.x,self.y,self.width,self.height))
        screen.blit(self.text_render,(self.x-10+self.width/2,self.y+10))
