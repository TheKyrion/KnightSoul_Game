import sys, pygame
from pygame.font import Font
from pygame import Surface, Rect

from code.Const import COLOR_WHITE, ALTURA_TELA, LARG_TELA
from code.Entity import Entity
from code.EntityFactory import EntityFactory
from code.Player import Player, Player2
from code.Enemy import Enemy
from code.Background import Background


class Level:
    def __init__(self, window, name, game_mode):
        self.window = window
        self.name = name
        self.game_mode = game_mode

        # -------- fundos -------------------------------------------------
        self.backgrounds = EntityFactory.get_entity("bg1")

        # -------- lista principal de entidades --------------------------
        self.game_entities: list[Entity] = []

        # player 1 (âncora da câmera)
        self.player = EntityFactory.get_entity("player",
                                               (100, ALTURA_TELA // 2))
        self.game_entities.append(self.player)

        # player 2 opcional
        if "COOPERATIVO" in game_mode:
            p2 = EntityFactory.get_entity("player2",
                                          (200, ALTURA_TELA // 2))
            self.game_entities.append(p2)

        # inimigos iniciais
        for x in (600, 900, 1200, 1500, 1800):
            e = EntityFactory.get_entity("enemy", (x, 0))
            self.game_entities.append(e)

        self.timeout = 20000

    # ===================================================================
    def run(self):
        pygame.mixer_music.load("./assets/level1.mp3")
        pygame.mixer_music.play(-1)
        clock = pygame.time.Clock()

        level_active = True
        while level_active:
            clock.tick(60)

            # === 1. Eventos ============================================
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit();
                    sys.exit()
                if event.type == pygame.KEYDOWN \
                        and event.key == pygame.K_ESCAPE:
                    level_active = False

            # === 2. Move players / inimigos ============================
            players = [e for e in self.game_entities if isinstance(e, Player)]
            enemies = [e for e in self.game_entities if isinstance(e, Enemy)]

            for ent in self.game_entities:
                if isinstance(ent, Player):
                    ent.move()
                elif isinstance(ent, Enemy):
                    ent.move(players)  # passa lista de players

            # === 3. Scroll da câmera (player 1) ========================
            delta_x = getattr(self.player, "delta_x", 0)
            for bg in self.backgrounds:
                bg.move(delta_x)
            for ent in self.game_entities:
                if ent is not self.player:
                    ent.rect.x -= delta_x

            # === 4. Colisões / dano / score ===========================
            # players atacam
            for pl in players:
                hb = pl.get_attack_hitbox()
                if not hb:
                    continue
                for en in enemies:
                    if en.state == "DEATH":
                        continue
                    if hb.colliderect(en.rect):
                        died = en.take_damage(1)
                        if died:
                            pl.score += 100  # +100 pontos!

            # inimigos atacam
            now = pygame.time.get_ticks()
            for en in enemies:
                hb = en.get_attack_hitbox()
                if not hb or now < en.next_attack:
                    continue
                for pl in players:
                    if pl.state != "death" and hb.colliderect(pl.rect):
                        pl.take_damage(1)
                        en.next_attack = now + en.ATTACK_COOLDOWN

            # === 5. Atualiza animações + limpa mortos =================
            alive = []
            for ent in self.game_entities:
                ent.update()
                if isinstance(ent, Enemy) and ent.state == "DEATH" \
                        and ent.frame_index >= len(ent.death_frames):
                    continue
                if isinstance(ent, Player) and ent.state == "death" \
                        and ent.frame_index >= len(ent.death_frames):
                    continue
                alive.append(ent)
            self.game_entities = alive

            # === 6. Desenha ===========================================
            self.window.fill((0, 0, 0))  # clear

            for bg in self.backgrounds:
                self.window.blit(bg.surf, bg.rect)
            for ent in self.game_entities:
                self.window.blit(ent.surf, ent.rect)

            # HUD (HP + SCORE)
            self.draw_hud(players)

            # extras: fps / entidades
            self.level_text(14, f"fps: {clock.get_fps():.0f}",
                            COLOR_WHITE, (10, ALTURA_TELA - 35))
            self.level_text(14, f"Entidades: {len(self.game_entities)}",
                            COLOR_WHITE, (10, ALTURA_TELA - 20))

            pygame.display.flip()

        return "level_finished"

    # ------------------------------------------------------------------
    def draw_hud(self, players):
        """Mostra HP e SCORE de cada player no canto sup-esq."""
        x0, y0, dy = 10, 10, 20
        for idx, pl in enumerate(players, 1):
            txt = f"P{idx}  HP:{pl.hp:3d}   SCORE:{pl.score:5d}"
            self.level_text(30, txt, COLOR_WHITE, (x0, y0 + (idx - 1) * dy))

    # ------------------------------------------------------------------
    def level_text(self, size: int, txt: str, color: tuple, pos: tuple):
        font: Font = pygame.font.SysFont("Lucida Sans Typewriter", size)
        surf: Surface = font.render(txt, True, color).convert_alpha()
        rect: Rect = surf.get_rect(topleft=pos)
        self.window.blit(surf, rect)
