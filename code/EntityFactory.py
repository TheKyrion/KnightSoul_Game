from code.Background import Background
from code.Const import LARG_TELA, ALTURA_TELA
from code.Player import Player, Player2


class EntityFactory:

    @staticmethod
    def get_entity(entity_name: str, position=(0, 0)):
        match entity_name:
            case 'bg1':
                list_bg = []
                for i in range(7):
                    # nomes das imagens bg10.png, bg11.png, ... bg16.png, por exemplo
                    list_bg.append(Background(f'bg1{i}', (0, 0)))
                    list_bg.append(Background(f'bg1{i}', (LARG_TELA, 0)))
                return list_bg

            case 'player':
                return Player('player', position)
            case 'player2':
                return Player2('player2', position)
