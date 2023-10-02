import pygame
from pygame.locals import *
from sys import exit
from random import randint

cont = 0
pygame.init()
pygame.mixer.init()

collision_sound = pygame.mixer.Sound('mario_moeda_efeito_sonoro_toquesengracadosmp3.com.mp3')
collision_sound.set_volume(0.3)

class Game:
    largura: int
    altura: int

    def __init__(self):
        self.largura = 700
        self.altura = 700
        self.background = pygame.image.load('uma-multidao-de-pessoas-esta-reunida-em-um-clube-com-uma-luz-rosa-e-roxa.jpg')
        self.background = pygame.transform.scale(self.background, (self.largura, self.altura))
    
    def set_font(self):
        fonte = pygame.font.SysFont('arial', 30, True, True)
        return fonte

    def set_mode(self):
        tela_jogo = pygame.display.set_mode((self.largura, self.altura))
        return tela_jogo
    
    def set_caption(self):
        pygame.display.set_caption('Segurança de bar')
    
    def render(self, fonte, texto):
        texto_formatado = fonte.render(texto, True, (255, 255, 255))
        return texto_formatado

class Block:
    x: int
    y: int

    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def create_rect(self, tela_jogo, color):
        bloco = pygame.draw.rect(tela_jogo, color, (self.x, self.y, 50, 50))      
        return bloco
    
    def create_security(self, tela_jogo):
        all_sprites.draw(tela_jogo)

class Segurança(pygame.sprite.Sprite):
    x: int
    y: int

    def __init__ (self ,x ,y):
        self.x = x
        self.y = y
        pygame.sprite.Sprite.__init__(self)
        self.sprites = []
        self.sprites.append(pygame.image.load('./sprites_new/idle_0.png'))
        self.sprites.append(pygame.image.load('./sprites_new/run_1.png'))
        self.sprites.append(pygame.image.load('./sprites_new/run_2.png'))
        self.sprites.append(pygame.image.load('./sprites_new/run_3.png'))
        self.sprites.append(pygame.image.load('./sprites_new/run_4.png'))
        self.sprites.append(pygame.image.load('./sprites_new/run_5.png'))
        self.sprite_atual = 0
        self.image = self.sprites[self.sprite_atual]
        self.image = pygame.transform.scale(self.image, (36*2, 45*2))
        self.rect = self.image.get_rect()
        self.rect.center = x, y

    def move(self, x ,y):
        self.rect = self.image.get_rect()
        self.rect.center = x, y

    def run_animation(self):
        if self.sprite_atual == 0:
            self.sprite_atual = 1
        self.sprite_atual = self.sprite_atual + 0.004
        if self.sprite_atual >= len(self.sprites):
            self.sprite_atual = 1
        self.image = self.sprites[int(self.sprite_atual)]
        self.image = pygame.transform.scale(self.image, (36*2, 45*2))
    
    def idle(self):
        self.sprite_atual = 0
        self.image = self.sprites[self.sprite_atual]
        self.image = pygame.transform.scale(self.image, (36*2, 45*2))
        
    def flip(self):
        self.image = pygame.transform.flip(self.image,True,False)

all_sprites = pygame.sprite.Group()
segurança = Segurança(0,0)
all_sprites.add(segurança)

game = Game()
fonte = game.set_font()
tela_jogo = game.set_mode()
game.set_caption()
pygame.mixer.music.load('Daniel Birch - Dancing With Fire.mp3')
pygame.mixer.music.play(-1) 

move_speed = 0.3

x = game.largura/2
y = game.altura/2

pontos_verde = 0
pontos_azul = 0
pontos_vermelho = 0
flipped = False

def criar_blocos(cor, quantidade, lista_blocos):
    for _ in range(quantidade):
        x = randint(10, 600)
        y = randint(20, 500)
        bloco = Block(x, y)
        bloco.create_rect(tela_jogo, color=cor)
        bloco.create_security(tela_jogo)
        lista_blocos.append({'bloco': bloco, 'cor': cor})

lista_blocos = []
criar_blocos('red', 1, lista_blocos)
criar_blocos('blue', 1, lista_blocos )
criar_blocos('green',1, lista_blocos )

while True:
    tela_jogo.blit(game.background, (0, 0))
    andando = False
    texto_formatado = game.render(fonte=fonte, texto=f'Big Apple: {pontos_verde}')
    texto_formatado_2 = game.render(fonte=fonte, texto=f'Água: {pontos_azul}')
    texto_formatado_3 = game.render(fonte=fonte, texto=f'Suco de Morango: {pontos_vermelho}')

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()

    if pygame.key.get_pressed()[K_a]:
        flipped = True
        x = x - move_speed
        andando = True
    if pygame.key.get_pressed()[K_d]:
        x = x + move_speed
        andando = True
        flipped = False
    if pygame.key.get_pressed()[K_w]:
        y = y - move_speed
        andando = True
    if pygame.key.get_pressed()[K_s]:
        y = y + move_speed
        andando = True
    if not andando:
        segurança.idle()
    else:
        segurança.run_animation()
    if flipped:
        segurança.flip()

    for bloco_info in lista_blocos:
        bloco = bloco_info['bloco']
        cor = bloco_info['cor']
        rect = bloco.create_rect(tela_jogo, color=cor)

        if segurança.rect.colliderect(rect):
            collision_sound.play()
            bloco.x = randint(10, 600)
            bloco.y = randint(20, 500)
            if cor == 'red':  # Vermelho
                pontos_vermelho += 1
            elif cor == 'blue':  # Azul
                pontos_azul += 1
            elif cor == 'green':  # Verde
                pontos_verde += 1

    segurança.move(x, y)
    all_sprites.draw(tela_jogo)
    
    if x < -100:
        x = 700 + 100
    elif x > 700 + 100:
        x = -100
    if y < -100:
        y = 700 + 100
    elif y > 700 + 100:
        y = -100

    tela_jogo.blit(texto_formatado, (400, 40))
    tela_jogo.blit(texto_formatado_2, (400, 0))
    tela_jogo.blit(texto_formatado_3, (400, 80))
    pygame.display.update()
