#!/usr/bin/env python3
import pygame
from pygame.locals import *
from src.main import game
import webbrowser

# inicializando pygame
pygame.init()

# tamanho da janela
width, height = (1000, 600)
window = pygame.display.set_mode((width, height))

# configurações da janela
pygame.display.set_caption('Lyria - Global Game Jam 2020')
pygame.display.set_icon(pygame.image.load('src/img/egua.png'))
run = True


def ui_plate():
    global uiW, uiH, uiX, uiY
    if height > width*0.5296:
        uiW = int(width)
        uiH = int(uiW*0.5296)
    else:
        uiH = int(height)
        uiW = int(uiH/0.5296)
    uiX = int((width - uiW)/2)
    uiY = int((height - uiH)/2)


# botões
class button:
    def __init__(self, action, actionParam, buttonPic, x, y, w, h):
        self.action = action
        self.actionParam = actionParam

        self.bx = int(uiX + (x * uiW))
        self.by = int(uiY + (y * uiH))
        self.bw = int(w * uiW)
        self.bh = int(h * uiH)

        self.buttonPic = pygame.transform.scale(buttonPic, (self.bw, self.bh))

        self.over = pygame.Surface((self.bw, self.bh))
        self.over.fill((0,0,0))

    def draw_button(self):
        if window.blit(self.buttonPic, (self.bx, self.by)).collidepoint(mouse):
            self.over.set_alpha(50)
            if click[0]:
                self.over.set_alpha(100)
        else: self.over.set_alpha(0)
        window.blit(self.buttonPic, (self.bx, self.by))
        window.blit(self.over, (self.bx, self.by))

    def click_button(self):
        if window.blit(self.buttonPic, (self.bx, self.by)).collidepoint(mouse):
            self.action(self.actionParam)


# ações botão
def open_github(link):
    webbrowser.open(link)

# musica infinita do jogo
pygame.mixer.music.load('src/sound/menu.mp3')
pygame.mixer.music.play(-1)

# menu
def main_menu():
    global button_list

    backGround_image = pygame.image.load('src/img/bg.png')
    backGround = pygame.transform.scale(backGround_image, (width, height))
    btn_play = pygame.image.load('src/img/play.png')
    btn_credits = pygame.image.load('src/img/credits.png')

    button_list = [
    button(game, 'game', btn_play, .1, .3, .1, .1),
    button(open_github, 'https://github.com/lucaspompeun/lyria', btn_credits, .1, .5, .1, .1)
]
    window.blit(backGround, (0, 0))
    for b in button_list:
        b.draw_button()

def main_loop():
    global run, width, height, mouse, click
    ui_plate()
    backGround = 0

    while run:
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        current_screen()
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.VIDEORESIZE:
                window = pygame.display.set_mode ( (event.w, event.h) )
                width, height = event.w, event.h
                ui_plate()
            if event.type == pygame.MOUSEBUTTONUP:
                for b in button_list:
                    b.click_button()

        pygame.display.update()



# chamada do jogo
current_screen = main_menu
main_loop()

pygame.quit()