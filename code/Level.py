import sys, pygame
from pygame.font import Font
from pygame import Surface, Rect

from code.Const import COLOR_WHITE, ALTURA_TELA
from code.Entity import Entity
from code.EntityFactory import EntityFactory
from code.Player import Player
from code.Enemy import Enemy


class Level:
    """Fase do jogo.  Level 1 → 20 s;  Level 2 → 30 s."""

    def __init__(self, window, name, game_mode, players=None):
        self.window = window
        self.name = name  # "Level 1"  ou  "Level 2"
        self.game_mode = game_mode

        # -------- fundo ----------------------------------------------
        bg_tag = "bg1" if name == "Level 1" else "bg2"
        self.backgrounds = EntityFactory.get_entity(bg_tag)

        # -------- lista de entidades ---------------------------------
        self.game_entities: list[Entity] = []

        # -------- players --------------------------------------------
        if players is None:  # Level 1
            p1 = EntityFactory.get_entity("player",
                                          (100, ALTURA_TELA // 2))
            self.game_entities.append(p1)
            if "2P" in game_mode:
                p2 = EntityFactory.get_entity("player2",
                                              (200, ALTURA_TELA // 2))
                self.game_entities.append(p2)
        else:  # Level 2
            for pl in players:
                pl.rect.centery = ALTURA_TELA // 2
                pl.hp = 100  # restaura HP
                self.game_entities.append(pl)
            p1 = players[0]

        self.player = p1  # ancora

        # -------- inimigos ------------------------------------------
        for x in (600, 900, 1200, 1500, 1800):
            self.game_entities.append(
                EntityFactory.get_entity("enemy", (x, 0))
            )

        # -------- cronômetro ----------------------------------------
        if name == "Level 1":
            self.time_limit = 10_000  # 20 s
        elif name == "Level 2":
            self.time_limit = 10_000  # 20 s
        else:
            self.time_limit = 0  # sem limite
        self.time_left = self.time_limit

    # =================================================================
    def run(self):
        pygame.mixer_music.load("./assets/level1.mp3")
        pygame.mixer_music.set_volume(0.2)
        pygame.mixer_music.play(-1)
        clock = pygame.time.Clock()

        level_active = True
        while level_active:
            dt = clock.tick(60)

            # ---------------- eventos --------------------------------
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    pygame.quit();
                    sys.exit()
                if ev.type == pygame.KEYDOWN and ev.key == pygame.K_ESCAPE:
                    level_active = False

            # ---------------- cronômetro -----------------------------
            if self.time_limit:
                self.time_left -= dt

                if self.name == "Level 1" and self.time_left <= 0:
                    players_alive = [e for e in self.game_entities
                                     if isinstance(e, Player)]
                    return "next_level", players_alive

                if self.name == "Level 2" and self.time_left <= 0:
                    return "level_finished", None

            # ---------------- move entidades -------------------------
            players = [e for e in self.game_entities if isinstance(e, Player)]
            enemies = [e for e in self.game_entities if isinstance(e, Enemy)]

            for ent in self.game_entities:
                ent.move(players) if isinstance(ent, Enemy) else ent.move()

            # ---------------- scroll câmera --------------------------
            delta_x = getattr(self.player, "delta_x", 0)
            for bg in self.backgrounds:
                bg.move(delta_x)
            for ent in self.game_entities:
                if ent is not self.player:
                    ent.rect.x -= delta_x

            # ---------------- combate / score ------------------------
            for pl in players:
                hb = pl.get_attack_hitbox()
                if hb:
                    for en in enemies:
                        if en.state != "DEATH" and hb.colliderect(en.rect):
                            if en.take_damage(1):
                                pl.score += 100

            now = pygame.time.get_ticks()
            for en in enemies:
                hb = en.get_attack_hitbox()
                if hb and now >= en.next_attack:
                    for pl in players:
                        if pl.state != "death" and hb.colliderect(pl.rect):
                            pl.take_damage(1)
                            en.next_attack = now + en.ATTACK_COOLDOWN

            # ---------------- update / limpa mortos ------------------
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
            # -------------------------------------------------------
            # Se QUALQUER jogador terminou a animação de morte,
            # encerra a fase e volta ao menu
            # -------------------------------------------------------
            for pl in alive:
                if isinstance(pl, Player) and pl.state == "death" \
                        and pl.frame_index >= len(pl.death_frames) - 1:
                    return "player_dead", None

            # ---------------- desenha -------------------------------
            self.window.fill((0, 0, 0))
            for bg in self.backgrounds:
                self.window.blit(bg.surf, bg.rect)
            for ent in self.game_entities:
                self.window.blit(ent.surf, ent.rect)

            self.draw_hud(players)
            if self.time_limit:
                self.level_text(20,
                                f"TIME: {max(0, self.time_left) // 1000:02d}s",
                                COLOR_WHITE, (10, 50))

            pygame.display.flip()

        return "level_finished", None  # abortado por ESC

    # =================================================================
    def draw_hud(self, players):
        x0, y0, dy = 10, 10, 20
        for idx, pl in enumerate(players, 1):
            txt = f"P{idx}  HP:{pl.hp:3d}   SCORE:{pl.score:5d}"
            self.level_text(14, txt, COLOR_WHITE, (x0, y0 + (idx - 1) * dy))

    def level_text(self, size: int, txt: str, color: tuple, pos: tuple):
        font = pygame.font.SysFont("Lucida Sans Typewriter", size)
        surf = font.render(txt, True, color).convert_alpha()
        rect = surf.get_rect(topleft=pos)
        self.window.blit(surf, rect)
