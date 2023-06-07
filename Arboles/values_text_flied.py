from text_field import text_field

class values_text_field(text_field):

    def __init__(self,coords,font):
        super().__init__(coords,font)
        self.text = ""

    def write_char(self, character):
        if self.selected:
            self.text = self.text + character
        
            self.text_render = self.font.render(self.text,True,(50,50,50))
    
    def delete_char(self):
        if self.selected:
            self.text = self.text[:len(self.text)-1]
            self.text_render = self.font.render(self.text,True,(50,50,50))