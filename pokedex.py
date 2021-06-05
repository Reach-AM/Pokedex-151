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
pygame.display.set_caption("Pokédex")
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

############################################################
########################## Assets ##########################
############################################################

background = pygame.image.load(path + 'dex.png')
icons = pygame.image.load(path + 'icons.png')
Font=pygame.font.Font(path+'Pixel-Regular.ttf', 16)
FontS=pygame.font.Font(path+'Pixel-Regular.ttf', 10)
FontT=pygame.font.Font(path+'Pixel-Title.ttf', 23)
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
gal_height = 11 + 105*(math.floor(len(toys)/4)) - 2 + 26
dex_height = 1900
soundon = True
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
def Menu():
  click = 0
  while True:
      screen.fill((230, 230, 230))
      mouse_x, mouse_y = pygame.mouse.get_pos()
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          pygame.quit()
          exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
          if event.button == 1: click = True

      MenuButtons(click, mouse_x, mouse_y)
      TitleBar(click, mouse_x, mouse_y, "Menu", False)

      click = False
      Background()
      pygame.display.update()

def MenuButtons(click, mouse_x, mouse_y):
    global img_act
    pokedex = pygame.Rect(52, 480, 64, 64)
    gallery = pygame.Rect(129, 480, 64, 64)
    pygame.draw.rect(screen, (163, 0, 41), pokedex, border_radius = 2)
    pygame.draw.rect(screen, (41, 41, 163), gallery, border_radius = 2)

    if click:
      if pokedex.collidepoint((mouse_x, mouse_y)):
        Pokedex()
        img_act = -1
      if gallery.collidepoint((mouse_x, mouse_y)):
        Gallery()
        img_act = -1


############################################################
########################## Pokédex #########################
############################################################

def Pokedex():
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
        elif event.button == 4: scroll_y = max(scroll_y - 35, 0)
        elif event.button == 5: scroll_y = min(scroll_y + 35, dex_height - 324)

    Imagenes_Dex(click, mouse_x, mouse_y, scroll_y)
    able = TitleBar(click, mouse_x, mouse_y, "Pokédex", True)
    if (img_act > -1):
      Entrada()

    click = False
    Background()
    if able: break
    pygame.display.update()


############################################################
#################### Galería de Imagenes ###################
############################################################

def Gallery():
  global img_act
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
        elif event.button == 5: scroll_y = min(scroll_y + 20, gal_height - 324)

    Imagenes_Prueba(click, mouse_x, mouse_y, scroll_y)
    able = TitleBar(click, mouse_x, mouse_y, "Gallery", True)
    if (img_act > -1):
      Resultado()

    click = False
    Background()
    if able: break
    pygame.display.update()

############################################################
################### Impresión del Títulos ##################
############################################################

def TitleBar(click, mouse_x, mouse_y, word, able):
    global soundon
    letter=Font.render(word, False, (230,230,230),(20,20,20))
    w, h = Font.size(word)
    pygame.draw.rect(screen, (20, 20, 20), (39, 443,434,27))
    sx,ex = 444, 44

    soundButton = pygame.Rect(sx, 444.5, 24, 24)
    pygame.draw.rect(screen, (20, 20, 20), soundButton)
    if able:
        backButton = pygame.Rect(ex, 444.5, 24, 24)
        pygame.draw.rect(screen, (20, 20, 20), backButton)
        screen.blit(icons, (ex,444.5), (48,0,24,24))

    if click:
        if able and backButton.collidepoint((mouse_x, mouse_y)):
            return True
        if soundButton.collidepoint((mouse_x, mouse_y)):
            soundon = not soundon
    if soundon:
        screen.blit(icons, (sx,444.5), (0,0,24,24))
        mixer.music.set_volume(0.05)
    else:
        screen.blit(icons, (sx,444.5), (24,0,24,24))
        mixer.music.set_volume(0)
    screen.blit(letter, (44+424/2-w/2,445))
    return False

def UpBar(num, prediccion, porcentaje, p):
    pygame.draw.rect(screen, (20, 20, 20), (40, 40, 432, 36))
    text = FontT.render(str(num) + '.' + prediccion, False, (230,230,230), (20,20,20))
    w, h = FontT.size(prediccion)
    screen.blit(text, (40+6, 40+8))
    if p:
        num = str(math.floor(porcentaje)) + '%'
        text = FontT.render(num, False, (230,230,230), (20,20,20))
        w, h = FontT.size(num)
        screen.blit(text, (472-8-w, 40+8))

############################################################
################### Imagenes de Pokedex ###################
############################################################

def Imagenes_Dex(click, mouse_x, mouse_y, scroll_y):
  global img_act
  options = pygame.surface.Surface((424, dex_height))
  options.fill((230, 230, 230))
  select = []
  for i in range(len(dex)):
    row = math.floor(i/6)
    column = i - 6 * row
    select.append(pygame.Rect((64+8)*column, 33 + (64+8)*row, 64, 64))
    sprite = pygame.image.load(sprites_path + str(i+1) + '.png')
    pygame.draw.rect(options, (20, 20, 20), select[i], 2, 2)
    options.blit(sprite, ((64+8)*column, 34 + (64+8)*row))

  for i in range(len(select)):
    if select[i].collidepoint((mouse_x-44-1, mouse_y-444+scroll_y-1)) and mouse_y-443-28 > 0:
      if click and img_act != i:
        img_act = i

  screen.blit(options, (44, 444), (0, scroll_y, 424, 324))

############################################################
###################### Mostrar Entrada #####################
############################################################

def Entrada():
  UpBar(img_act+1, dex[img_act], 0, False)
  sprite = pygame.image.load(sprites_path + str(img_act+1) + '.png')
  sprite = pygame.transform.scale(sprite, (128, 128))
  FlavorDex(img_act)
  pygame.draw.rect(screen, (20, 20, 20), (54,96,130,130), 4, 2)
  screen.blit(sprite, (56, 98))

def FlavorDex(num):
    txt = flavor.iloc[num]['flavor_text']
    txt = txt.replace("\n"," ")
    txt = txt.replace("\x0c"," ")
    txt = txt.split(" ")
    sentence = []
    act = '\"'
    for i in range(len(txt)):
        w, h = Font.size(act + txt[i] + ' ')
        if(w <= 270):
            act = act + ' ' + txt[i]
        else:
            sentence.append(act)
            act = txt[i]
    sentence.append(act+'\"')
    for i in range(len(sentence)):
        text = Font.render(sentence[i], False, (20,20,20),(230,230,230))
        w, h = Font.size(sentence[i])
        screen.blit(text, (330 - w/2, 156 - 21*len(sentence)/2 + i*21))

############################################################
################### Pantalla de Imagenes ###################
############################################################

def Imagenes_Prueba(click, mouse_x, mouse_y, scroll_y):
  global img_act, prediccion, porcentaje
  adjustment = 26
  options = pygame.surface.Surface((424, gal_height))
  options.fill((230, 230, 230))
  select = []
  for i in range(len(toys)):
      row = math.floor(i/4)
      column = i - 4 * row
      toy = pygame.transform.scale(toys[i], (92, 92))
      if column >= 2:
        select.append(pygame.Rect(margin - 4 + (92+margin) * column - 2, margin + (92+margin) * row - 3 + adjustment, 94, 94))
        options.blit(toy, (margin - 4 + (92+margin) * column - 1, margin + (92+margin) * row - 2 + adjustment))
        pygame.draw.rect(options, (20, 20, 20), select[i], 2, 2)
      else:
        select.append(pygame.Rect(margin - 4 + (92+margin) * column - 1, margin + (92+margin) * row - 3 + adjustment, 94, 94))
        options.blit(toy, (margin - 4 + (92+margin) * column, margin + (92+margin) * row - 2 + adjustment))
        pygame.draw.rect(options, (20, 20, 20), select[i], 2, 2)
  for i in range(len(select)):
    if select[i].collidepoint((mouse_x-44-1, mouse_y-444+scroll_y-1)) and mouse_y-443-28 > 0:
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
    #border = pygame.Rect(16+40,58+40,244,244)
    toy = pygame.transform.scale(toys[img_act], (240, 240))
    screen.blit(toy, (16+40, 58+40))
    num = dex.index(prediccion) + 1
    UpBar(num, prediccion, porcentaje, True)
    Real(num)
    pygame.draw.rect(screen, (20, 20, 20), (16+40,58+40,244,244), 5, 2)

def Real(num):
    sprite = pygame.image.load(sprites_path + str(num) + '.png')
    sprite = pygame.transform.scale(sprite, (128, 128))
    Flavor(num-1)
    screen.blit(sprite, (320, 104))

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
Menu()
