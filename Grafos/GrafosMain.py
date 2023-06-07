#pip install --upgrade pygame
from io import BytesIO
import json
import random
import requests
import urllib.parse
import pygame
import networkx as nx
import matplotlib.pyplot as plt
from faker import Faker
from button import Button
from randombutton import randombutton
from PIL import Image
import os.path

fake = Faker()

# Configuración de la ventana
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 600
BACKGROUND_COLOR = (255, 255, 255)

def generate_profile_image_url(name):
    # Generar una URL de imagen de perfil falsa con un avatar generado
    style = random.choice(["female", "male"])
    encoded_name = urllib.parse.quote(name)
    url = f"https://avatars.dicebear.com/api/{style}/{encoded_name}.png"
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Error al generar la imagen de perfil: {response.status_code}")
    content_type = response.headers.get("content-type")
    if "image" not in content_type:
        raise Exception("La respuesta no es una imagen válida.")
    return url

def generate_fake_data(num_users):
    users = []
    relationships = {}

    for i in range(num_users):
        try:
            name = fake.name()
            cities = [("Manizales",0),("Bogota",5),("Cali",3),("Medellin",4),("Pereira",1)]
            city = random.choice(cities)
            profile_image_url = generate_profile_image_url(name)
            position = random.randint(0,1000000)
            randi= random.randint(1,4)
            color = (random.randint(100,200),random.randint(100,200),random.randint(100,200))
            
            
            user = {
                "id": i + 1,
                "name": name,
                "email": f"{name}@example.com",
                "birthdate": "1990-01-01",
                "profile_image_url": profile_image_url,
                "city": city,
                "liked_photos": [],
                "family": [],
                "communities": [],
                "position": position,
                "color": color
            }
            users.append(user)
            comunidades = ["Artistas","Tejedores","Comida","Belleza","Deporte","Juegos","Videos"]
            user["communities"].extend(random.sample(comunidades,randi))
            if i > 4:
                num_family_members = random.randint(0,4)
            elif i == 0:
                num_family_members=0
            else:
                num_family_members = random.randint(0,i)
            family_membersa = random.sample(users, num_family_members)
            family_members =[]
            for j in family_membersa:
                if j not in family_members:
                    family_members.append(j)
            options = ["Father","Mother","Sibling"]                   
            for family_member in family_members:
                if family_member["name"] != user["name"]:
                    choice = random.choice(options)
                    if choice == "Father" or choice == "Mother":
                        options.remove(choice)
                        reverserelation = {
                            "name": user["name"],
                            "relation": "Son"
                        }
                        family_member["family"].append(reverserelation)
                    if choice == "Sibling":
                        reverserelation = {
                            "name": user["name"],
                            "relation": "Sibling"
                        }
                        family_member["family"].append(reverserelation)
                    member = {
                        "name": family_member["name"],
                        "relation": choice
                    }
                else:
                    member = None
                if member is not None:
                    user["family"].append(member)
        except Exception as e:
            print(f"Error al generar el usuario {i + 1}: {e}")

    graph = nx.DiGraph()

    for user in users: 
        graph.add_node(user["id"], data=user)

    for user in users:
        num_friends = random.randint(2, 10)
        friends = random.sample(users, num_friends)

        for i in range(0,len(friends)):
            if friends[i]["name"] == user["name"]:
                friends.pop(i)
                break
        relationship_ids = [friend["id"] for friend in friends]
        relationships[user["id"]] = relationship_ids
        for friend in friends:
            graph.add_edge(user["id"], friend["id"])

    data = {
        "users": users,
        "relationships": relationships
    }

    return data, graph

def write_json_file(data, filename):
    with open(filename, "w") as file:
        json.dump(data, file, indent=2)

    print(f"El archivo {filename} ha sido creado exitosamente.")

def read_facebook_data(filename):
    with open(filename, "r") as file:
        data = json.load(file)

        # Leer usuarios
        print("Usuarios:")
        for user in data["users"]:
            print("ID:", user["id"])
            print("Nombre:", user["name"])
            print("Email:", user)
            print("Fecha de nacimiento:", user["birthdate"])
            print("URL de imagen de perfil:", user["profile_image_url"])
            print("Miembros de la familia:")
            for family_member in user["family"]:
                print("Nombre:", family_member["name"])
                print("Relación:", family_member["relation"])
            print("------------------------")

        # Leer relaciones de amistad
        print("Relaciones de amistad:")
        for user_id, friends in data["relationships"].items():
            print("ID de usuario:", user_id)
            print("Amigos:", friends)
            print("------------------------")

def load_profile_images(users):
    for user in users:
        try:
            response = requests.get(user["profile_image_url"])
            if response.status_code == 200:
                image_data = response.content
                image = Image.open(BytesIO(image_data))
                image = image.resize((80, 80))  # Ajusta el tamaño de la imagen si es necesario
                image = pygame.image.fromstring(image.tobytes(), image.size, image.mode)
                user["profile_image"] = image
        except Exception as e:
            print(f"Error al cargar la imagen de perfil para el usuario {user['id']}: {e}")


def generate_random_seeded_coords(seed):
    random.seed(seed)
    posx = random.randint(0,700)
    random.seed(seed+1)
    posy = random.randint(0,600)
    return (posx,posy)



def draw_network(user, relationships,dragmousepos,font, amigo, listoffriends, opcion,seed,users):
    # Calcular las coordenadas de los nodos
    node_radius = 50
    
    empiezox= 350
    empiezoy = 300
    if opcion == 1:
        
        for x in listoffriends:
            cords = generate_random_seeded_coords(seed)
            pygame.draw.line(window,(0,0,0),(empiezox+dragmousepos[0],empiezoy+dragmousepos[1]),(cords[0]+dragmousepos[0],cords[1]+dragmousepos[1]))
            pygame.draw.circle(window, x.get("color"), (cords[0]+dragmousepos[0],cords[1]+dragmousepos[1]), node_radius)

            profile_image = x.get("profile_image")
            window.blit(profile_image, (cords[0]+dragmousepos[0]-40, cords[1]+dragmousepos[1]-45))
            label_name = font.render(x.get("name"),True,(30,30,30))
            window.blit(label_name,(cords[0]+dragmousepos[0]-70,cords[1]+dragmousepos[1]-70))
            seed +=1
    seed+=1
    if opcion == 2:
        listoffamily= []
        familia = user["family"]
        for x in users:
            for y in familia:
                if x["name"] == y["name"]:
                    listoffamily.append((x,y["relation"]))
        for x in listoffamily:
            relacion = x[1]
            x = x[0]
            cords = generate_random_seeded_coords(seed)
            pygame.draw.line(window,(0,0,0),(350+dragmousepos[0],300+dragmousepos[1]),(cords[0]+dragmousepos[0],cords[1]+dragmousepos[1]))
            pygame.draw.circle(window, x.get("color"), (cords[0]+dragmousepos[0],cords[1]+dragmousepos[1]), node_radius)

            profile_image = x.get("profile_image")
            window.blit(profile_image, (cords[0]+dragmousepos[0]-40, cords[1]+dragmousepos[1]-45))
            label_name = font.render(x.get("name"),True,(30,30,30))
            window.blit(label_name,(cords[0]+dragmousepos[0]-70,cords[1]+dragmousepos[1]-70))
            label_relation = font.render(relacion,True,(30,30,30))
            window.blit(label_relation,(cords[0]+dragmousepos[0]-35,cords[1]+dragmousepos[1]+60))
            seed +=1
    seed+=1 
    if opcion == 3:
        listofcomunities = user["communities"]
        r=100
        g=100
        b=100
        for x in listofcomunities:
            cords = generate_random_seeded_coords(seed)
            pygame.draw.line(window,(0,0,0),(350+dragmousepos[0],300+dragmousepos[1]),(cords[0]+dragmousepos[0],cords[1]+dragmousepos[1]))
            pygame.draw.circle(window, (r,g,b), (cords[0]+dragmousepos[0],cords[1]+dragmousepos[1]), node_radius)
            label_name = font.render(x,True,(30,30,30))
            window.blit(label_name,(cords[0]+dragmousepos[0]-30,cords[1]+dragmousepos[1]-20))
            r+=20
            g+=20
            b+=20
            seed +=1

    seed+=1 
    if opcion == 4:
        listofcomunities = user["communities"]
        listoffriendcomunities = amigo["communities"]
        listadeambos = list(set(listofcomunities).intersection(listoffriendcomunities))
        r=100
        g=100
        b=100
        for x in listadeambos:
            cords = generate_random_seeded_coords(seed)
            pygame.draw.line(window,(0,0,0),(empiezox+dragmousepos[0],empiezoy-100+dragmousepos[1]),(cords[0]+dragmousepos[0],cords[1]+dragmousepos[1]))
            pygame.draw.line(window,(0,0,0),(empiezox+dragmousepos[0],empiezoy+100+dragmousepos[1]),(cords[0]+dragmousepos[0],cords[1]+dragmousepos[1]))
            pygame.draw.circle(window, (r,g,b), (cords[0]+dragmousepos[0],cords[1]+dragmousepos[1]), node_radius)
            label_name = font.render(x,True,(30,30,30))
            window.blit(label_name,(cords[0]+dragmousepos[0]-30,cords[1]+dragmousepos[1]-20))
            r+=20
            g+=20
            b+=20
            seed +=1
        
        pygame.draw.circle(window, amigo.get("color"), (empiezox+dragmousepos[0],empiezoy+100+dragmousepos[1]), node_radius)
        profile_image = amigo.get("profile_image")
        window.blit(profile_image, (empiezox -40+dragmousepos[0],empiezoy-45+100+dragmousepos[1]))
        label_name = font.render(amigo.get("name"),True,(30,30,30))
        window.blit(label_name,(empiezox-70+dragmousepos[0],empiezoy-70+100+dragmousepos[1]))
        empiezoy-=100
    seed+=1 
    if opcion == 5:

        idListOffriends = relationships[str(amigo["id"])]
        realListOfFriends= []
        listadeambos=[]
        for x in users:
            if x["id"] in idListOffriends:
                realListOfFriends.append(x)
        for x in listoffriends:
            for y in realListOfFriends:
                if x["name"] == y["name"]:
                    listadeambos.append(x)
        r=100
        g=100
        b=100
        for x in listadeambos:
            cords = generate_random_seeded_coords(seed)
            pygame.draw.line(window,(0,0,0),(empiezox+dragmousepos[0],empiezoy-100+dragmousepos[1]),(cords[0]+dragmousepos[0],cords[1]+dragmousepos[1]))
            pygame.draw.line(window,(0,0,0),(empiezox+dragmousepos[0],empiezoy+100+dragmousepos[1]),(cords[0]+dragmousepos[0],cords[1]+dragmousepos[1]))
            pygame.draw.circle(window, x.get("color"), (cords[0]+dragmousepos[0],cords[1]+dragmousepos[1]), node_radius)
            profile_image = x.get("profile_image")
            window.blit(profile_image, (cords[0]+dragmousepos[0]-40, cords[1]+dragmousepos[1]-45))
            label_name = font.render(x.get("name"),True,(30,30,30))
            window.blit(label_name,(cords[0]+dragmousepos[0]-70,cords[1]+dragmousepos[1]-70))
            r+=20
            g+=20
            b+=20
            seed +=1
        
        pygame.draw.circle(window, amigo.get("color"), (empiezox+dragmousepos[0],empiezoy+100+dragmousepos[1]), node_radius)
        profile_image = amigo.get("profile_image")
        window.blit(profile_image, (empiezox -40+dragmousepos[0],empiezoy-45+100+dragmousepos[1]))
        label_name = font.render(amigo.get("name"),True,(30,30,30))
        window.blit(label_name,(empiezox-70+dragmousepos[0],empiezoy-70+100+dragmousepos[1]))
        empiezoy-=100
    if opcion == 6:
        for x in listoffriends:
            if x["city"][0] == user["city"][0]:
                cords = generate_random_seeded_coords(seed)
                pygame.draw.line(window,(0,0,0),(empiezox+dragmousepos[0],empiezoy+dragmousepos[1]),(cords[0]+dragmousepos[0],cords[1]+dragmousepos[1]))
                pygame.draw.circle(window, x.get("color"), (cords[0]+dragmousepos[0],cords[1]+dragmousepos[1]), node_radius)

                profile_image = x.get("profile_image")
                window.blit(profile_image, (cords[0]+dragmousepos[0]-40, cords[1]+dragmousepos[1]-45))
                label_name = font.render(x.get("name"),True,(30,30,30))
                window.blit(label_name,(cords[0]+dragmousepos[0]-40,cords[1]+dragmousepos[1]-70))
                label_city = font.render(user["city"][0],True,(30,30,30))
                window.blit(label_city,(cords[0]+dragmousepos[0]-35,cords[1]+dragmousepos[1]+65))
                window.blit(label_city,(empiezox-40+dragmousepos[0],empiezoy+65+dragmousepos[1]))
                seed +=1
    if opcion == 7:
        mayor = 0
        curentuser=None
        for x in listoffriends:
            if (abs(int(x["city"][1]) - int(user["city"][1])) > mayor):
                mayor =abs(int(x["city"][1]) - int(user["city"][1])) 
                curentuser=x

        cords = generate_random_seeded_coords(seed)
        pygame.draw.line(window,(0,0,0),(empiezox+dragmousepos[0],empiezoy+dragmousepos[1]),(cords[0]+dragmousepos[0],cords[1]+dragmousepos[1]))
        pygame.draw.circle(window, curentuser.get("color"), (cords[0]+dragmousepos[0],cords[1]+dragmousepos[1]), node_radius)

        profile_image = curentuser.get("profile_image")
        window.blit(profile_image, (cords[0]+dragmousepos[0]-40, cords[1]+dragmousepos[1]-45))
        label_name = font.render(curentuser.get("name"),True,(30,30,30))
        window.blit(label_name,(cords[0]+dragmousepos[0]-40,cords[1]+dragmousepos[1]-70))
        label_city = font.render(user["city"][0],True,(30,30,30))
        label_amigo_city = font.render(curentuser["city"][0],True,(30,30,30))
        window.blit(label_amigo_city,(cords[0]+dragmousepos[0]-35,cords[1]+dragmousepos[1]+65))
        window.blit(label_city,(empiezox-40+dragmousepos[0],empiezoy+65+dragmousepos[1]))
        seed +=1
    pygame.draw.circle(window, user.get("color"), (empiezox+dragmousepos[0],empiezoy+dragmousepos[1]), node_radius)
    profile_image = user.get("profile_image")
    window.blit(profile_image, (empiezox -40+dragmousepos[0],empiezoy-45+dragmousepos[1]))
    label_name = font.render(user.get("name"),True,(30,30,30))
    window.blit(label_name,(empiezox-70+dragmousepos[0],empiezoy-70+dragmousepos[1]))
def main():
    # Verificar si el archivo JSON ya existe
    filename = "facebook_data.json"
    if os.path.isfile(filename):
        # El archivo existe, leer y cargar los datos
        with open(filename, "r") as file:
            data = json.load(file)
            users = data["users"]
            relationships = data["relationships"]
            load_profile_images(users)
    else:
        # El archivo no existe, generar datos falsos y escribir el archivo JSON
        data, graph = generate_fake_data(30)
        write_json_file(data, filename)
        users = data["users"]
        relationships = data["relationships"]
        load_profile_images(users)

    draggingMouse = False
    dragmousepos = [0,0]
    owofont = pygame.font.SysFont("Helvetica",24)
    small_font = pygame.font.SysFont("Helvetica",22)
    contador_usuario_actual = 0
    currentUser = users[contador_usuario_actual]
    idListOffriends = relationships[str(currentUser["id"])]
    realListOfFriends= []
    
    seed = 0
    for user in users:
        if user["id"] in idListOffriends:
            realListOfFriends.append(user)

    currentFriend = random.choice(realListOfFriends)

    
    label_name = small_font.render(currentUser.get("name"),True,(50,50,50))
    label_usuario_actual = owofont.render("Usuario seleccionado",True,(0,0,0))
    label_selecion_grafo = owofont.render("Seleccion de grafos:",True,(0,0,0))
    label_amigo_actual = owofont.render("Amigo seleccionado:",True,(0,0,0))
    label_friend_name = small_font.render(currentFriend.get("name"),True,(50,50,50))


    btn_red_amigos = Button((725,150),small_font,"Red de amigos")
    btn_red_familia = Button((725,200),small_font,"Red de familia")
    btn_red_coom = Button((725,250),small_font,"Red Comunidades")
    btn_red_coomfriend = Button((725,380),small_font,"Comunidades con amigo")
    btn_red_amigos_comun = Button((725,430),small_font,"Amigos en comun")
    btn_red_amigos_ciudad = Button((725,480),small_font,"Amigos misma ciudad")
    btn_red_amigo_lejano = Button((725,530),small_font,"Amigo mas lejano")

    btn_ramdo_user = randombutton((745,75))
    btn_ramdo_friend = randombutton((745,355))
    btn_rando_seed = randombutton((40,40))
    
    selected_option = 1
    while True:
        random.seed()
        # Manejar eventos
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                draggingMouse = True
                currentmousepos = mouse_pos

                if btn_ramdo_user.is_click(mouse_pos):
                    contador_usuario_actual +=1
                    if contador_usuario_actual == 29:
                        contador_usuario_actual=0
                    currentUser = users[contador_usuario_actual]
                    idListOffriends = relationships[str(currentUser["id"])]
                    realListOfFriends= []
                    for user in users:
                        if user["id"] in idListOffriends:
                            realListOfFriends.append(user)

                    currentFriend = random.choice(realListOfFriends)
                    label_name = small_font.render(currentUser.get("name"),True,(50,50,50))
                    label_friend_name = small_font.render(currentFriend.get("name"),True,(50,50,50))
                if btn_rando_seed.is_click(mouse_pos):
                    seed = random.randint(0,1000)

                if btn_red_amigos.is_click(mouse_pos):
                    selected_option = 1
                if btn_red_familia.is_click(mouse_pos):
                    selected_option = 2
                if btn_red_coom.is_click(mouse_pos):
                    selected_option = 3
                if btn_red_coomfriend.is_click(mouse_pos):
                    selected_option = 4
                if btn_red_amigos_comun.is_click(mouse_pos):
                    selected_option = 5
                if btn_red_amigos_ciudad.is_click(mouse_pos):
                    selected_option = 6
                if btn_red_amigo_lejano.is_click(mouse_pos):
                    selected_option = 7

                
                if btn_ramdo_friend.is_click(mouse_pos):
                    idListOffriends = relationships[str(currentUser["id"])]
                    realListOfFriends= []
                    for user in users:
                        if user["id"] in idListOffriends:
                            realListOfFriends.append(user)

                    currentFriend = random.choice(realListOfFriends)
                    label_friend_name = small_font.render(currentFriend.get("name"),True,(50,50,50))
            if event.type == pygame.MOUSEBUTTONUP:
                draggingMouse = False
        if draggingMouse:
            dragmousepos[0] = mouse_pos[0]-currentmousepos[0]
            dragmousepos[1] =mouse_pos[1]-currentmousepos[1]
        # Actualizar la ventana
        window.fill(BACKGROUND_COLOR)
        draw_network(currentUser,relationships,dragmousepos,small_font,currentFriend,realListOfFriends,selected_option,seed,users)
        pygame.draw.rect(window,(200,200,200),pygame.Rect(700,0,300,600))
        pygame.draw.rect(window,(255,253,208),pygame.Rect(725,55,250,40))
        pygame.draw.rect(window,(255,253,208),pygame.Rect(725,335,250,40))
        window.blit(label_name,(765,62))
        window.blit(label_usuario_actual,(734,20))
        window.blit(label_selecion_grafo,(734,120))
        window.blit(label_amigo_actual,(734,300))
        window.blit(label_friend_name,(765,340))
        btn_red_amigos.draw(window)
        btn_red_familia.draw(window)
        btn_red_coom.draw(window)
        btn_red_coomfriend.draw(window)
        btn_red_amigos_comun.draw(window)
        btn_red_amigos_ciudad.draw(window)
        btn_red_amigo_lejano.draw(window)
        btn_ramdo_user.draw(window)
        btn_ramdo_friend.draw(window)
        btn_rando_seed.draw(window)
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    pygame.init()
    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Red de Usuarios de Facebook")
    clock = pygame.time.Clock()

    main()