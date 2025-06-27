import pygame
from code.Entity import Entity
from code.Const import CARPET_TOP, CARPET_BOTTOM, LARG_TELA

class Enemy(Entity):
    """Inimigo genérico com idle, ataque, dano e morte."""

    def __init__(self, name: str, position: tuple):
        super().__init__(name, position)

        # ---- carrega sprites ------------------------------------------
        idle   = pygame.image.load("./assets/FLYING.png").convert_alpha()
        attack = pygame.image.load("./assets/ATTACK.png").convert_alpha()
        hit    = pygame.image.load("./assets/HURT.png").convert_alpha()
        die    = pygame.image.load("./assets/DEATH.png").convert_alpha()

        # quantos quadros em cada spritesheet
        self.idle_frames   = self._split_sheet(idle,   4)  # 6 quadros
        self.attack_frames = self._split_sheet(attack, 8)
        self.hit_frames    = self._split_sheet(hit,    4)
        self.die_frames    = self._split_sheet(die,    6)

        # ---- estado ----------------------------------------------------
        self.state        = "FLYING"      # idle / attack / hit / die
        self.frame_index  = 0
        self.delay        = 120         # ms por quadro
        self.last_update  = pygame.time.get_ticks()
        self.speed        = 1           # patrulha lenta

        self.surf = self.idle_frames[0]
        self.rect = self.surf.get_rect(topleft=position)
        self.rect.bottom = CARPET_BOTTOM - 50
        self.rect.y -= 40

        # ...................................................................
    def _split_sheet(self, sheet: pygame.Surface, n_frames: int):
        w, h = sheet.get_size()
        frame_w = w // n_frames
        return [sheet.subsurface(pygame.Rect(i*frame_w, 0, frame_w, h))
                for i in range(n_frames)]

    # ...................................................................
    def move(self):
        # patrulha simples – vai e volta entre 0 e LARG_TELA-rect.w
        self.rect.x += self.speed
        if self.rect.right >= LARG_TELA or self.rect.left <= 0:
            self.speed *= -1

        # mantém no tapete
        self.rect.bottom = CARPET_BOTTOM - 6


    # ...................................................................
    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update < self.delay:
            return

        self.last_update = now
        self.frame_index += 1

        if self.state == "FLYING":
            self.frame_index %= len(self.idle_frames)
            self.surf = self.idle_frames[self.frame_index]

        elif self.state == "ATTACK":
            if self.frame_index >= len(self.attack_frames):
                self.state = "FLYING"
                self.frame_index = 0
            self.surf = self.attack_frames[min(self.frame_index, len(self.attack_frames)-1)]

        elif self.state == "HURT":
            if self.frame_index >= len(self.hit_frames):
                self.state = "FLYING"
                self.frame_index = 0
            self.surf = self.hit_frames[min(self.frame_index, len(self.hit_frames)-1)]

        elif self.state == "DEATH":
            if self.frame_index >= len(self.die_frames):
                self.kill()                     # remove do grupo se usar pygame.sprite
                return
            self.surf = self.die_frames[self.frame_index]
