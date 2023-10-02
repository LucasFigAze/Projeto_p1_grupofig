import pygame
from pygame.locals import *
from sys import exit
from random import randint
cont = 0
pygame.init()
############## ajeitar a musica de fundo ################
#musica_de_fundo = pygame.mixer.music.load('Daniel Birch - Dancing With Fire.mp3')
#pygame.mixer.music.play(-1)

#barulho_colisao = pygame.mixer.Sound('mario_moeda_efeito_sonoro_toquesengracadosmp3.com.mp3')

class Game:
    largura: int
    altura: int

    def __init__(self):
        self.largura = 700
        self.altura = 700
    
    def set_font(self):
        # texto em arial, tamanho 40, negrito true e itálico true
        fonte = pygame.font.SysFont('arial', 40, True, True)
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
        bloco = pygame.draw.rect(tela_jogo, color, (self.x, self.y, 100, 100))      
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
    
    #Animação do boneco correndo
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
        
    #Quando clicar 'a' girar boneco
    def flip(self):
        self.image = pygame.transform.flip(self.image,True,False)
        


all_sprites = pygame.sprite.Group()
segurança = Segurança(0,0)
all_sprites.add(segurança)


game = Game()
fonte = game.set_font()
tela_jogo = game.set_mode()
game.set_caption()

move_speed = 0.3

x = game.largura/2
y = game.altura/2

# posição random bloco verde
x_verde = randint(10,600)
y_verde = randint(20,500)

# posição random bloco azul
x_azul = randint(30, 400)
y_azul = randint(40, 300)

# posição random bloco vermelho
x_vermelho = randint(50, 400)
y_vermelho = randint(60, 300)

pontos_verde = 0
pontos_azul = 0
pontos_vermelho = 0


flipped=False
#relogio = pygame.time.Clock()

#criando o loop principal
while True:
    #relogio.tick(60)
    andando=False
    tela_jogo.fill((0,0,0))
    texto_formatado = game.render(texto=f'Verde: {pontos_verde}', fonte=fonte)
    texto_formatado_2 = game.render(texto=f'Azul: {pontos_azul}', fonte=fonte)
    texto_formatado_3 = game.render(texto=f'Vermelho: {pontos_vermelho}', fonte=fonte)
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
        andando=True
        flipped = False
    if pygame.key.get_pressed()[K_w]:
        y = y - move_speed
        andando=True
    if pygame.key.get_pressed()[K_s]:
        y = y + move_speed
        andando=True
    if not andando:
        segurança.idle()
    else:
        segurança.run_animation()
    if flipped:
        segurança.flip()

    bloco_vermelho = Block(x=x_vermelho, y=y_vermelho)
    rect_vermelho = bloco_vermelho.create_rect(tela_jogo, color=(200,0,0))
    
    bloco_azul = Block(x=x_azul, y=y_azul)
    rect_azul = bloco_azul.create_rect(tela_jogo, color=(0,0,200))
    
    bloco_verde = Block(x=x_verde, y=y_verde)
    rect_verde = bloco_verde.create_rect(tela_jogo, color=(0,200,0))

    segurança.move(x,y)
    all_sprites.draw(tela_jogo)
    
# Ultrapassando os limites da tela volta do outro lado.
    if x < -100:
        x = 700 + 100
    elif x > 700 + 100:
        x = -100
    if y < -100:
        y = 700 + 100
    elif y > 700 + 100:
        y = -100

    if segurança.rect.colliderect(rect_verde):
        x_verde = randint(10,600)
        y_verde = randint(20,500)
        pontos_verde += 1
        #barulho_colisao.play()
    if segurança.rect.colliderect(rect_azul):
        x_azul = randint(30, 400)
        y_azul = randint(40, 300)
        pontos_azul += 1
        #barulho_colisao.play()
    if segurança.rect.colliderect(rect_vermelho):
        x_vermelho = randint(50, 400)
        y_vermelho = randint(60, 300)
        pontos_vermelho += 1
        #barulho_colisao.play()

    tela_jogo.blit(texto_formatado, (400, 40))
    tela_jogo.blit(texto_formatado_2, (400, 0))
    tela_jogo.blit(texto_formatado_3, (400, 80))
    pygame.display.update()