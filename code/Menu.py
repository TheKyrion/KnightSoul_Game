import pygame
import sys
from pygame.font import Font
from pygame import Surface, Rect
from code.Const import COLOR_WHITE, MENU_OPTION, MENU_SELECT, LARG_TELA, ALTURA_TELA


class Menu:
    def __init__(self, window):
        self.window = window
        self.font = pygame.font.SysFont(name="Arial", size=24)  # Exemplo de fonte
        self.selected_option_index = 0
        self.menu_options = MENU_OPTION  # Usando a tupla de Const.py

        # Carrega a imagem de fundo do menu, se houver
        try:
            self.background_image = pygame.image.load(
                './assets/Battleground2.png').convert_alpha()
            self.background_image = pygame.transform.scale(self.background_image, (LARG_TELA, ALTURA_TELA))
        except FileNotFoundError:
            print("[ERRO] Imagem de fundo do menu não encontrada. Usando fundo preto.")
            self.background_image = None

    def run(self):
        menu_active = True
        while menu_active:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.selected_option_index = (self.selected_option_index - 1) % len(self.menu_options)
                    elif event.key == pygame.K_DOWN:
                        self.selected_option_index = (self.selected_option_index + 1) % len(self.menu_options)
                    elif event.key == pygame.K_RETURN:  # Se ENTER for pressionado
                        # Retorna a opção selecionada em vez de agir diretamente
                        return self.menu_options[self.selected_option_index]

            # Desenha o fundo
            if self.background_image:
                self.window.blit(self.background_image, (0, 0))
            else:
                self.window.fill((0, 0, 0))  # Fundo preto se não houver imagem

            # Desenha as opções do menu
            for i, option in enumerate(self.menu_options):
                color = MENU_SELECT if i == self.selected_option_index else COLOR_WHITE
                text_surf = self.font.render(option, True, color)
                text_rect = text_surf.get_rect(center=(LARG_TELA // 2, ALTURA_TELA // 2 + i * 50))
                self.window.blit(text_surf, text_rect)

            pygame.display.flip()

        # Se por algum motivo o loop terminar sem uma seleção, retorna algo padrão
        return None
