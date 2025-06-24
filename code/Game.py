import pygame
import sys

from code.Menu import Menu
from code.Const import LARG_TELA, ALTURA_TELA, MENU_OPTION
from code.Level import Level


class Game:

    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode((LARG_TELA, ALTURA_TELA))
        pygame.display.set_caption("Meu Jogo 2D") # Adicionei um título para a janela

    def run(self):
        current_state = "menu" # Começamos no estado de menu
        game_mode = None # Variável para guardar o modo de jogo selecionado no menu

        while True:
            if current_state == "menu":
                # Cria e executa o menu. Ele vai retornar a opção selecionada.
                menu = Menu(self.window)
                menu_return = menu.run()

                if menu_return in [MENU_OPTION[0], MENU_OPTION[1], MENU_OPTION[2]]:
                    print(f"Iniciar jogo - Modo: {menu_return}")
                    current_state = "level_1" # Muda para o estado do nível
                    game_mode = menu_return # Salva o modo de jogo
                elif menu_return == MENU_OPTION[3]:
                    print("Exibir pontuação")
                    current_state = "score" # Exemplo de outro estado para pontuação
                elif menu_return == MENU_OPTION[4]:
                    print("Sair do jogo")
                    pygame.quit()
                    sys.exit() # Saída limpa do programa

            elif current_state == "level_1":
                # Cria e executa o nível. Ele vai rodar até terminar e retornar um resultado.
                level = Level(self.window, "Level 1", game_mode)
                level_return = level.run()

                # Ao retornar do level.run(), você pode verificar o resultado
                # Por exemplo, se level_return for "game_over" ou "level_complete"
                print(f"Nível terminou com resultado: {level_return}")
                current_state = "menu" # Por enquanto, sempre volta para o menu

            elif current_state == "score":
                # Lógica para exibir a tela de pontuação
                print("Exibindo pontuação. Pressione ESC para voltar ao menu.")
                # Implementação simples: espera por uma tecla ou um tempo
                waiting_for_input = True
                while waiting_for_input:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_ESCAPE: # Pressione ESC para voltar
                                waiting_for_input = False
                    # Você precisaria de alguma renderização aqui para a tela de score
                    self.window.fill((0, 0, 100)) # Fundo azul para a tela de score
                    # self.level_text(..., "PONTUAÇÃO AQUI", ...)
                    pygame.display.flip()

                current_state = "menu" # Volta para o menu após exibir pontuação

            # Você pode adicionar mais estados aqui (e.g., "game_over", "victory_screen")