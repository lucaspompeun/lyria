#!/usr/bin/env python3
import pygame
from pygame.locals import *
import random
import sys


def game(start):
    # fps do jogo
    fps_clock = pygame.time.Clock()

    # pixels por quadrado
    tilesize = 40

    # numero de quadrados na tela
    width = 30
    height = 15

    # configurações do inventário
    height_inventory = 2*tilesize
    padding = tilesize/2

    # constante de cores
    black = (0, 0, 0)
    white = (255, 255, 255)

    # objetos

    ground = 0
    grass = 1
    house = 2
    castle_1 = 3
    castle_2 = 4
    trees = 5
    cloud = 11

    # lista de recursos
    resources = [ground, grass, house, castle_1, castle_2, trees]

    # dicionário dos assets
    textures = {
        ground: pygame.image.load('src/img/ground.png'),
        grass: pygame.image.load('src/img/grass.png'),
        house: pygame.image.load('src/img/house.png'),
        castle_1: pygame.image.load('src/img/castle_1.png'),
        castle_2: pygame.image.load('src/img/castle_2.png'),
        trees: pygame.image.load('src/img/trees.png'),
        cloud: pygame.image.load('src/img/cloud.png')
    }

    # inventário inicial
    inventory = {
        ground: 0,
        grass: 0,
        house: 0,
        castle_1: 0,
        castle_2: 0,
        trees: 0,
    }

    # mapeamento das teclas
    controls = {
        ground: 49,         # tecla 1
        grass: 50,          # tecla 2
        house: 51,          # tecla 3
        castle_1: 52,       # tecla 4
        castle_2: 53,       # tecla 5
        trees: 54,          # tecla 6
    }

    # constantes de raridade
    base_rarity = 0
    very_common = 30
    common = 45
    rare = 50
    very_rare = 53
    ultra_rare = 54

    # inicializando pygame
    pygame.init()

    # criando interface gráfica
    graphic_display = pygame.display.set_mode(
        (width*tilesize, height*tilesize + height_inventory))

    # configurações da janela
    pygame.display.set_caption('Lyria - Global Game Jam 2020')
    pygame.display.set_icon(pygame.image.load('src/img/egua.png'))

    #musica infinita do jogo
    pygame.mixer.music.load('src/sound/game.mp3')
    pygame.mixer.music.play(-1)

    # geração do mapa com os quadrados randomicamente baseado na raridade
    tilemap = [[grass for i in range(width)] for j in range(height)]
    for row in range(height):
        for column in range(width):
            random_num = random.randint(base_rarity, ultra_rare)
            this_tile = grass

            if random_num < very_common:
                if (random_num % 3) == 0:
                    this_tile = castle_2
                else:
                    this_tile = grass

            elif random_num >= very_common and random_num < common:
                if (random_num % 2) == 0:
                    this_tile = castle_1
                else:
                    this_tile = trees

            elif random_num >= rare and random_num < very_rare:
                if (random_num % 2) == 0:
                    this_tile = house
                else:
                    this_tile = ground

            tilemap[row][column] = this_tile

    # fonte do inventário
    font_inventory = pygame.font.Font('src/font/freesansbold.ttf', 18)

    # jogador
    player = pygame.image.load('src/img/geraldo.gif')

    # posição randômica do geraldo
    player_position = [random.randint(
        0, width - 1), random.randint(0, height - 1)]

    # posição nuvem
    cloud_x_position = [-200, -500, -1000]
    cloud_y_position = [random.randint(0, height*tilesize - 1), random.randint(
        0, height*tilesize - 1), random.randint(0, height*tilesize - 1)]

    # loop do jogo
    while True:
        # limpando a tela
        graphic_display.fill(black)

        # ações ao receber eventos do usuário
        for event in pygame.event.get():
            # saindo do jogo
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            # usando setas
            elif event.type == KEYDOWN:

                # seta direita
                if (event.key == K_RIGHT) and (player_position[0] < width - 1):
                    player_position[0] += 1

                # seta esquerda
                elif (event.key == K_LEFT) and (player_position[0] > 0):
                    player_position[0] -= 1

                # seta cima
                elif (event.key == K_UP) and (player_position[1] > 0):
                    player_position[1] -= 1

                # seta baixo
                elif (event.key == K_DOWN) and (player_position[1] < height - 1):
                    player_position[1] += 1

                # tecla espaço
                elif (event.key == K_SPACE):
                    this_tile = tilemap[player_position[1]][player_position[0]]
                    inventory[this_tile] += 1
                    tilemap[player_position[1]][player_position[0]] = ground

                # usando recursos do inventário
                for key in controls:
                    if (event.key == controls[key]) and (inventory[key] > 0):
                        standing_tile = tilemap[player_position[1]
                                                ][player_position[0]]
                        inventory[standing_tile] += 1
                        inventory[key] -= 1
                        tilemap[player_position[1]][player_position[0]] = key

        # mostrando mapa atualizado após ações do usuário
        for row in range(height):
            for column in range(width):
                graphic_display.blit(
                    textures[tilemap[row][column]], (column*tilesize, row*tilesize))

        # configurações do inventário
        inventory_x_position = padding
        inventory_y_position = height*tilesize + padding

        for item in resources:
            graphic_display.blit(
                textures[item], (inventory_x_position, inventory_y_position))

            inventory_x_position += padding

            numInventoryText = font_inventory.render(
                str(inventory[item]), True, white, black)

            graphic_display.blit(
                numInventoryText, (inventory_x_position, inventory_y_position))

            inventory_x_position += padding*2

        # mostrando jogador graficamente
        graphic_display.blit(
            player, (player_position[0]*tilesize, player_position[1]*tilesize))

        # configurações da nuvem
        for each in range(len(cloud_x_position)):
            graphic_display.blit(
                textures[cloud], (cloud_x_position[each], cloud_y_position[each]))
            cloud_x_position[each] += 1

            if cloud_x_position[each] > width*tilesize:
                cloud_x_position[each] = -random.randint(0, 450)
                cloud_y_position[each] = random.randint(0, height*tilesize - 1)

        # atualizando tela a cada 24 ticks
        pygame.display.update()
        fps_clock.tick(60)
