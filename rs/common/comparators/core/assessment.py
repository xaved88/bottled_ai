from typing import Callable, TypeVar, List

from rs.calculator.battle_state import BattleState
from rs.calculator.enums.card_id import CardId
from rs.calculator.enums.potion_id import PotionId
from rs.calculator.enums.power_id import PowerId
from rs.calculator.enums.relic_id import RelicId
from rs.calculator.interfaces.memory_items import ResetSchedule, MemoryItem, StanceType
from rs.calculator.powers import get_power_count
from rs.game.card import CardType

T = TypeVar('T')


class ComparatorAssessmentConfig:
    def __init__(self, powers_we_like: List[PowerId], powers_we_like_less: List[PowerId],
                 powers_we_dislike: List[PowerId], powers_we_love: List[PowerId] = None,
                 cards_that_exit_wrath: List[CardId] = None):
        self.powers_we_love: List[PowerId] = [] if powers_we_love is None else powers_we_love
        self.powers_we_like: List[PowerId] = powers_we_like
        self.powers_we_like_less: List[PowerId] = powers_we_like_less
        self.powers_we_dislike: List[PowerId] = powers_we_dislike
        self.cards_that_exit_wrath: List[CardId] = [] if cards_that_exit_wrath is None else cards_that_exit_wrath


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
        alive_monsters = False
        unawakened_present = False
        for mon in self.state.monsters:
            if mon.current_hp > 0:
                alive_monsters = True
            if mon.powers.get(PowerId.UNAWAKENED, 0):
                unawakened_present = True
        return self.__get_value('bw', lambda: not alive_monsters and not unawakened_present)

    def battle_lost(self) -> bool:
        return self.__get_value('bl', lambda: self.state.player.current_hp <= 0)

    def incoming_damage(self) -> int:
        return self.__get_value('id', lambda: self.original.player.current_hp - self.state.player.current_hp)

    def dead_monsters(self) -> int:
        return self.__get_value('dm', lambda: len([True for monster in self.state.monsters if monster.current_hp <= 0]))

    def dead_edge_monsters(self) -> int:
        return self.__get_value('dem', lambda:
        0 if self.battle_won() else self.state.monsters[0].current_hp <= 0 or self.state.monsters[2].current_hp <= 0)

    def monsters_vulnerable_hp(self) -> List[int]:
        return self.__get_value('mvhp',
                                lambda: [monster.current_hp - min(monster.powers.get(PowerId.VULNERABLE, 0) * 5, 3) for
                                         monster in self.state.monsters if monster.current_hp > 0] or [0])

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
        0 if self.battle_won() else sum(
            self.monsters_vulnerable_hp()) - self.state.total_random_damage_dealt - self.state.total_random_poison_added)

    def total_monster_health_percent(self) -> float:
        return self.__get_value('total_monster_health_percent', lambda: 0 if self.battle_won()
        else float(sum([m.current_hp for m in self.state.monsters])) / float(
            sum([m.max_hp for m in self.state.monsters])))

    def draw_free_early(self) -> int:
        return self.__get_value('dfe', lambda: self.state.draw_free_early)

    def draw_free(self) -> int:
        return self.__get_value('df', lambda: self.state.draw_free + self.state.draw_free_early)

    def draw_pay_early(self) -> int:
        return self.__get_value('dpe', lambda: self.state.draw_pay_early)

    def draw_pay(self) -> int:
        return self.__get_value('dp', lambda: self.state.draw_pay + self.state.draw_pay_early)

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

    def enemy_talking_to_hand(self) -> int:
        return self.__get_value('eh',
                                lambda: min(max([m.powers.get(PowerId.BLOCK_RETURN, 0) for m in self.state.monsters]),
                                            10))

    def player_max_hp(self) -> int:
        return self.__get_value('pmhp', lambda: self.state.player.max_hp)

    def pen_nib_counter(self) -> int:
        return self.__get_value('penc', lambda: self.state.player.relics.get(RelicId.PEN_NIB, -1))

    def nunchaku_counter(self) -> int:
        return self.__get_value('nunc', lambda: self.state.player.relics.get(RelicId.NUNCHAKU, -1))

    def ink_bottle_counter(self) -> int:
        return self.__get_value('ink_bottle_counter', lambda: self.state.player.relics.get(RelicId.INK_BOTTLE, -1))

    def player_powers_great(self) -> int:
        return self.__get_value('player_powers_great',
                                lambda: get_power_count(self.state.player.powers, self.config.powers_we_love))

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

    def ethereal_saved_for_later(self) -> int:
        return self.__get_value('ethereal_saved_for_later',
                                lambda: len([True for c in self.state.discard_pile if c.ethereal
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
        return self.__get_value('barricaded_block', lambda: sum(
            [m.block for m in self.state.monsters if m.powers.get(PowerId.BARRICADE, 0) != 0]))

    def nob_adjusted_scaling_damage(self) -> int:
        return self.__get_value('nob_adjusted_incoming_damage', self.__nob_adjusted_incoming_damage)

    def __nob_adjusted_incoming_damage(self) -> int:
        anger_strength_up = sum([m.powers.get(PowerId.STRENGTH, 0) for m in self.state.monsters if
                                 m.powers.get(PowerId.ANGER_NOB, 0)])  # Probably going too high!!
        gremlin_nob_hp = sum([m.current_hp for m in self.state.monsters if m.powers.get(PowerId.ANGER_NOB, 0)])
        return self.original.player.current_hp - self.state.player.current_hp + (
                int(gremlin_nob_hp / 15) * anger_strength_up)

    def orb_slot_count(self) -> int:
        return self.__get_value('orb_slots', lambda: self.state.orb_slots)

    def channeled_orb_count(self) -> int:
        return self.__get_value('orb_count', lambda: len(self.state.orbs))

    def player_bias(self) -> int:
        return self.__get_value('player_bias', lambda: self.state.player.powers.get(PowerId.BIAS, 0))

    def repair_count(self) -> int:
        missing_hp = self.state.player.max_hp - self.state.player.current_hp
        if missing_hp >= 1:
            return self.__get_value('repair_count', lambda: self.state.player.powers.get(PowerId.REPAIR, 0))
        return 0

    def cards_left_in_hand(self) -> int:
        return self.__get_value('cards_left_in_hand', lambda: len(self.state.hand))

    def power_up_ritual_dagger(self) -> int:
        return self.__get_value('power_up_ritual_dagger',
                                lambda: sum(
                                    self.state.memory_by_card[CardId.RITUAL_DAGGER][ResetSchedule.GAME].values()))

    def power_up_genetic_algorithm(self) -> int:
        return self.__get_value('power_up_genetic_algorithm',
                                lambda: sum(
                                    self.state.memory_by_card[CardId.GENETIC_ALGORITHM][ResetSchedule.GAME].values()))

    def power_down_steam_barrier(self) -> int:
        return self.__get_value('power_down_steam_barrier',
                                lambda: sum(
                                    self.state.memory_by_card[CardId.STEAM_BARRIER][ResetSchedule.BATTLE].values()))

    def powered_up_claws(self) -> int:
        return self.__get_value('powered_up_claws',
                                lambda: self.state.memory_general[MemoryItem.CLAWS_THIS_BATTLE])

    def enemy_plated_armor(self) -> int:
        return self.__get_value('enemy_plated_armor', lambda: sum(
            [m.powers.get(PowerId.PLATED_ARMOR, 0) for m in self.state.monsters if
             m.powers.get(PowerId.PLATED_ARMOR, 0) != 0]))

    def stance_is_calm(self) -> int:
        return self.__get_value('stance_is_calm',
                                lambda: 1 if self.state.memory_general[MemoryItem.STANCE] == StanceType.CALM else 0)

    def stance_is_not_wrath(self) -> int:
        exit_plan = False
        for c in self.state.hand:
            if c.id in self.config.cards_that_exit_wrath:
                exit_plan = True
        return self.__get_value('stance_is_not_wrath',
                                lambda: 1 if self.state.memory_general[
                                                 MemoryItem.STANCE] == StanceType.WRATH and not exit_plan else 0)

    def played_blasphemy(self) -> int:
        return self.__get_value('we_played_blasphemy_without_permission',
                                lambda: 1 if self.state.player.powers.get(PowerId.BLASPHEMER, 0) else 0)

    def most_kills_with_lesson_learned(self) -> int:
        return self.__get_value('most_kills_with_lesson_learned',
                                lambda: self.state.memory_general[MemoryItem.KILLED_WITH_LESSON_LEARNED])

    def count_tranquility(self) -> int:
        return self.__get_value('tinh',
                                lambda: len([True for c in self.state.hand if (c.id == CardId.TRANQUILITY)]))

    def count_crescendo(self) -> int:
        return self.__get_value('cinh',
                                lambda: len([True for c in self.state.hand if (c.id == CardId.CRESCENDO)]))

    def block_for_next_turn(self) -> int:
        return self.__get_value('bfnt', lambda: self.state.saved_block_for_next_turn)

    def count_expensive_cheapening_retain_cards(self) -> int:
        return self.__get_value('cdst',
                                lambda: len(
                                    [True for c in self.state.hand if (c.id == CardId.SANDS_OF_TIME and c.cost > 0)]))
        # this will behave like >1 since we know it'll reduce by 1 when retaining

    def inconvenient_time_warp_count(self) -> int:
        bad_time_warp = False
        for m in self.state.monsters:
            if PowerId.TIME_WARP in m.powers:
                if m.powers[PowerId.TIME_WARP] == 10 or \
                        m.powers[PowerId.TIME_WARP] == 11:
                    bad_time_warp = True

        return self.__get_value('nitwc', lambda: bad_time_warp)

    def revive_option_count(self) -> int:
        fairy_count = 0
        lizard_count = 0

        if PotionId.FAIRY_IN_A_BOTTLE in self.state.potions:
            for p in self.state.potions:
                if p == PotionId.FAIRY_IN_A_BOTTLE:
                    fairy_count += 1
        if self.state.relics.get(RelicId.LIZARD_TAIL):
            if self.state.relics[RelicId.LIZARD_TAIL] != -2:
                lizard_count += 1

        return self.__get_value('roc', lambda: fairy_count + lizard_count)

    def spear_lowest_health(self) -> int:
        return self.__get_value('slh', lambda: self.monsters_vulnerable_hp()[-1])

    def excessive_amount_of_cards_played_this_turn(self) -> int:
        return self.__get_value('ctt', lambda: max(self.state.memory_general[MemoryItem.CARDS_THIS_TURN], 50))
