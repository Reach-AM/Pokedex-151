import math
import numpy as np
import pandas as pd
import platform
import pygame
from pygame import mixer
import os
import tensorflow as tf
from tensorflow import keras

############################################################
###################### Setup General #######################
############################################################

if platform.system() == "Darwin":
  path = "assets/"
  toys_path = "toys/"
  sprites_path = "sprites/"
else:
  path = "assets\\"
  toys_path = "toys\\"
  sprites_path = "sprites\\"

############################################################
###################### Loading screen ######################
############################################################
x_width, y_width = 512, 808
pygame.init()
mixer.init()
load_screen = pygame.image.load(path + 'load.png')
icono = pygame.image.load(path + 'icon.png')
mixer.music.load(path + "song.mp3")
screen = pygame.display.set_mode((x_width, y_width))
screen.blit(load_screen, (0,0))
mixer.music.set_volume(0.05)
mixer.music.play(loops = -1)
pygame.display.set_icon(icono)
pygame.display.set_caption("Pokedex")
pygame.display.update()

############################################################
##################### Setup de la Red ######################
############################################################

img_height = 512
img_width = 512
class_names = ['Abra', 'Aerodactyl', 'Alakazam', 'Arbok', 'Arcanine', 'Articuno',
               'Beedrill', 'Bellsprout', 'Blastoise', 'Bulbasaur', 'Butterfree',
               'Caterpie', 'Chansey', 'Charizard', 'Charmander', 'Charmeleon',
               'Clefable', 'Clefairy', 'Cloyster', 'Cubone', 'Dewgong', 'Diglett',
               'Ditto', 'Dodrio', 'Doduo', 'Dragonair', 'Dragonite', 'Dratini',
               'Drowzee', 'Dugtrio', 'Eevee', 'Ekans', 'Electabuzz', 'Electrode',
               'Exeggcute', 'Exeggutor', 'Farfetchd', 'Fearow', 'Flareon', 'Gastly',
               'Gengar', 'Geodude', 'Gloom', 'Golbat', 'Goldeen', 'Golduck', 'Golem',
               'Graveler', 'Grimer', 'Growlithe', 'Gyarados', 'Haunter', 'Hitmonchan',
               'Hitmonlee', 'Horsea', 'Hypno', 'Ivysaur', 'Jigglypuff', 'Jolteon',
               'Jynx', 'Kabuto', 'Kabutops', 'Kadabra', 'Kakuna', 'Kangaskhan',
               'Kingler', 'Koffing', 'Krabby', 'Lapras', 'Lickitung', 'Machamp',
               'Machoke', 'Machop', 'Magikarp', 'Magmar', 'Magnemite', 'Magneton',
               'Mankey', 'Marowak', 'Meowth', 'Metapod', 'Mew', 'Mewtwo', 'Moltres',
               'MrMime', 'Muk', 'Nidoking', 'Nidoqueen', 'Nidorina', 'Nidorino',
               'Ninetales', 'Oddish', 'Omanyte', 'Omastar', 'Onix', 'Paras',
               'Parasect', 'Persian', 'Pidgeot', 'Pidgeotto', 'Pidgey', 'Pikachu',
               'Pinsir', 'Poliwag', 'Poliwhirl', 'Poliwrath', 'Ponyta', 'Porygon',
               'Primeape', 'Psyduck', 'Raichu', 'Rapidash', 'Raticate', 'Rattata',
               'Rhydon', 'Rhyhorn', 'Sandshrew', 'Sandslash', 'Scyther', 'Seadra',
               'Seaking', 'Seel', 'Shellder', 'Slowbro', 'Slowpoke', 'Snorlax',
               'Spearow', 'Squirtle', 'Starmie', 'Staryu', 'Tangela', 'Tauros',
               'Tentacool', 'Tentacruel', 'Vaporeon', 'Venomoth', 'Venonat',
               'Venusaur', 'Victreebel', 'Vileplume', 'Voltorb', 'Vulpix', 'Wartortle',
               'Weedle', 'Weepinbell', 'Weezing', 'Wigglytuff', 'Zapdos', 'Zubat']

############################################################
########################## Assets ##########################
############################################################

background = pygame.image.load(path + 'dex.png')
typo_title = pygame.image.load(path + 'typo1.png')
sound = pygame.image.load(path + 'sound.png')
Font=pygame.font.Font(path+'Pixel-Regular.ttf', 16)
FontS=pygame.font.Font(path+'Pixel-Regular.ttf', 10)

flavor = pd.read_csv(path + 'flavor.csv')

number_of_tests = 0
for base, dirs, files in os.walk(toys_path):
    for file in files:
      if(file != '.DS_Store'):
        number_of_tests  += 1

toys = []
for i in range(number_of_tests):
    toys.append(pygame.image.load(toys_path + str(i+1) + '.jpeg'))

############################################################
################### Setup de la Interfaz ###################
############################################################

margin =  13
sc_height = 11 + 105*(math.floor(len(toys)/4)) - 2 + 26
print("holaaaa")
print(sc_height)
print(len(toys))
img_act, prediccion = -1, ''
porcentaje = 0.0

############################################################
##################### Pequeños ajustes #####################
############################################################

def Background():
    screen.blit(background, (0,0))

############################################################
########################### Menu ###########################
############################################################

def MainMenu():
  global img_act
  soundon = True
  click, scroll_y  = False, 0
  while True:
    screen.fill((230, 230, 230))
    mouse_x, mouse_y = pygame.mouse.get_pos()
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        exit()
      if event.type == pygame.MOUSEBUTTONDOWN:
        if event.button == 1: click = True
        elif event.button == 4: scroll_y = max(scroll_y - 20, 0)
        elif event.button == 5: scroll_y = min(scroll_y + 20, sc_height - 324)

    Background()
    Imagenes_Prueba(click, mouse_x, mouse_y, scroll_y)
    soundon = TitleBar(click, mouse_x, mouse_y, soundon)
    if (img_act > -1):
      Resultado()

    click = False
    pygame.display.update()

def TitleBar(click, mouse_x, mouse_y, soundon):
    letter=Font.render("Gallery", False, (230,230,230),(20,20,20))
    w, h = Font.size("Gallery")
    pygame.draw.rect(screen, (20, 20, 20), (39, 443,434,27),border_radius =  4)
    pygame.draw.rect(screen, (20, 20, 20), (39, 448,434,22))
    sx = 444
    soundButton = pygame.Rect(sx, 444.5, 24, 24)
    pygame.draw.rect(screen, (20, 20, 20), soundButton)

    if soundButton.collidepoint((mouse_x, mouse_y)) and click:
        soundon = not soundon
    if soundon:
        screen.blit(sound, (sx,444.5), (0,0,24,24))
        mixer.music.set_volume(0.05)
    else:
        screen.blit(sound, (sx,444.5), (24,0,24,24))
        mixer.music.set_volume(0)
    screen.blit(letter, (44+424/2-w/2,445))
    return soundon


############################################################
################### Pantalla de Imagenes ###################
############################################################

def Imagenes_Prueba(click, mouse_x, mouse_y, scroll_y):
  global img_act, prediccion, porcentaje
  adjustment = 26
  options = pygame.surface.Surface((424, sc_height))
  options.fill((230, 230, 230))
  select = []
  for i in range(len(toys)):
      row = math.floor(i/4)
      column = i - 4 * row
      toy = pygame.transform.scale(toys[i], (92, 92))
      if column >= 2:
        select.append(pygame.Rect(margin - 4 + (92+margin) * column - 2, margin + (92+margin) * row - 3 + adjustment, 94, 94))
        options.blit(toy, (margin - 4 + (92+margin) * column - 1, margin + (92+margin) * row - 2 + adjustment))
        pygame.draw.rect(options, (0, 0, 0), select[i], 2, 2)
      else:
        select.append(pygame.Rect(margin - 4 + (92+margin) * column - 1, margin + (92+margin) * row - 3 + adjustment, 94, 94))
        options.blit(toy, (margin - 4 + (92+margin) * column, margin + (92+margin) * row - 2 + adjustment))
        pygame.draw.rect(options, (0, 0, 0), select[i], 2, 2)
  for i in range(len(select)):
    if select[i].collidepoint((mouse_x-44-1, mouse_y-444+scroll_y-1)):
      if click and img_act != i:
        img_act = i
        prediccion, porcentaje = Analizar(str(i+1) + '.jpeg')
  screen.blit(options, (44, 444), (0, scroll_y, 424, 324))

############################################################
####################### Uso de la Red ######################
############################################################

def Analizar(imagen):
    img = keras.preprocessing.image.load_img(toys_path+imagen, target_size=(img_height, img_width))
    img_array = keras.preprocessing.image.img_to_array(img)
    img_array = tf.expand_dims(img_array, 0) # Create a batch

    predictions = model.predict(img_array)
    score = tf.nn.softmax(predictions[0])

    return class_names[np.argmax(score)], 100 * np.max(score)

############################################################
##################### Mostrar Resultado ####################
############################################################

def Resultado():
    global img_act, prediccion, porcentaje
    border = pygame.Rect(16+40,64+40,244,244)
    toy = pygame.transform.scale(toys[img_act], (240, 240))
    screen.blit(toy, (16+40, 64+40))
    Name(prediccion)
    Number(porcentaje)
    Real(prediccion)
    pygame.draw.rect(screen, (0, 0, 0), border, 5, 2)

def Name(prediccion):
    for i in range(len(prediccion)):
        pos = ord(prediccion[i].lower()) - 97
        screen.blit(typo_title, (16+40+29*i, 16+40), (pos*32,0,32,32))

def Number(porcentaje):
    screen.blit(typo_title, (456-27, 16+40), (320,32,32,32))
    porcentaje = math.floor(porcentaje)
    unit = (porcentaje%10)
    decimal = math.floor(porcentaje/10)
    screen.blit(typo_title, (456-55, 16+40), (32*unit,32,32,32))
    screen.blit(typo_title, (456-83, 16+40), (32*decimal,32,32,32))

def Real(prediccion):
    dex = ['Bulbasaur', 'Ivysaur', 'Venusaur', 'Charmander', 'Charmeleon', 'Charizard',
           'Squirtle', 'Wartortle', 'Blastoise', 'Caterpie', 'Metapod', 'Butterfree',
           'Weedle', 'Kakuna', 'Beedrill', 'Pidgey', 'Pidgeotto', 'Pidgeot',
           'Rattata', 'Raticate', 'Spearow', 'Fearow', 'Ekans', 'Arbok',
           'Pikachu', 'Raichu', 'Sandshrew', 'Sandslash', 'Nidoran', 'Nidorina', 'Nidoqueen',
           'Nidoran', 'Nidorino', 'Nidoking', 'Clefairy', 'Clefable',
           'Vulpix', 'Ninetales', 'Jigglypuff', 'Wigglytuff', 'Zubat', 'Golbat',
           'Oddish', 'Gloom', 'Vileplume', 'Paras', 'Parasect',
           'Venonat', 'Venomoth','Diglett', 'Dugtrio', 'Meowth', 'Persian',
           'Psyduck', 'Golduck', 'Mankey', 'Primeape', 'Growlithe', 'Arcanine',
           'Poliwag', 'Poliwhirl', 'Poliwrath', 'Abra', 'Kadabra', 'Alakazam',
           'Machop', 'Machoke',  'Machamp', 'Bellsprout', 'Weepinbell', 'Victreebel',
           'Tentacool', 'Tentacruel', 'Geodude', 'Graveler', 'Golem',
           'Ponyta', 'Rapidash', 'Slowpoke', 'Slowbro', 'Magnemite', 'Magneton', 'Farfetchd',
           'Doduo', 'Dodrio', 'Seel', 'Dewgong', 'Grimer', 'Muk',
           'Shellder', 'Cloyster', 'Gastly', 'Haunter', 'Gengar', 'Onix',
           'Drowzee', 'Hypno', 'Krabby', 'Kingler', 'Voltorb', 'Electrode',
           'Exeggcute', 'Exeggutor', 'Cubone', 'Marowak', 'Hitmonlee', 'Hitmonchan',
           'Lickitung', 'Koffing', 'Weezing', 'Rhyhorn', 'Rhydon', 'Chansey',
           'Tangela', 'Kangaskhan', 'Horsea', 'Seadra', 'Goldeen', 'Seaking',
           'Staryu', 'Starmie', 'MrMime', 'Scyther', 'Jynx', 'Electabuzz',
           'Magmar', 'Pinsir', 'Tauros', 'Magikarp', 'Gyarados', 'Lapras',
           'Ditto', 'Eevee', 'Vaporeon', 'Jolteon', 'Flareon', 'Porygon',
           'Omanyte', 'Omastar', 'Kabuto', 'Kabutops', 'Aerodactyl', 'Snorlax',
           'Articuno', 'Zapdos', 'Moltres', 'Dratini', 'Dragonair', 'Dragonite',
           'Mewtwo', 'Mew']
    num = dex.index(prediccion) + 1
    sprite = pygame.image.load(sprites_path + str(num) + '.png')
    sprite = pygame.transform.scale(sprite, (128, 128))
    Flavor(num-1)
    screen.blit(sprite, (330, 40 + 70))

def Flavor(num):
    txt = flavor.iloc[num]['flavor_text']
    txt = txt.replace("\n"," ")
    txt = txt.replace("\x0c"," ")
    txt = txt.split(" ")
    sentence = []
    act = '\"'
    for i in range(len(txt)):
        w, h = FontS.size(act + txt[i] + ' ')
        if(w <= 158):
            act = act + ' ' + txt[i]
        else:
            sentence.append(act)
            act = txt[i]
    sentence.append(act+'\"')
    for i in range(len(sentence)):
        text = FontS.render(sentence[i], False, (20,20,20),(230,230,230))
        w, h = FontS.size(sentence[i])
        screen.blit(text, (387 - w/2, 254 + i*16))

############################################################
########################### Fin ############################
############################################################

model = keras.models.load_model('Modelo')
MainMenu()
