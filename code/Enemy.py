# =====================================================================
# ENEMY
# =====================================================================
import pygame
from code.Const import CARPET_BOTTOM, LARG_TELA
from code.Entity import Entity


class Enemy(Entity):
    ATTACK_RANGE = 30  # inicia ataque só bem perto
    ATTACK_COOLDOWN = 20  # ms entre golpes

    def __init__(self, name, position):
        # 1) carrega um dos sprites reais para definir tamanho
        idle_sheet = pygame.image.load("./assets/FLYING.png").convert_alpha()
        self.idle_frames = self._split(idle_sheet, 4)

        # usa o primeiro quadro como superfície inicial
        first_frame = self.idle_frames[0]
        self.surf = first_frame
        self.rect = first_frame.get_rect(topleft=position)

        # >>> NÃO chame super().__init__()  <<<
        # super().__init__() só serviria para procurar enemy.png

        # agora continue carregando o resto normalmente:
        attack = pygame.image.load("./assets/ATTACK.png").convert_alpha()
        hurt = pygame.image.load("./assets/HURT.png").convert_alpha()
        death = pygame.image.load("./assets/DEATH.png").convert_alpha()

        self.attack_frames = self._split(attack, 8)
        self.hurt_frames = self._split(hurt, 4)
        self.death_frames = self._split(death, 6)

        # atributos…
        self.state = "FLYING"
        self.frame_index = 0
        self.delay = 100
        self.last_update = pygame.time.get_ticks()

        self.speed = 1
        self.facing = 1  # 1→dir, -1→esq
        self.hp = 5  # mais vida
        self.next_attack = 0  # cooldown

        self.surf = self.idle_frames[0]
        self.rect = self.surf.get_rect(topleft=position)
        self.rect.bottom = CARPET_BOTTOM - 6

    # ------------------------------------------------------------------
    def move(self, players):
        if self.state == "DEATH":
            return

        # distância até algum player
        should_attack = any(
            abs(self.rect.centerx - p.rect.centerx) <= self.ATTACK_RANGE
            for p in players if p.state != "death"
        )

        if should_attack:
            if self.state != "ATTACK":
                self.state = "ATTACK"
                self.frame_index = 0
        else:
            if self.state == "ATTACK":
                self.state = "FLYING"
                self.frame_index = 0

        # patrulha horizontal (sempre), mas não troca de lado durante ataque
        if self.state != "ATTACK":
            self.rect.x += self.speed
            if self.rect.right >= LARG_TELA or self.rect.left <= 0:
                self.speed *= -1
                self.facing *= -1

        self.rect.bottom = CARPET_BOTTOM - 6

    # -----------------------------------------------------------------

    def check_attack(self, player):
        if self.state == "DEATH":
            return
        distance = abs(self.rect.centerx - player.rect.centerx)
        if distance <= self.ATTACK_RANGE:
            if self.state != "ATTACK":
                self.state = "ATTACK"
                self.frame_index = 0
        else:
            if self.state == "ATTACK":
                self.state = "FLYING"
                self.frame_index = 0

    def _split(self, sheet: pygame.Surface, n):
        """Corta 'n' quadros na horizontal."""
        w, h = sheet.get_size()
        fw = w // n
        return [sheet.subsurface(pygame.Rect(i * fw, 0, fw, h)) for i in range(n)]

    # -----------------------------------------------------------------
    def move(self, players=None):
        if self.state == "DEATH":
            return

        # Se receber players, verifica se deve atacar
        if players:
            atacando = False
            for p in players:
                distance = abs(self.rect.centerx - p.rect.centerx)
                if distance <= self.ATTACK_RANGE:
                    if self.state != "ATTACK":
                        self.state = "ATTACK"
                        self.frame_index = 0
                    atacando = True
                    break
            if not atacando and self.state == "ATTACK":
                self.state = "FLYING"
                self.frame_index = 0

        # Se não estiver atacando, se move horizontalmente
        if self.state != "ATTACK":
            self.rect.x += self.speed
            if self.rect.right >= LARG_TELA or self.rect.left <= 0:
                self.speed *= -1

        self.rect.bottom = CARPET_BOTTOM - 6

    # -----------------------------------------------------------------
    def get_attack_hitbox(self):
        """hit-box curto à frente, só nos quadros 2-5."""
        if self.state == "ATTACK" and 2 <= self.frame_index <= 5:
            width = self.rect.width // 2
            hb = pygame.Rect(0, 0, width, self.rect.height - 10)
            hb.center = self.rect.center
            hb.x += self.facing * width // 2
            return hb
        return None

    def take_damage(self, amt=1):
        """Causa dano e devolve True se o inimigo morreu neste golpe."""
        if self.state == "DEATH":
            return False
        self.hp -= amt
        if self.hp <= 0:
            self.state = "DEATH"
            self.frame_index = 0
            return True  # morreu agora
        else:
            self.state = "HURT"
            self.frame_index = 0
            return False

    # -----------------------------------------------------------------
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
            self.surf = self.attack_frames[min(self.frame_index,
                                               len(self.attack_frames) - 1)]

        elif self.state == "HURT":
            if self.frame_index >= len(self.hurt_frames):
                self.state = "FLYING"
                self.frame_index = 0
            self.surf = self.hurt_frames[min(self.frame_index,
                                             len(self.hurt_frames) - 1)]

        elif self.state == "DEATH":
            if self.frame_index >= len(self.death_frames):
                # mantém último frame; Level removerá após animação
                self.frame_index = len(self.death_frames) - 1
            self.surf = self.death_frames[self.frame_index]
