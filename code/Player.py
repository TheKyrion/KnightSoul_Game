import pygame
from code.Const import ALTURA_TELA
from code.Entity import Entity


class Player(Entity):

    def __init__(self, name: str, position: tuple):
        super().__init__(name, position)
        sprite_sheet_idle = pygame.image.load('./assets/idle.png').convert_alpha()
        sprite_sheet_run = pygame.image.load('./assets/idle9.png').convert_alpha()

        # Configurações da spritesheet idle
        sheet_width_idle, sheet_height_idle = sprite_sheet_idle.get_size()
        num_idle_frames = 8 # Verifique se são realmente 9 frames!
        frame_width_idle = sheet_width_idle // num_idle_frames
        frame_height_idle = sheet_height_idle

        self.idle_frames = []
        for i in range(num_idle_frames):
            rect = pygame.Rect(i * frame_width_idle, 0, frame_width_idle, frame_height_idle)
            self.idle_frames.append(sprite_sheet_idle.subsurface(rect))

        # Configurações da spritesheet run
        sheet_width_run, sheet_height_run = sprite_sheet_run.get_size()
        num_run_frames = 8 # Verifique se são realmente 9 frames!
        frame_width_run = sheet_width_run // num_run_frames
        frame_height_run = sheet_height_run

        self.run_frames = []
        for i in range(num_run_frames):
            rect = pygame.Rect(i * frame_width_run, 0, frame_width_run, frame_height_run)
            self.run_frames.append(sprite_sheet_run.subsurface(rect))

        # Inicialização de atributos
        self.frame_index = 0
        self.animation_delay = 100 # Tempo em ms para mudar de frame
        self.last_update = pygame.time.get_ticks()

        self.state = 'idle' # Estado inicial
        self.speed_y = 5
        self.name = name

        # Define a imagem inicial e a posição
        self.surf = self.idle_frames[self.frame_index]
        self.rect = self.surf.get_rect()
        self.rect.topleft = position

    def update(self):
        # Sempre atualiza a imagem com base no estado atual
        if self.state == 'idle':
            # Se estiver idle, exibe apenas a primeira frame da animação idle
            self.surf = self.idle_frames[0] # <--- MUDANÇA AQUI: Sempre frame 0 para idle
            # Não avança o frame_index para idle
        elif self.state == 'run':
            current_time = pygame.time.get_ticks()
            if current_time - self.last_update > self.animation_delay:
                self.last_update = current_time
                # Avança o frame_index apenas para o estado 'run'
                self.frame_index = (self.frame_index + 1) % len(self.run_frames) # Use len() para ser mais robusto
                self.surf = self.run_frames[self.frame_index]

    def move(self):
        keys = pygame.key.get_pressed()

        # Guarda o estado anterior para checar se houve mudança
        prev_state = self.state

        # Movimento vertical com limites (mantido como está)
        if keys[pygame.K_UP]:
            self.rect.y = max(0, self.rect.y - self.speed_y)
        if keys[pygame.K_DOWN]:
            self.rect.y = min(ALTURA_TELA - self.rect.height, self.rect.y + self.speed_y)

        # Alterna o estado com base nas teclas horizontais
        # E só muda para 'run' se uma tecla de movimento horizontal estiver pressionada
        # E se o player não estiver se movendo horizontalmente, define para 'idle'
        if keys[pygame.K_RIGHT] or keys[pygame.K_LEFT]:
            self.state = 'run'
        else:
            self.state = 'idle'

        # Opcional: Resetar o frame_index se o estado mudou de 'run' para 'idle'
        if prev_state == 'run' and self.state == 'idle':
            self.frame_index = 0 # Reinicia a animação ao parar de correr