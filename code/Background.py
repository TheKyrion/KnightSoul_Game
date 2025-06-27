from code.Entity import Entity
from code.Const import LARG_TELA, ALTURA_TELA, ENTITY_SPEED
import pygame


class Background(Entity):
    def __init__(self, name: str, position: tuple):
        super().__init__(name, position)

        # redimensiona para caber na tela inteira
        self.surf = pygame.transform.scale(self.surf, (LARG_TELA, ALTURA_TELA))
        self.rect = self.surf.get_rect(topleft=position)
        self.width = self.rect.width

        # fator de paralaxe desta camada
        self.layer_speed = ENTITY_SPEED[self.name]

    # -----------------------------------------------------------------
    # dx_pixels → deslocamento do jogador em pixels (positivo: anda p/ direita)
    # -----------------------------------------------------------------
    def move(self, dx_pixels: int = 0):
        if dx_pixels == 0 or self.layer_speed == 0:
            return  # nada a mover

        # fundo se move na direção oposta ao jogador
        self.rect.x -= dx_pixels * self.layer_speed

        # recicla imagem quando sai da tela (scroll infinito)
        if self.rect.right < 0:                 # passou todo p/ esquerda
            self.rect.left += self.width * 2    # recoloca à direita
        elif self.rect.left > LARG_TELA:        # passou todo p/ direita
            self.rect.right -= self.width * 2   # recoloca à esquerda
