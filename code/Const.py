# code/Const.py

LARG_TELA = 890
ALTURA_TELA = 500
VOLUME = 0.03
CARPET_TOP = 260
CARPET_BOTTOM = 450

PLAYER_ANCHOR_X = LARG_TELA // 2

# Cores
COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0,0,0)
MENU_SELECT = (255, 255, 0) # Adicione esta linha! (Exemplo: Amarelo)

# Opções do Menu
MENU_OPTION = ("NOVO JOGO 1P",
               "NOVO JOGO 2P - COOPERATIVO",
               "NOVO JOGO 2P - COMPETITIVO",
               "PONTUAÇÃO",
               "SAIR")



ENTITY_SPEED = {
    # ---------- fundo Level 1 ----------
    'bg10': 0,
    'bg11': 1,
    'bg12': 2,
    'bg13': 3,
    'bg14': 4,
    'bg15': 5,
    'bg16': 6,

    # ---------- fundo Level 2 ----------
    'bg20': 0,     # camada mais distante
    'bg21': 1,
    'bg22': 2,
    'bg23': 3,
    'bg24': 4,
    'bg25': 5,
    'bg26': 6      # camada mais próxima
}
