import pygame
from code.Const import ALTURA_TELA
from code.Entity import Entity


class Player(Entity):
    def __init__(self, name: str, position: tuple):
        super().__init__(name, position)

        # ---- spritesheets -------------------------------------------------
        sprite_sheet_idle   = pygame.image.load('./assets/idle.png').convert_alpha()
        sprite_sheet_run    = pygame.image.load('./assets/idle9.png').convert_alpha()
        sprite_sheet_attack = pygame.image.load('./assets/idle3.png').convert_alpha()

        # ---------------- idle (8) ----------------------------------------
        sheet_width_idle, sheet_height_idle = sprite_sheet_idle.get_size()
        num_idle_frames  = 8
        frame_w_idle     = sheet_width_idle // num_idle_frames
        self.idle_frames = [
            sprite_sheet_idle.subsurface(pygame.Rect(i * frame_w_idle, 0, frame_w_idle, sheet_height_idle))
            for i in range(num_idle_frames)
        ]

        # ---------------- run (8) -----------------------------------------
        sheet_width_run, sheet_height_run = sprite_sheet_run.get_size()
        num_run_frames  = 8
        frame_w_run     = sheet_width_run // num_run_frames
        self.run_frames = [
            sprite_sheet_run.subsurface(pygame.Rect(i * frame_w_run, 0, frame_w_run, sheet_height_run))
            for i in range(num_run_frames)
        ]

        # ---------------- attack (6) --------------------------------------
        sheet_width_att, sheet_height_att = sprite_sheet_attack.get_size()
        num_attack_frames = 6
        frame_w_att       = sheet_width_att // num_attack_frames
        self.attack_frames = [
            sprite_sheet_attack.subsurface(pygame.Rect(i * frame_w_att, 0, frame_w_att, sheet_height_att))
            for i in range(num_attack_frames)
        ]

        # ---- atributos ----------------------------------------------------
        self.frame_index     = 0
        self.animation_delay = 100   # ms

        self.last_update = pygame.time.get_ticks()
        self.state       = 'idle'
        self.attacking   = False

        self.speed_y = 5
        self.name    = name

        self.surf = self.idle_frames[self.frame_index]
        self.rect = self.surf.get_rect()
        self.rect.topleft = position

    # ---------------------------------------------------------------------
    # LÓGICA DE ANIMAÇÃO
    # ---------------------------------------------------------------------
    def update(self):
        current_time = pygame.time.get_ticks()

        # ---------- ataque -------------------------------------------------
        if self.state == 'attack':
            if current_time - self.last_update > self.animation_delay:
                self.last_update = current_time
                self.frame_index += 1

                if self.frame_index >= len(self.attack_frames):
                    # terminou o ataque
                    self.state     = 'idle'
                    self.attacking = False
                    self.frame_index = 0

            idx = min(self.frame_index, len(self.attack_frames) - 1)
            self.surf = self.attack_frames[idx]

        # ---------- idle ---------------------------------------------------
        elif self.state == 'idle':
            self.surf = self.idle_frames[0]

        # ---------- run ----------------------------------------------------
        elif self.state == 'run':
            if current_time - self.last_update > self.animation_delay:
                self.last_update = current_time
                self.frame_index = (self.frame_index + 1) % len(self.run_frames)
            self.surf = self.run_frames[self.frame_index]

    # ---------------------------------------------------------------------
    # CONTROLE / MOVIMENTO
    # ---------------------------------------------------------------------
    def move(self):
        keys = pygame.key.get_pressed()

        # já em ataque? não altera estado nem posição
        if self.attacking:
            return

        # -------- iniciar ataque ------------------------------------------
        if keys[pygame.K_SPACE]:
            self.state       = 'attack'
            self.attacking   = True
            self.frame_index = 0
            self.last_update = pygame.time.get_ticks()
            return

        # -------- movimento vertical --------------------------------------
        if keys[pygame.K_UP]:
            self.rect.y = max(0, self.rect.y - self.speed_y)
        if keys[pygame.K_DOWN]:
            self.rect.y = min(ALTURA_TELA - self.rect.height, self.rect.y + self.speed_y)

        # -------- idle / run ----------------------------------------------
        if keys[pygame.K_RIGHT] or keys[pygame.K_LEFT]:
            if self.state != 'run':
                self.frame_index = 0          # reinicia animação de corrida
            self.state = 'run'
        else:
            self.state = 'idle'
