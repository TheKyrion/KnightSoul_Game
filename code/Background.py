from code.Entity import Entity
from code.Const import LARG_TELA, ALTURA_TELA, ENTITY_SPEED
import pygame


class Background(Entity):
    def __init__(self, name: str, position: tuple):
        super().__init__(name, position)
        # Redimensiona a imagem para a largura e altura da tela
        self.surf = pygame.transform.scale(self.surf, (LARG_TELA, ALTURA_TELA))
        self.rect = self.surf.get_rect(topleft=position)
        self.width = self.rect.width

    def move(self, direction_x=0):
        self.rect.x -= ENTITY_SPEED[self.name] * direction_x

        if self.rect.right < 0:
            self.rect.left += self.width * 2

        elif self.rect.left > LARG_TELA:
            self.rect.right -= self.width * 2
