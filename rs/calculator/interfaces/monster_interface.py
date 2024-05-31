from typing import List, Optional

from rs.calculator.interfaces.target_interface import TargetInterface


class MonsterInterface(TargetInterface):
    damage: int
    hits: int
    is_gone: bool
    name: str


def find_lowest_hp_monster(monsters: List[MonsterInterface]) -> Optional[MonsterInterface]:
    lowest: Optional[MonsterInterface] = None
    for monster in monsters:
        if monster.is_gone or monster.current_hp <= 0:
            continue
        if lowest is None or monster.current_hp < lowest.current_hp:
            lowest = monster
    return lowest
