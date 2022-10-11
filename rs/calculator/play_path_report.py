from rs.calculator.hand_state import HandState
from rs.calculator.play_path import PlayPath
from rs.calculator.powers import PowerId


# this would never play bloodletting or offering? unless it helps prevent damage.
# the dude with barricade isn't considered here and prob will be weird.

class PathPlayReport:

    def __init__(self, hand_state: HandState, original_hp: int, path: PlayPath):
        self.path: PlayPath = path
        self.battle_lost: bool = hand_state.player.current_hp <= 0
        monsters_hp = [monster.current_hp for monster in hand_state.monsters if monster.current_hp > 0]
        self.battle_won: bool = not len(monsters_hp)
        self.incoming_damage: int = original_hp - hand_state.player.current_hp
        self.dead_monsters: int = len([True for monster in hand_state.monsters if monster.current_hp <= 0])
        monsters_vulnerable_hp = [monster.current_hp - min(monster.powers.get(PowerId.VULNERABLE, 0) * 5, 3)
                                  for monster in hand_state.monsters if monster.current_hp > 0]
        self.lowest_health_monster: int = 0 if self.battle_won else min(monsters_vulnerable_hp)
        self.total_monster_health: int = 0 if self.battle_won else sum(monsters_vulnerable_hp)
