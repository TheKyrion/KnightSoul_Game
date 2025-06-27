import pygame
from code.Const import (
    LARG_TELA,
    ALTURA_TELA,
    CARPET_TOP,
    CARPET_BOTTOM,
)
from code.Entity import Entity

# ------------------------------------------------------------
# CONSTANTE: posição-âncora (centro horizontal da janela)
# ------------------------------------------------------------
PLAYER_ANCHOR_X = LARG_TELA // 2


class Player(Entity):
    """Jogador principal (setas + espaço)."""

    def __init__(self, name: str, position: tuple):
        super().__init__(name, position)

        # -------- carrega sprites ---------------------------------------
        idle = pygame.image.load("./assets/idle.png").convert_alpha()
        run = pygame.image.load("./assets/idle9.png").convert_alpha()
        attack = pygame.image.load("./assets/idle3.png").convert_alpha()

        w, h = idle.get_size()
        self.idle_frames = [idle.subsurface(pygame.Rect(i * w // 8, 0, w // 8, h)) for i in range(8)]
        w, h = run.get_size()
        self.run_frames = [run.subsurface(pygame.Rect(i * w // 8, 0, w // 8, h)) for i in range(8)]
        w, h = attack.get_size()
        self.attack_frames = [attack.subsurface(pygame.Rect(i * w // 6, 0, w // 6, h)) for i in range(6)]

        # -------- atributos ---------------------------------------------
        self.state = "idle"
        self.attacking = False
        self.frame_index = 0
        self.animation_delay = 100
        self.last_update = pygame.time.get_ticks()

        self.speed = 1  # velocidade em px por quadro
        self.delta_x = 0  # ← deslocamento “desejado” neste frame

        self.surf = self.idle_frames[0]
        self.rect = self.surf.get_rect()
        self.rect.centerx = PLAYER_ANCHOR_X  # sempre fixo
        self.rect.centery = position[1]

    # ------------------------------------------------------------------
    #  ANIMAÇÃO
    # ------------------------------------------------------------------
    def update(self):
        now = pygame.time.get_ticks()

        if self.state == "attack":
            if now - self.last_update > self.animation_delay:
                self.last_update = now
                self.frame_index += 1
                if self.frame_index >= len(self.attack_frames):
                    self.state = "idle"
                    self.attacking = False
                    self.frame_index = 0
            self.surf = self.attack_frames[min(self.frame_index, len(self.attack_frames) - 1)]

        elif self.state == "run":
            if now - self.last_update > self.animation_delay:
                self.last_update = now
                self.frame_index = (self.frame_index + 1) % len(self.run_frames)
            self.surf = self.run_frames[self.frame_index]

        else:  # idle
            self.surf = self.idle_frames[0]

    # ------------------------------------------------------------------
    #  MOVIMENTO / CONTROLES
    # ------------------------------------------------------------------
    def move(self):
        keys = pygame.key.get_pressed()

        # ataque ---------------------------------------------------------
        if not self.attacking and keys[pygame.K_SPACE]:
            self.state = "attack"
            self.attacking = True
            self.frame_index = 0
            self.last_update = pygame.time.get_ticks()
            self.delta_x = 0
            return

        if self.attacking:
            self.delta_x = 0
            return

        # deslocamento “desejado” ---------------------------------------
        dx = 0
        dy = 0

        # setas horizontais
        if keys[pygame.K_RIGHT]:
            dx += self.speed
        if keys[pygame.K_LEFT]:
            dx -= self.speed

        # setas verticais
        if keys[pygame.K_UP]:
            dy -= self.speed
        if keys[pygame.K_DOWN]:
            dy += self.speed

        # trava vertical no tapete
        self.rect.y = max(CARPET_TOP, min(self.rect.y + dy, CARPET_BOTTOM - self.rect.height))

        # mantém sempre no centro
        self.rect.centerx = PLAYER_ANCHOR_X

        # guarda deslocamento horizontal real para o Level usar
        self.delta_x = dx

        # decide estado (run / idle) ------------------------------------
        self.state = "run" if (dx or dy) else "idle"


# ---------------------------------------------------------------------
#  PLAYER 2 – WASD + F, sprites *_p2
# ---------------------------------------------------------------------
class Player2(Player):
    """Segundo jogador fixo no centro (usa WASD + F)."""

    def __init__(self, name: str, position: tuple):
        super().__init__(name, position)
        self._load_p2_sprites()

    def _load_p2_sprites(self):
        idle = pygame.image.load("./assets/idle_p2.png").convert_alpha()
        run = pygame.image.load("./assets/idle9_p2.png").convert_alpha()
        attack = pygame.image.load("./assets/idle5_p2.png").convert_alpha()

        w, h = idle.get_size()
        self.idle_frames = [idle.subsurface(pygame.Rect(i * w // 8, 0, w // 8, h)) for i in range(8)]
        w, h = run.get_size()
        self.run_frames = [run.subsurface(pygame.Rect(i * w // 8, 0, w // 8, h)) for i in range(8)]
        w, h = attack.get_size()
        self.attack_frames = [attack.subsurface(pygame.Rect(i * w // 6, 0, w // 6, h)) for i in range(6)]
        self.surf = self.idle_frames[0]

    # controles WASD ----------------------------------------------------
    def move(self):
        keys = pygame.key.get_pressed()

        if not self.attacking and keys[pygame.K_f]:
            self.state = "attack"
            self.attacking = True
            self.frame_index = 0
            self.last_update = pygame.time.get_ticks()
            self.delta_x = 0
            return

        if self.attacking:
            self.delta_x = 0
            return

        dx = dy = 0
        if keys[pygame.K_d]:
            dx += self.speed
        if keys[pygame.K_a]:
            dx -= self.speed
        if keys[pygame.K_w]:
            dy -= self.speed
        if keys[pygame.K_s]:
            dy += self.speed

        # Limita verticalmente no tapete
        self.rect.y = max(CARPET_TOP, min(self.rect.y + dy, CARPET_BOTTOM - self.rect.height))

        # Limita horizontalmente dentro da tela (ajuste conforme quiser)
        self.rect.x = max(0, min(self.rect.x + dx, LARG_TELA - self.rect.width))

        # Atualiza delta_x para poder usar se quiser, mas player2 não move o mapa
        self.delta_x = dx

        self.state = "run" if (dx or dy) else "idle"
