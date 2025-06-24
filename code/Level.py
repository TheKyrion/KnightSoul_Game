import sys
import pygame
from pygame import Surface, Rect
from pygame.font import Font
from code.Player import Player
from code.Const import COLOR_WHITE, ALTURA_TELA, LARG_TELA # Importe LARG_TELA
from code.Entity import Entity
from code.EntityFactory import EntityFactory
from code.Background import Background # Importar Background

class Level:

    def __init__(self, window, name, game_mode):
        self.window = window
        self.name = name
        self.game_mode = game_mode

        self.backgrounds: list[Background] = EntityFactory.get_entity('bg1')
        self.game_entities: list[Entity] = []

        self.player = EntityFactory.get_entity('player', (100, ALTURA_TELA // 2))
        self.game_entities.append(self.player)

        self.timeout = 20000

    def run(self):
        pygame.mixer_music.load('./assets/level1.mp3')
        pygame.mixer_music.play(-1)
        clock = pygame.time.Clock()

        level_active = True # Novo controle de loop para o nível
        while level_active: # O loop do nível roda enquanto 'level_active' for True
            clock.tick(60)

            # === 1. Eventos ===
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit() # Sai do programa se a janela for fechada

                # Exemplo: Se pressionar ESC no nível, ele termina e volta para o menu
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        level_active = False # Isso vai sair do loop 'while level_active'

            # === 2. Entrada do teclado ===
            keys = pygame.key.get_pressed()

            direction_x = 0
            if keys[pygame.K_RIGHT]:
                direction_x = 1
            elif keys[pygame.K_LEFT]:
                direction_x = -1

            # === 3. Atualiza lógica ===
            for bg in self.backgrounds:
                bg.move(direction_x)

            for ent in self.game_entities:
                if isinstance(ent, Player):
                    ent.move()
                # else: # Outras entidades podem ter outras lógicas de movimento
                #    ent.move(direction_x)

            self.player.update()

            # Exemplo: Diminui o timeout (remova se não usar)
            # self.timeout -= clock.get_rawtime()
            # if self.timeout <= 0:
            #     level_active = False # Nível termina por timeout
            #     return "timeout" # Retorna um resultado específico

            # === 4. Limpa tela ===
            self.window.fill((0, 0, 0))

            # === 5. Desenha entidades ===
            for bg in self.backgrounds:
                self.window.blit(bg.surf, bg.rect)

            for ent in self.game_entities:
                self.window.blit(ent.surf, ent.rect)
                # Opcional: Desenhar o retângulo para depuração (remova depois de testar)
                # if isinstance(ent, Player):
                #    pygame.draw.rect(self.window, (255, 0, 0), ent.rect, 2)

            # === 6. Informações na tela ===
            self.level_text(14, f'{self.name} - Timeout: {self.timeout / 1000:.1f}s', COLOR_WHITE, (10, 5))
            self.level_text(14, f'fps: {clock.get_fps():.0f}', COLOR_WHITE, (10, ALTURA_TELA - 35))
            self.level_text(14, f'entidades: {len(self.game_entities)}', COLOR_WHITE, (10, ALTURA_TELA - 20))

            pygame.display.flip()

        return "level_finished" # Retorna um resultado quando o loop do nível termina

    def level_text(self, text_size: int, text: str, text_color: tuple, text_pos: tuple):
        text_font: Font = pygame.font.SysFont(name="Lucida Sans Typewriter", size=text_size)
        text_surf: Surface = text_font.render(text, True, text_color).convert_alpha()
        text_rect: Rect = text_surf.get_rect(left=text_pos[0], top=text_pos[1])
        self.window.blit(text_surf, text_rect)