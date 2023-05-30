from typing import Callable, TypeVar, List

from rs.calculator.battle_state import BattleState
from rs.calculator.enums.card_id import CardId
from rs.calculator.enums.power_id import PowerId
from rs.calculator.enums.relic_id import RelicId
from rs.calculator.powers import get_power_count
from rs.game.card import CardType

T = TypeVar('T')


class ComparatorAssessmentConfig:
    def __init__(self, powers_we_like: List[PowerId], powers_we_like_less: List[PowerId],
                 powers_we_dislike: List[PowerId]):
        self.powers_we_like: List[PowerId] = powers_we_like
        self.powers_we_like_less: List[PowerId] = powers_we_like_less
        self.powers_we_dislike: List[PowerId] = powers_we_dislike


class ComparatorAssessment:
    def __init__(self, state: BattleState, original: BattleState, config: ComparatorAssessmentConfig):
        self.state: BattleState = state
        self.original: BattleState = original
        self.cached_values: dict[str, any] = {}
        self.config: ComparatorAssessmentConfig = config

    def __get_value(self, name: str, load_function: Callable[[], T]) -> T:
        if self.cached_values.get(name) is None:
            self.cached_values[name] = load_function()
        return self.cached_values.get(name)

    def battle_won(self) -> bool:
        return self.__get_value('bw', lambda: not [True for m in self.state.monsters if m.current_hp > 0])

    def battle_lost(self) -> bool:
        return self.__get_value('bl', lambda: self.state.player.current_hp <= 0)

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

    def lowest_true_health_monster(self) -> int:
        return self.__get_value('lowest_true_health_monster', lambda:
        0 if self.battle_won() else min([m.current_hp for m in self.state.monsters]))

    # for finding the lowest health monster either at the front or back (basically only for sentries
    def lowest_health_edge_monster(self) -> int:
        return self.__get_value('lowest_health_edge_monster', lambda:
        0 if self.battle_won() else min(self.monsters_vulnerable_hp()[0], self.monsters_vulnerable_hp()[-1]))

    def total_monster_health(self) -> int:
        return self.__get_value('tmh', lambda:
        0 if self.battle_won() else sum(self.monsters_vulnerable_hp()) -
                                    self.state.total_random_damage_dealt - self.state.total_random_poison_added)

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

    def ink_bottle_counter(self) -> int:
        return self.__get_value('ink_bottle_counter', lambda: self.state.player.relics.get(RelicId.INK_BOTTLE, -1))

    def player_powers_good(self) -> int:
        return self.__get_value('player_powers_good',
                                lambda: get_power_count(self.state.player.powers, self.config.powers_we_like))

    def player_powers_less_good(self) -> int:
        return self.__get_value('powers_less_good',
                                lambda: get_power_count(self.state.player.powers, self.config.powers_we_like_less))

    def player_powers_bad(self) -> int:
        return self.__get_value('player_powers_bad',
                                lambda: get_power_count(self.state.player.powers, self.config.powers_we_dislike))

    def bad_cards_exhausted(self) -> int:
        return self.__get_value('bad_cards_exhausted', lambda: len(
            [True for c in self.state.exhaust_pile if c.type == CardType.CURSE or c.type == CardType.STATUS]))

    def saved_for_later(self) -> int:
        return self.__get_value('saved_for_later', lambda: len([True for c in self.state.discard_pile if c.ethereal
                                                                and c.type != CardType.CURSE
                                                                and c.type != CardType.STATUS]))

    def awkward_shivs(self) -> int:
        return self.__get_value('awkward_shivs',
                                lambda: len([True for c in self.state.hand if c.id == CardId.SHIV]) + len(
                                    [True for c in self.state.discard_pile if c.id == CardId.SHIV]))

    def enemy_artifacts(self) -> int:
        return self.__get_value('enemy_artifacts',
                                lambda: sum([m.powers.get(PowerId.ARTIFACT, 0) for m in self.state.monsters]))

    def barricaded_block(self) -> int:
        return self.__get_value('enemy_artifacts', lambda: sum(
            [m.block for m in self.state.monsters if m.powers.get(PowerId.BARRICADE, 0) != 0]))

    def nob_adjusted_scaling_damage(self) -> int:
        return self.__get_value('nob_adjusted_incoming_damage', self.__nob_adjusted_incoming_damage)

    def __nob_adjusted_incoming_damage(self) -> int:
        anger_strength_up = sum([m.powers.get(PowerId.STRENGTH, 0) for m in self.state.monsters if
                                 m.powers.get(PowerId.ANGER_NOB, 0)])  # Probably going too high!!
        gremlin_nob_hp = sum([m.current_hp for m in self.state.monsters if m.powers.get(PowerId.ANGER_NOB, 0)])
        return self.original.player.current_hp - self.state.player.current_hp + (
                    int(gremlin_nob_hp / 15) * anger_strength_up)
