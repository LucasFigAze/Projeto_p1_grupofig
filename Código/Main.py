import pygame
from pygame.locals import *
from sys import exit
from random import randint
cont = 0
pygame.init()
musica_de_fundo = pygame.mixer.music.load('Daniel Birch - Dancing With Fire.mp3')
pygame.mixer.music.play(-1)

barulho_colisao = pygame.mixer.Sound('mario_moeda_efeito_sonoro_toquesengracadosmp3.com.mp3')

largura = 700
altura = 700
x = largura/2
y = altura/2

# texto em arial, tamanho 40, negrito true e itálico true
fonte = pygame.font.SysFont('arial', 40, True, True)

# posição random bloco verde
x_verde = randint(10,600)
y_verde = randint(20,500)

# posição random bloco azul
x_azul = randint(30, 400)
y_azul = randint(40, 300)

# posição random bloco vermelho
x_vermelho = randint(50, 400)
y_vermelho = randint(60, 300)

tela_jogo = pygame.display.set_mode((largura,altura))
pygame.display.set_caption('Segurança de bar')

pontos_verde = 0
pontos_azul = 0
pontos_vermelho = 0

#criando o loop principal
while True:
    tela_jogo.fill((0,0,0))
    texto = f'Verde: {pontos_verde}'
    texto_2 = f'Azul: {pontos_azul}'
    texto_3 = f'Vermelho: {pontos_vermelho}'
    texto_formatado = fonte.render(texto, True, (255, 255, 255))
    texto_formatado_2 = fonte.render(texto_2, True, (255, 255, 255))
    texto_formatado_3 = fonte.render(texto_3, True, (255, 255, 255))
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        '''if event.type == KEYDOWN:
            if event.key == K_a:
                x = x-15
            if event.key == K_d:
                x = x+15
            if event.key == K_w:
                y = y-15
            if event.key == K_s:
                y = y+15'''
        if pygame.key.get_pressed()[K_a]:
            x = x - 15
        if pygame.key.get_pressed()[K_d]:
            x = x + 15
        if pygame.key.get_pressed()[K_w]:
            y = y - 15
        if pygame.key.get_pressed()[K_s]:
            y = y + 15

    bloco_vermelho = pygame.draw.rect(tela_jogo,(200,0,0),(x_vermelho,y_vermelho,100,100))
    bloco_azul = pygame.draw.rect(tela_jogo, (0, 0, 200), (x_azul, y_azul, 100, 100))
    bloco_verde = pygame.draw.rect(tela_jogo,(0,200,0),(x_verde,y_verde,100,100))
    circulo_cinza = pygame.draw.circle(tela_jogo, (100, 100, 100), (x, y), 50)
    if circulo_cinza.colliderect(bloco_verde):
        x_verde = randint(10,600)
        y_verde = randint(20,500)
        pontos_verde += 1
        barulho_colisao.play()
    if circulo_cinza.colliderect(bloco_azul):
        x_azul = randint(30, 400)
        y_azul = randint(40, 300)
        pontos_azul += 1
        barulho_colisao.play()
    if circulo_cinza.colliderect(bloco_vermelho):
        x_vermelho = randint(50, 400)
        y_vermelho = randint(60, 300)
        pontos_vermelho += 1
        barulho_colisao.play()

    tela_jogo.blit(texto_formatado, (400, 40))
    tela_jogo.blit(texto_formatado_2, (400, 0))
    tela_jogo.blit(texto_formatado_3, (400, 80))
    pygame.display.update()