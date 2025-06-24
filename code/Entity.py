import pygame


class Entity:
    def __init__(self, name: str, position: tuple):
        self.name = name
        self.surf = self.load_image(name)
        self.rect = self.surf.get_rect(topleft=position)

    def load_image(self, name: str) -> pygame.Surface:
        try:
            return pygame.image.load(f'./assets/{name}.png').convert_alpha()
        except FileNotFoundError:
            print(f"[ERRO] Imagem './assets/{name}.png' não encontrada!")
            # Gera uma superfície padrão vermelha para debug
            surface = pygame.Surface((50, 50), pygame.SRCALPHA)
            surface.fill((255, 0, 0, 128))
            return surface

    def update(self):
        pass  # Para ser sobrescrito pelas classes filhas (como Player)

    def move(self, direction_x=0):
        pass  # Para entidades que se movem (como o background)
