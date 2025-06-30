import pygame, sys
from code.Menu  import Menu
from code.Const import LARG_TELA, ALTURA_TELA, MENU_OPTION
from code.Level import Level


class Game:
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode((LARG_TELA, ALTURA_TELA))
        pygame.display.set_caption("Knight Soul")

    # ================================================================
    def run(self):
        state         = "menu"
        game_mode     = None           # modo selecionado no menu
        keep_players  = None           # jogadores vivos vindos do level 1

        while True:

            # ---------------- MENU -----------------------------------
            if state == "menu":
                menu = Menu(self.window)
                choice = menu.run()                       # string retornada

                if choice in (MENU_OPTION[0], MENU_OPTION[1]):   # 1P / coop
                    game_mode = choice
                    state = "level_1"
                elif choice == MENU_OPTION[2]:                   # competitivo
                    game_mode = choice
                    state = "level_1"
                elif choice == MENU_OPTION[3]:                   # pontuação
                    self.show_score()
                elif choice == MENU_OPTION[4]:                   # sair
                    pygame.quit(); sys.exit()
                continue

            # --------------- LEVEL 1 ---------------------------------
            if state == "level_1":
                lvl1 = Level(self.window, "Level 1", game_mode)
                result, keep_players = lvl1.run()        # tupla (str, list)

                if result == "next_level":
                    state = "level_2"                    # segue p/ fase 2
                else:                                    # morreu ou ESC
                    state = "menu"
                continue

            # --------------- LEVEL 2 ---------------------------------
            if state == "level_2":
                lvl2 = Level(self.window, "Level 2",
                             game_mode, keep_players)
                lvl2.run()                               # retorno ignorado
                state = "menu"                           # volta ao menu
                continue

    # ================================================================
    def show_score(self):
        """Tela de pontuação simples (ESC para voltar)."""
        waiting = True
        while waiting:
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    pygame.quit(); sys.exit()
                if ev.type == pygame.KEYDOWN and ev.key == pygame.K_ESCAPE:
                    waiting = False
            self.window.fill((0, 0, 100))
            pygame.display.flip()
