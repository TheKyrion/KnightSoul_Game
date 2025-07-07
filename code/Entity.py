import pygame


class Entity:
    def __init__(self, name: str, position: tuple, skip_image=False):
        self.name = name

        if not skip_image:
            self.surf = self.load_image(name)
            self.rect = self.surf.get_rect(topleft=position)
        else:
            # Espera que a classe filha defina `surf` e `rect`
            self.surf = None
            self.rect = pygame.Rect(position[0], position[1], 0, 0)

    def load_image(self, name: str) -> pygame.Surface:
        try:
            return pygame.image.load(f'./assets/{name}.png').convert_alpha()
        except FileNotFoundError:
            print(f"[ERRO] Imagem './assets/{name}.png' não encontrada!")
            surface = pygame.Surface((50, 50), pygame.SRCALPHA)
            surface.fill((255, 0, 0, 128))  # Transparente avermelhado
            return surface

    def update(self):
        pass  # Para ser sobrescrito pelas classes filhas

    def move(self, direction_x=0):
        pass  # Usado apenas por entidades com rolagem (ex: fundo)
