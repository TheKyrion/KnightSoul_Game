import pygame
from code.Const import (
    LARG_TELA,
    CARPET_TOP,
    CARPET_BOTTOM,
)
from code.Entity import Entity

# Âncora horizontal (player 1 fica fixo nela)
PLAYER_ANCHOR_X = LARG_TELA // 2


# =====================================================================
# PLAYER 1  &  PLAYER 2
# =====================================================================
class Player(Entity):
    """Jogador principal (setas + espaço)."""

    def __init__(self, name: str, position: tuple):
        super().__init__(name, position)

        # ---- sprites -------------------------------------------------
        idle = pygame.image.load("./assets/idle.png").convert_alpha()
        run = pygame.image.load("./assets/idle9.png").convert_alpha()
        attack = pygame.image.load("./assets/idle3.png").convert_alpha()
        death = pygame.image.load("./assets/idle6.png").convert_alpha()
        hurt = pygame.image.load("./assets/idle7.png").convert_alpha()

        self.idle_frames = self._split(idle, 7)
        self.run_frames = self._split(run, 8)
        self.attack_frames = self._split(attack, 6)
        self.death_frames = self._split(death, 12)
        self.hurt_frames = self._split(hurt, 4)

        # ---- atributos ----------------------------------------------
        self.state = "idle"
        self.frame_index = 0
        self.delay = 100
        self.last_update = pygame.time.get_ticks()
        self.attacking = False
        self.hp = 100
        self.score = 0
        self.speed = 2
        self.delta_x = 0
        self.facing = 1  # 1 = direita, -1 = esquerda

        self.invulnerable_until = 0  # timestamp
        self.hurt_delay = 20  # ms

        self.surf = self.idle_frames[0]
        self.rect = self.surf.get_rect()
        self.rect.centerx = PLAYER_ANCHOR_X
        self.rect.centery = position[1]

    # -----------------------------------------------------------------
    def _split(self, sheet: pygame.Surface, n):
        w, h = sheet.get_size()
        fw = w // n
        return [sheet.subsurface(pygame.Rect(i * fw, 0, fw, h)) for i in range(n)]

    # -----------------------------------------------------------------
    def move(self):
        keys = pygame.key.get_pressed()
        if self.state == "death":
            self.delta_x = 0
            return

        if not self.attacking and keys[pygame.K_SPACE]:
            self.state = "attack"
            self.attacking = True
            self.frame_index = 0
            self.delta_x = 0
            return
        if self.attacking:
            self.delta_x = 0
            return

        dx = dy = 0
        if keys[pygame.K_RIGHT]:
            dx += self.speed
        if keys[pygame.K_LEFT]:
            dx -= self.speed
        if keys[pygame.K_UP]:
            dy -= self.speed
        if keys[pygame.K_DOWN]:
            dy += self.speed

        if dx:
            self.facing = 1 if dx > 0 else -1
        self.delta_x = dx

        # travas
        self.rect.y = max(CARPET_TOP, min(self.rect.y + dy, CARPET_BOTTOM - self.rect.height))
        self.rect.centerx = PLAYER_ANCHOR_X

        self.state = "run" if (dx or dy) else "idle"

    # -----------------------------------------------------------------

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update < self.delay:
            return
        self.last_update = now
        self.frame_index += 1

        if self.state == "idle":
            self.frame_index %= len(self.idle_frames)
            self.surf = self.idle_frames[self.frame_index]
        elif self.state == "run":
            self.frame_index %= len(self.run_frames)
            self.surf = self.run_frames[self.frame_index]
        elif self.state == "attack":
            if self.frame_index >= len(self.attack_frames):
                self.state = "idle"
                self.attacking = False
                self.frame_index = 0
            self.surf = self.attack_frames[min(self.frame_index, len(self.attack_frames) - 1)]
        elif self.state == "hurt":
            if self.frame_index >= len(self.hurt_frames):
                self.state = "idle"
                self.frame_index = 0
            else:
                self.surf = self.hurt_frames[self.frame_index]
        elif self.state == "death":
            if self.frame_index >= len(self.death_frames):
                self.frame_index = len(self.death_frames) - 1
            self.surf = self.death_frames[self.frame_index]

    # -----------------------------------------------------------------
    def get_attack_hitbox(self):
        if self.state == "attack" and 1 <= self.frame_index <= 3:
            hb = self.rect.inflate(10, -10)  # caixa menor
            return hb.move(15 * self.facing, 0)  # desloca menos para frente
        return None

    def take_damage(self, dmg=1):
        now = pygame.time.get_ticks()
        if self.state == "death":
            return
        if now < self.invulnerable_until:
            return  # ainda piscando – ignora

        self.hp -= dmg
        self.invulnerable_until = now + self.hurt_delay
        if self.hp <= 0:
            self.state = "death"
            self.frame_index = 0
        else:
            self.state = "hurt"
            self.frame_index = 0


class Player2(Player):
    """Segundo jogador (WASD + F)."""

    def __init__(self, name: str, position: tuple):
        super().__init__(name, position)
        self._load_p2_sprites()

    def _load_p2_sprites(self):
        idle = pygame.image.load("./assets/idle_p2.png").convert_alpha()
        run = pygame.image.load("./assets/idle9_p2.png").convert_alpha()
        attack = pygame.image.load("./assets/idle5_p2.png").convert_alpha()
        death = pygame.image.load("./assets/idle6_p2.png").convert_alpha()
        self.idle_frames = self._split(idle, 7)
        self.run_frames = self._split(run, 8)
        self.attack_frames = self._split(attack, 6)
        self.death_frames = self._split(death, 6)
        self.surf = self.idle_frames[0]

    def move(self):
        keys = pygame.key.get_pressed()
        if self.state == "death":
            self.delta_x = 0
            return
        if not self.attacking and keys[pygame.K_f]:
            self.state = "attack"
            self.attacking = True
            self.frame_index = 0
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
        if dx:
            self.facing = 1 if dx > 0 else -1
        self.rect.y = max(CARPET_TOP, min(self.rect.y + dy, CARPET_BOTTOM - self.rect.height))
        self.rect.x = max(0, min(self.rect.x + dx, LARG_TELA - self.rect.width))
        self.delta_x = dx
        self.state = "run" if (dx or dy) else "idle"
