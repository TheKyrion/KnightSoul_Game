import sys
import pygame
from pygame import Surface, Rect
from pygame.font import Font
from code.Player import Player
from code.Const import COLOR_WHITE, ALTURA_TELA, LARG_TELA, CARPET_BOTTOM  # Importe LARG_TELA
from code.Entity import Entity
from code.EntityFactory import EntityFactory
from code.Background import Background  # Importar Background


class Level:

    def __init__(self, window, name, game_mode):
        self.window = window
        self.name = name
        self.game_mode = game_mode

        self.backgrounds: list[Background] = EntityFactory.get_entity('bg1')
        self.game_entities: list[Entity] = []

        self.player = EntityFactory.get_entity('player', (100, ALTURA_TELA // 2))
        self.game_entities.append(self.player)

        if "COOPERATIVO" in game_mode:
            p2 = EntityFactory.get_entity('player2', (200, ALTURA_TELA // 2))
            self.game_entities.append(p2)

        enemy1 = EntityFactory.get_entity(
            'enemy',
            (600, 0)  # 64 = altura aproximada do sprite
        )
        self.game_entities.append(enemy1)

        self.timeout = 20000

    def run(self):
        pygame.mixer_music.load('./assets/level1.mp3')
        pygame.mixer_music.play(-1)
        clock = pygame.time.Clock()

        level_active = True
        while level_active:
            clock.tick(60)

            # === 1. Eventos ===
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    level_active = False

            # === 2. Movimento de todos os Players ===
            for p in self.game_entities:
                if isinstance(p, Player):
                    p.move()

            # === 3. Scroll da câmera (Player-1) ===
            delta_x = getattr(self.player, "delta_x", 0)

            # 3a. Fundo se move no sentido oposto
            for bg in self.backgrounds:
                bg.move(delta_x)

            # 3b. TODO objeto que NÃO é o Player-1 é empurrado pelo scroll
            for ent in self.game_entities:
                if ent is not self.player:  # Player-2, inimigos, etc.
                    ent.rect.x -= delta_x

            # === 4. Atualiza animações ===
            for ent in self.game_entities:
                ent.update()

            # === 5. Limpa tela ===
            self.window.fill((0, 0, 0))

            # === 6. Desenha fundo e entidades ===
            for bg in self.backgrounds:
                self.window.blit(bg.surf, bg.rect)

            for ent in self.game_entities:
                self.window.blit(ent.surf, ent.rect)

            # === 7. HUD simples ===
            self.level_text(14, f'{self.name} - Timeout: {self.timeout / 1000:.1f}s', COLOR_WHITE, (10, 5))
            self.level_text(14, f'fps: {clock.get_fps():.0f}', COLOR_WHITE, (10, ALTURA_TELA - 35))
            self.level_text(14, f'entidades: {len(self.game_entities)}', COLOR_WHITE, (10, ALTURA_TELA - 20))

            pygame.display.flip()

        return "level_finished"  # Retorna um resultado quando o loop do nível termina

    def level_text(self, text_size: int, text: str, text_color: tuple, text_pos: tuple):
        text_font: Font = pygame.font.SysFont(name="Lucida Sans Typewriter", size=text_size)
        text_surf: Surface = text_font.render(text, True, text_color).convert_alpha()
        text_rect: Rect = text_surf.get_rect(left=text_pos[0], top=text_pos[1])
        self.window.blit(text_surf, text_rect)
