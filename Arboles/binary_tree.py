import pygame

class Node:
    def __init__(self, value, font):
        self.value = value
        self.left = None
        self.right = None
        self.font = font
        self.text_render = self.font.render(str(self.value),True,(255,255,255))

    def insert(self, value):
        if self.value is None:
            self.value = value
        
        if self.value is not None:
            if value < self.value:
                if self.left is None:
                   self.left = Node(value,self.font)
                else:
                   self.left.insert(value)
            elif value > self.value:
                
                if self.right is None:
                    self.right = Node(value,self.font)
                else:
                    self.right.insert(value)
            else:
                self.value = value
        self.text_render = self.font.render(str(self.value),True,(255,255,255))
    def initialTraversal(self,coords, screen):
        if self.value is None:
            return
        if self:  
            pygame.draw.circle(screen, (0,0,0), coords, 40)
            screen.blit(self.text_render,(coords[0]-10,coords[1]-15))
            newCords = coords.copy()
            
            if self.left:
                self.left.leftTraversal(1,newCords,screen)
            if self.right:
                self.right.rightTraversal(1,newCords,screen)

    def rightTraversal(self, deepcounter, coords, screen):
        if self:   
            newCords = coords.copy()
            newCords[0] = coords[0] + 150 * (1/deepcounter)
            newCords[1] = coords[1] + 100
            pygame.draw.line(screen,(0,0,0),coords,newCords)
            pygame.draw.circle(screen, (0,0,0), newCords, 40)
            screen.blit(self.text_render,(newCords[0]-10,newCords[1]-15))
            deepcounter+=0.5
            
            if self.left:
                self.left.leftTraversal(deepcounter,newCords,screen)
            if self.right:
                self.right.rightTraversal(deepcounter,newCords,screen)
                
    def leftTraversal(self, deepcounter, coords, screen):
        if self:   
            newCords = coords.copy()
            newCords[0] = coords[0] - 150 * (1/deepcounter)
            newCords[1] = coords[1] + 100
            pygame.draw.line(screen,(0,0,0),coords,newCords)
            pygame.draw.circle(screen, (0,0,0), newCords, 40)
            screen.blit(self.text_render,(newCords[0]-10,newCords[1]-15))
            deepcounter+=0.5
            
            if self.left:
                self.left.leftTraversal(deepcounter,newCords,screen)
                print(self.value)
            if self.right:
                self.right.rightTraversal(deepcounter,newCords,screen)

    def resetTree(self):
        self.value = None
        self.left = None
        self.right = None