from typing import Callable, List

from rs.calculator.battle_state import BattleState
from rs.calculator.enums.card_id import CardId
from rs.calculator.interfaces.comparator_interface import ComparatorInterface
from rs.calculator.enums.power_id import PowerId
from rs.calculator.powers import DEBUFFS
from rs.common.comparators.core.assessment import ComparatorAssessmentConfig
from rs.common.comparators.core.comparisons import *

Comparison = Callable[[CA, CA], Optional[bool]]

default_comparisons = [
    battle_not_lost,
    battle_is_won,
    preserve_revive_options,
    most_optimal_winning_battle,
    no_blasphemy,
    most_free_early_draw,
    most_free_draw,
    most_lasting_intangible,
    least_incoming_damage_over_1,
    most_great_player_powers,
    most_dead_monsters,
    most_tranquility,
    most_enemy_talking_to_hand,
    most_enemy_vulnerable,
    most_enemy_weak,
    least_awkward_shivs,
    killed_with_lesson_learned,
    most_powered_up_ritual_dagger,
    kept_expensive_decreasing_cost_retain_cards,
    lowest_health_monster,
    lowest_total_monster_health,
    lowest_barricaded_block,
    lowest_enemy_plated_armor,
    most_orb_slots,
    most_channeled_orbs,
    excessive_amount_of_cards_played_this_turn,
    most_draw_pay_early,
    most_draw_pay,
    most_good_player_powers,
    least_bad_player_powers,
    most_less_good_player_powers,
    least_enemy_artifacts,
    most_bad_cards_exhausted,
    most_powered_up_genetic_algorithm,
    most_cards_left_in_hand,
    least_incoming_damage,
    most_ethereal_cards_saved_for_later,
    most_powered_up_claws,
    stance_is_not_wrath,
    stance_is_calm,
    least_powered_down_steam_barrier,
    most_block_saved_for_next_turn,
    most_energy,
]

powers_we_like: List[PowerId] = [
    PowerId.ACCURACY,
    PowerId.AFTER_IMAGE,
    PowerId.BATTLE_HYMN,
    PowerId.BARRICADE,
    PowerId.BERSERK,
    PowerId.BLUR,
    PowerId.BUFFER,
    PowerId.COLLECT,
    PowerId.CORRUPTION,
    PowerId.DARK_EMBRACE,
    PowerId.DEMON_FORM,
    PowerId.DEVA,
    PowerId.DEVOTION,
    PowerId.ECHO_FORM,
    PowerId.ELECTRO,
    PowerId.ENVENOM,
    PowerId.ESTABLISHMENT,
    PowerId.EVOLVE,
    PowerId.FAKE_ALPHA_BETA,
    PowerId.FEEL_NO_PAIN,
    PowerId.FIRE_BREATHING,
    PowerId.FOCUS,
    PowerId.FORESIGHT,
    PowerId.HEATSINK,
    PowerId.INFINITE_BLADES,
    PowerId.INTANGIBLE_PLAYER,
    PowerId.JUGGERNAUT,
    PowerId.LIKE_WATER,
    PowerId.LOOP,
    PowerId.MACHINE_LEARNING,
    PowerId.MANTRA_INTERNAL,
    PowerId.MASTER_REALITY,
    PowerId.MAYHEM,
    PowerId.MENTAL_FORTRESS,
    PowerId.METALLICIZE,
    PowerId.NIRVANA,
    PowerId.NOXIOUS_FUMES,
    PowerId.OMEGA,
    PowerId.PANACHE_INTERNAL,
    PowerId.PHANTASMAL,
    PowerId.PLATED_ARMOR,
    PowerId.REPAIR,
    PowerId.RUSHDOWN,
    PowerId.SADISTIC,
    PowerId.SIMMERING_RAGE,
    PowerId.STUDY,
    PowerId.THORNS,
    PowerId.THOUSAND_CUTS,
    PowerId.TOOLS_OF_THE_TRADE,
]

powers_we_like_less: List[PowerId] = [
    PowerId.ARTIFACT,
    PowerId.DEXTERITY,
    PowerId.ENERGIZED,
    PowerId.FREE_ATTACK_POWER,
    PowerId.STRENGTH,
    PowerId.VIGOR,
]

cards_that_exit_wrath: List[CardId] = [
    CardId.EMPTY_BODY,
    CardId.EMPTY_FIST,
    CardId.EMPTY_MIND,
    CardId.FEAR_NO_EVIL,
    CardId.INNER_PEACE,
    CardId.TRANQUILITY,
    CardId.VIGILANCE,
]

powers_we_dislike: List[PowerId] = DEBUFFS.copy()


def add_to_comparison_list(comparisons: List[Comparison], comparison_to_add: Comparison, after: Comparison):
    index = comparisons.index(after) + 1
    comparisons.insert(index, comparison_to_add)


def move_in_comparison_list(comparisons: List[Comparison], comparison_to_move: Comparison, after: Comparison):
    comparisons.remove(comparison_to_move)
    add_to_comparison_list(comparisons, comparison_to_move, after)


class CommonGeneralComparator(ComparatorInterface):

    def __init__(self, comparisons: List[Comparison] = None, assessment_config: ComparatorAssessmentConfig = None):
        self.comparisons: List[Comparison] = default_comparisons if comparisons is None else comparisons
        self.assessment_config: ComparatorAssessmentConfig = \
            ComparatorAssessmentConfig(powers_we_like, powers_we_like_less, powers_we_dislike,
                                       cards_that_exit_wrath=cards_that_exit_wrath) \
                if assessment_config is None else assessment_config

    def does_challenger_defeat_the_best(self, best_state: BattleState, challenger_state: BattleState,
                                        original: BattleState) -> bool:
        best = CA(best_state, original, self.assessment_config)
        challenger = CA(challenger_state, original, self.assessment_config)

        for c in self.comparisons:
            v = c(best, challenger)
            if v is not None:
                del best
                del challenger
                return v
        del best
        del challenger
        return False
