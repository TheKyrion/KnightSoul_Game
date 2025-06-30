from code.Background import Background
from code.Const import LARG_TELA
from code.Player import Player, Player2
from code.Enemy import Enemy


class EntityFactory:

    @staticmethod
    def get_entity(entity_name: str, position=(0, 0)):
        """
        entity_name pode ser:
            • 'bg1'  → fundo da fase 1
            • 'bg2'  → fundo da fase 2
            • 'player', 'player2', 'enemy'
        """
        match entity_name:

            # ---------- BACKGROUND LEVEL 1 ----------------------------
            case "bg1":
                bgs = []
                for i in range(7):  # bg10 … bg16
                    bgs.append(Background(f"bg1{i}", (0, 0)))
                    bgs.append(Background(f"bg1{i}", (LARG_TELA, 0)))
                return bgs

            # ---------- BACKGROUND LEVEL 2 ----------------------------
            case "bg2":
                bgs = []
                for i in range(6):  # bg20 … bg26
                    bgs.append(Background(f"bg2{i}", (0, 0)))
                    bgs.append(Background(f"bg2{i}", (LARG_TELA, 0)))
                return bgs

            # ---------- ENTIDADES ------------------------------------
            case "player":
                return Player("player", position)
            case "player2":
                return Player2("player2", position)
            case "enemy":
                return Enemy("enemy", position)

            # ---------- não reconhecido -------------------------------
            case _:
                raise ValueError(f"Entidade desconhecida: {entity_name}")
