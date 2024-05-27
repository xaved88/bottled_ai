from rs.calculator.interfaces.player import PlayerInterface
from rs.calculator.interfaces.potions import Potions
from rs.calculator.interfaces.powers import Powers
from rs.calculator.interfaces.relics import Relics
from rs.calculator.targets import Target


class Player(Target, PlayerInterface):

    def __init__(self, is_player: bool, current_hp: int, max_hp: int, block: int, powers: Powers, energy: int,
                 relics: Relics, potions: Potions):
        super().__init__(is_player, current_hp, max_hp, block, powers, relics, potions)
        self.energy: int = energy

    def get_state_string(self) -> str:
        return super().get_state_string() + str(self.energy) + ","
