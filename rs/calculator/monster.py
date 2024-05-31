from rs.calculator.interfaces.monster_interface import MonsterInterface
from rs.calculator.interfaces.powers import Powers
from rs.calculator.targets import Target


class Monster(Target, MonsterInterface):

    def __init__(self, is_player: bool, current_hp: int, max_hp: int, block: int, powers: Powers, damage: int = 0,
                 hits: int = 0, is_gone: bool = False, name: str = None):
        super().__init__(is_player, current_hp, max_hp, block, powers)
        self.damage: int = damage
        self.hits: int = hits
        self.is_gone: bool = is_gone
        self.name: str = name

    def get_state_string(self) -> str:
        return super().get_state_string() + f"{self.damage},{self.hits},"
