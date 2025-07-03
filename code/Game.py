import json, pathlib, sys, pygame
from   code.Menu   import Menu
from   code.Const  import LARG_TELA, ALTURA_TELA, MENU_OPTION
from   code.Level  import Level

SCORES_FILE = pathlib.Path("scores.json")     # ← arquivo de score

class Game:
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode((LARG_TELA, ALTURA_TELA))
        pygame.display.set_caption("Knight Soul")

    # ================================================================
    def run(self):
        state        = "menu"
        game_mode    = None
        keep_players = None         # lista reutilizada pelo Level 2

        while True:

            # ------------- MENU --------------------------------------
            if state == "menu":
                choice = Menu(self.window).run()

                if choice in (MENU_OPTION[0], MENU_OPTION[1], MENU_OPTION[2]):
                    game_mode = choice
                    state = "level_1"

                elif choice == MENU_OPTION[3]:            # PONTUAÇÃO
                    self.show_score()                     # bloqueante
                    state = "menu"

                elif choice == MENU_OPTION[4]:            # SAIR
                    pygame.quit(); sys.exit()

                continue

            # ------------- LEVEL 1 -----------------------------------
            if state == "level_1":
                lvl1 = Level(self.window, "Level 1", game_mode)
                result, keep_players = lvl1.run()         # ("next_level", list)
                state = "level_2" if result == "next_level" else "menu"
                continue

            # ------------- LEVEL 2 -----------------------------------
            if state == "level_2":
                lvl2 = Level(self.window, "Level 2", game_mode, keep_players)
                lvl2.run()                                # encerra em 20 s
                self.save_scores(keep_players)            # grava placar
                state = "menu"
                continue

    # ================================================================
    #  GRAVAR  SCORES  ------------------------------------------------
    def save_scores(self, players):
        """Adiciona a pontuação de cada jogador ao scores.json."""
        try:
            scores = json.loads(SCORES_FILE.read_text(encoding="utf-8"))
        except (FileNotFoundError, json.JSONDecodeError):
            scores = []

        for idx, pl in enumerate(players, 1):
            scores.append({"name": f"P{idx}", "score": pl.score})

        SCORES_FILE.write_text(json.dumps(scores, indent=2),
                               encoding="utf-8")

    # ================================================================
    #  TELA DE SCORE --------------------------------------------------
    def show_score(self):
        try:
            scores = json.loads(SCORES_FILE.read_text(encoding="utf-8"))
        except (FileNotFoundError, json.JSONDecodeError):
            scores = []

        scores.sort(key=lambda s: s["score"], reverse=True)
        top10 = scores[:10]

        font_big  = pygame.font.SysFont("Lucida Sans Typewriter", 28)
        font_small = pygame.font.SysFont("Lucida Sans Typewriter", 22)

        waiting = True
        while waiting:
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    pygame.quit(); sys.exit()
                if ev.type == pygame.KEYDOWN and ev.key == pygame.K_ESCAPE:
                    waiting = False

            try:
                bg = pygame.image.load("./assets/Battleground4.png").convert()
                self.window.blit(bg, (0, 0))
            except pygame.error:
                self.window.fill((0, 0, 70))  # fallback caso a imagem não exista

            title = font_big.render("★  HIGH SCORES  ★", True, (255,255,0))
            self.window.blit(title, (LARG_TELA//2 - title.get_width()//2, 40))

            y = 110
            if not top10:
                no_data = font_small.render("Sem pontuações ainda!", True, (255,255,255))
                self.window.blit(no_data, (LARG_TELA//2 - no_data.get_width()//2, y))
            else:
                for rank, entry in enumerate(top10, 1):
                    line = f"{rank:2d}. {entry['name']} – {entry['score']:4d}"
                    txt  = font_small.render(line, True, (255,255,255))
                    self.window.blit(txt, (LARG_TELA//2 - txt.get_width()//2, y))
                    y += 30

            hint = font_small.render("ESC para voltar", True, (200,200,200))
            self.window.blit(hint, (LARG_TELA//2 - hint.get_width()//2, ALTURA_TELA-50))

            pygame.display.flip()
