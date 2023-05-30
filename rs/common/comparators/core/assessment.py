from typing import Callable, TypeVar, List

from rs.calculator.battle_state import BattleState
from rs.calculator.enums.card_id import CardId
from rs.calculator.enums.power_id import PowerId
from rs.calculator.enums.relic_id import RelicId

T = TypeVar('T')


class ComparatorAssessment:
    def __init__(self, state: BattleState, original: BattleState):
        self.state: BattleState = state
        self.original: BattleState = original
        self.cached_values: dict[str, any] = {}

    def __get_value(self, name: str, load_function: Callable[[], T]) -> T:
        if self.cached_values.get(name) is None:
            self.cached_values[name] = load_function()
        return self.cached_values.get(name)

    def battle_won(self) -> bool:
        return self.__get_value('bw', lambda: not [True for m in self.state.monsters if m.current_hp > 0])

    def battle_lost(self) -> bool:
        return self.__get_value('bl', lambda: self.state.player.current_hp > 0)

    def incoming_damage(self) -> int:
        return self.__get_value('id', lambda: self.original.player.current_hp - self.state.player.current_hp)

    def dead_monsters(self) -> int:
        return self.__get_value('dm', lambda: len([True for monster in self.state.monsters if monster.current_hp <= 0]))

    def monsters_vulnerable_hp(self) -> List[int]:
        return self.__get_value('mvhp',
                                lambda: [monster.current_hp - min(monster.powers.get(PowerId.VULNERABLE, 0) * 5, 3) for
                                         monster in self.state.monsters if monster.current_hp > 0])

    def lowest_health_monster(self) -> int:
        return self.__get_value('lhm', lambda: 0 if self.battle_won() else min(self.monsters_vulnerable_hp()))

    def total_monster_health(self) -> int:
        return self.__get_value('tmh', lambda: 0 if self.battle_won() else sum(self.monsters_vulnerable_hp()))

    def draw_free_early(self) -> int:
        return self.__get_value('dfe', lambda: len([True for c in self.state.hand if c.id == CardId.DRAW_FREE_EARLY]))

    def draw_free(self) -> int:
        return self.__get_value('df', lambda: len(
            [True for c in self.state.hand if c.id == CardId.DRAW_FREE or c.id == CardId.DRAW_FREE_EARLY]))

    def draw_pay_early(self) -> int:
        return self.__get_value('dpe', lambda: len([True for c in self.state.hand if c.id == CardId.DRAW_PAY_EARLY]))

    def draw_pay(self) -> int:
        return self.__get_value('dp', lambda: len(
            [True for c in self.state.hand if c.id == CardId.DRAW_PAY or c.id == CardId.DRAW_PAY_EARLY]))

    def energy(self) -> int:
        return self.__get_value('e', lambda: self.state.player.energy)

    def intangible(self) -> int:
        return self.__get_value('i', lambda: self.state.player.powers.get(PowerId.INTANGIBLE_PLAYER, 0))

    def enemy_vulnerable(self) -> int:
        return self.__get_value('ev',
                                lambda: min(max([m.powers.get(PowerId.VULNERABLE, 0) for m in self.state.monsters]), 4))

    def enemy_weak(self) -> int:
        return self.__get_value('ew',
                                lambda: min(max([m.powers.get(PowerId.WEAKENED, 0) for m in self.state.monsters]), 4))

    def player_max_hp(self) -> int:
        return self.__get_value('pmhp', lambda: self.state.player.max_hp)

    def pen_nib_counter(self) -> int:
        return self.__get_value('penc', lambda: self.state.player.relics.get(RelicId.PEN_NIB, -1))

    def nunchaku_counter(self) -> int:
        return self.__get_value('nunc', lambda: self.state.player.relics.get(RelicId.NUNCHAKU, -1))
