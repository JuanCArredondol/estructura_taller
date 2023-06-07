import pygame
import sys
from number_text_field import number_text_field
from values_text_flied import values_text_field
from button import Button
from binary_tree import Node

pygame.init()
screen = pygame.display.set_mode((1000,600))
width = screen.get_width()
height = screen.get_height()
font = pygame.font.SysFont("Helvetica",30)
small_font = pygame.font.SysFont("Helvetica",22)

label_node_ammount = small_font.render("Ingrese numero de nodos:",True,(50,50,50))
label_node_values = small_font.render("Ingrese valores de nodos:",True,(50,50,50))


node_ammount_textfield = number_text_field((725,150),font)
node_values_textfield = values_text_field((725,325),font)

generate_tree_button = Button((725,450),small_font)

binary_tree = Node(0, font)

print(binary_tree.right)
draggingMouse = False
dragmousepos = [0,0]
run = True
while run:
    mouse_pos = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            pygame.display.quit()
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            node_ammount_textfield.toggle_selected(mouse_pos)
            node_values_textfield.toggle_selected(mouse_pos)
            
            if generate_tree_button.is_click(mouse_pos):
                binary_tree.resetTree()
                listofvalues=[]
                number=""
                for x in node_values_textfield.text:
                    
                    if x != ',':
                        number+=x
                    else:
                        listofvalues.append(int(number))
                        number=""
                listofvalues.append(int(number))
                print(listofvalues)
                if int(node_ammount_textfield.text) == len(listofvalues):
                    for x in listofvalues:
                        binary_tree.insert(int(x))
                        


            draggingMouse = True
            currentmousepos = mouse_pos
        if event.type == pygame.MOUSEBUTTONUP:
            draggingMouse = False
        if event.type == pygame.KEYDOWN:
            character = event.unicode
            if character.isnumeric():
                node_ammount_textfield.write_char(character)
                node_values_textfield.write_char(character)
            if character == ',' or character == '-':
                node_values_textfield.write_char(character)
            if character == '\b':
                node_values_textfield.delete_char()
    if draggingMouse:
        dragmousepos[0] = mouse_pos[0]-currentmousepos[0]
        dragmousepos[1] =mouse_pos[1]-currentmousepos[1]
    screen.fill((255,255,255))
    binary_tree.initialTraversal([350+dragmousepos[0],100+dragmousepos[1]],screen)
    pygame.draw.rect(screen,(200,200,200),pygame.Rect(700,0,300,600))
    node_ammount_textfield.draw(screen)
    node_values_textfield.draw(screen)
    generate_tree_button.draw(screen)
    screen.blit(label_node_ammount,(725,100))
    screen.blit(label_node_values,(725,275))
    
    pygame.display.update()