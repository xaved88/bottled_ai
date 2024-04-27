import os
import sys
import time
import unittest

from ai.common.co_test_handler_fixture import CoTestHandlerFixture
from rs.calculator.enums.card_id import CardId
from rs.calculator.interfaces.memory_items import MemoryItem, ResetSchedule
from rs.common.handlers.common_battle_handler import CommonBattleHandler
from rs.game.card import CardType
from rs.machine.the_bots_memory_book import TheBotsMemoryBook
from test_helpers.resources import load_resource_state


class BattleHandlerTestCase(CoTestHandlerFixture):
    handler = CommonBattleHandler

    def test_plays_bash(self):
        self.execute_handler_tests('battles/general/basic.json', ['play 5 0'])

    def test_plays_kills_opponent(self):
        self.execute_handler_tests('battles/general/choose_kill.json', ['play 1 0'])

    def test_doesnt_play_burn(self):
        state = load_resource_state('battles/general/burns.json')
        self.assertEqual(['play 2 0'], CommonBattleHandler().handle(state).commands)

    @unittest.skipUnless(os.environ.get('EXTENSIVE_TESTS'), "we only want to run this expensive test occasionally")
    def test_complex_case_does_not_timeout(self):
        start = time.perf_counter()
        state = load_resource_state('battles/general/complex_case.json')
        self.assertEqual(['play 7'], CommonBattleHandler().handle(state).commands)
        end = time.perf_counter()
        if end > start + 40:
            self.fail("Process took too long!")

    def test_another_simple_case(self):
        state = load_resource_state('battles/general/another_simple.json')
        self.assertEqual(['play 5'], CommonBattleHandler().handle(state).commands)

    def test_discard_works_correctly(self):
        self.execute_handler_tests('/battles/general/discard.json', ['choose 1', 'confirm', 'wait 30'])

    def test_discard_is_okay_with_no_cards(self):
        self.execute_handler_tests('/battles/general/discard_no_cards.json', [])

    def test_attacks_into_block_when_barricade_is_up(self):
        self.execute_handler_tests('/battles/general/attack_barricade.json', ['play 1'])

    def test_plays_powers_when_nothing_better_to_do(self):
        self.execute_handler_tests('/battles/general/play_powers.json', ['play 3'])

    def test_do_not_expect_thorns_to_kill_debuffing_enemy(self):
        self.execute_handler_tests(
            '/battles/general/manual_kill_when_enemy_not_attacking_into_thorns.json', ['play 1 0'])

    def test_do_not_block_against_non_attack_even_though_enemy_is_strong(self):
        self.execute_handler_tests('/battles/general/monster_not_attacking_but_has_strength_up.json', ['play 2 1'])

    def test_plays_slimeds_when_nothing_better_to_do(self):
        self.execute_handler_tests('/battles/general/play_slimed.json', ['play 1'])

    def test_do_not_discard_bad_ethereal_cards(self):
        self.execute_handler_tests('/battles/general/discard_hold_on_to_bad_ethereals.json',
                                   ['choose 2', 'confirm', 'wait 30'])

    def test_save_unnecessary_apparition_for_later(self):
        self.execute_handler_tests('/battles/general/save_unnecessary_apparition_for_later.json',
                                   ['choose 1', 'confirm', 'wait 30'])

    def test_avoid_shivs_in_discard_play_shiv_despite_high_block(self):
        self.execute_handler_tests('/battles/general/play_shivs_despite_high_block.json', ['play 4'])

    def test_avoid_shivs_in_discard_play_storm_of_steel_later(self):
        self.execute_handler_tests('/battles/general/play_storm_of_steel_later.json', ['play 1'])

    def test_discard_doubt(self):
        self.execute_handler_tests('/battles/general/discard_doubt_specifically.json', ['play 1'])

    def test_gremlin_nob_defensive_skill_not_worth_it(self):
        self.execute_handler_tests(
            'battles/specific_comparator_cases/gremlin_nob/gremlin_nob_defend_early.json', ['end'])

    def test_gremlin_nob_defensive_skill_worth_it(self):
        self.execute_handler_tests(
            'battles/specific_comparator_cases/gremlin_nob/gremlin_nob_defend_late.json', ['play 5'])

    def test_gremlin_nob_damaging_skill_not_worth_it(self):
        self.execute_handler_tests(
            'battles/specific_comparator_cases/gremlin_nob/gremlin_nob_cloak_and_dagger_early.json', ['end'])

    def test_gremlin_nob_indirectly_damaging_skill_not_worth_it(self):
        self.execute_handler_tests(
            'battles/specific_comparator_cases/gremlin_nob/gremlin_nob_terror_and_thousand_cuts_late.json', ['end'])

    def test_gremlin_nob_damaging_skill_worth_it(self):
        self.execute_handler_tests(
            'battles/specific_comparator_cases/gremlin_nob/gremlin_nob_cloak_and_dagger_late.json', ['play 1'])

    def test_gremlin_nob_avoid_prepared_draw_free_early(self):
        self.execute_handler_tests(
            'battles/specific_comparator_cases/gremlin_nob/gremlin_nob_prepared.json', ['play 5'])

    def test_prefer_multiple_vulnerable_over_straight_damage(self):
        self.execute_handler_tests('battles/general/terror_vs_strike.json', ['play 1 0'])

    def test_general_artifact_prio(self):
        self.execute_handler_tests('battles/general/normal_artifact_removal.json', ['play 2 1'])

    def test_big_fight_higher_prio_remove_artifacts(self):
        self.execute_handler_tests(
            'battles/specific_comparator_cases/big_fight/big_fight_prioritize_artifact_removal_over_damage.json',
            ['play 1 0'])

    def test_big_fight_higher_prio_powers(self):
        self.execute_handler_tests(
            'battles/specific_comparator_cases/big_fight/big_fight_prioritize_power_over_damage.json', ['play 1'])

    def test_some_powers_higher_prio_than_others(self):
        self.execute_handler_tests('battles/general/prioritize_accuracy_over_energized.json', ['play 2'])

    def test_three_sentries_attacks_edge_sentry_even_when_mid_is_lower_health(self):
        self.execute_handler_tests(
            'battles/specific_comparator_cases/three_sentries/sentry_low_middle_health.json', ['play 4 0'])

    def test_three_sentries_aggression_over_defense(self):
        self.execute_handler_tests(
            'battles/specific_comparator_cases/three_sentries/sentry_yolo_state_with_three.json', ['play 4 0'])

    def test_three_sentries_use_normal_comparator_priorities_when_one_dead(self):
        self.execute_handler_tests('battles/specific_comparator_cases/three_sentries/sentry_one_dead.json', ['play 6'])

    def test_do_not_attack_escaped_mugger(self):
        self.execute_handler_tests('/battles/general/escaped_mugger.json', ['play 2 1'])

    def test_waiting_lagavulin_wait_for_powers(self):
        self.execute_handler_tests(
            '/battles/specific_comparator_cases/waiting_lagavulin/waiting_lagavulin_turn_1_with_powers_in_deck.json',
            ['end'])

    def test_waiting_lagavulin_use_power(self):
        self.execute_handler_tests(
            '/battles/specific_comparator_cases/waiting_lagavulin/waiting_lagavulin_turn_1_with_powers_in_hand.json',
            ['play 4'])

    def test_waiting_lagavulin_use_terror(self):
        self.execute_handler_tests(
            '/battles/specific_comparator_cases/waiting_lagavulin/waiting_lagavulin_turn_1_with_terror_in_hand.json',
            ['play 3 0'])

    def test_waiting_lagavulin_no_powers(self):
        self.execute_handler_tests(
            '/battles/specific_comparator_cases/waiting_lagavulin/waiting_lagavulin_turn_1_without_powers.json',
            ['play 3 0'])

    def test_waiting_lagavulin_turn_4(self):
        self.execute_handler_tests(
            '/battles/specific_comparator_cases/waiting_lagavulin/waiting_lagavulin_turn_4_with_powers.json',
            ['play 3 0'])

    def test_waiting_lagavulin_event_lagavulin(self):
        self.execute_handler_tests(
            '/battles/specific_comparator_cases/waiting_lagavulin/waiting_lagavulin_event_lagavulin_with_powers.json',
            ['play 3 0'])

    def test_waiting_lagavulin_no_powers_but_relic(self):
        self.execute_handler_tests(
            '/battles/specific_comparator_cases/waiting_lagavulin/waiting_lagavulin_turn_1_without_powers_but_relic.json',
            ['end'])

    def test_playing_random_damage_is_desirable(self):
        self.execute_handler_tests('/battles/general/play_random_damage_card.json', ['play 1'])

    def test_playing_random_poison_is_desirable(self):
        self.execute_handler_tests('/battles/general/play_bouncing_flask.json', ['play 1'])

    def test_play_self_repair_when_going_to_win_and_damaged(self):
        self.execute_handler_tests('/battles/powers/winning_play_self_repair.json', ['play 2'])

    def test_do_not_play_self_repair_when_more_important_things_happening(self):
        self.execute_handler_tests('/battles/powers/self_repair_in_hand.json', ['play 4 0'])

    def test_do_not_play_self_repair_when_full(self):
        self.execute_handler_tests('/battles/powers/winning_do_not_play_self_repair.json', ['play 5 0'])

    def test_retaining_enmasse_is_desirable(self):
        self.execute_handler_tests('/battles/general/play_equilibrium.json', ['play 3'])

    def test_retaining_individual_card_is_desirable(self):
        self.execute_handler_tests('/battles/general/save_flying_sleeves.json', ['play 3'])

    # medical kit not really relevant to react to, since the state is adjusted by the game to make status cards playable
    def test_medical_kit_playing_wound_is_good(self):
        self.execute_handler_tests('/battles/general/medical_kit_wound.json', ['play 3'])

    def test_go_for_kill_with_powered_up_ritual_dagger(self):
        card_uuid = "test_uuid_powered_up_ritual_dagger"
        mb = TheBotsMemoryBook.new_default()
        reset_schedule = next(iter(mb.memory_by_card[CardId.RITUAL_DAGGER].keys()))
        mb.memory_by_card[CardId.RITUAL_DAGGER][reset_schedule] = {card_uuid: 3}
        new_mb = self.execute_handler_tests('/battles/general/powered_up_ritual_dagger.json', ['play 3 0'], mb)
        self.assertEqual(6, new_mb.memory_by_card[CardId.RITUAL_DAGGER][reset_schedule][card_uuid])

    def test_prefer_killing_with_ritual_dagger(self):
        self.execute_handler_tests('/battles/general/kill_with_ritual_dagger.json', ['play 3 0'])

    def test_memory_book_attacks_per_turn_is_updated(self):
        mb = TheBotsMemoryBook.new_default(last_known_turn=1)
        mb.memory_general[MemoryItem.ATTACKS_THIS_TURN] = 2
        new_mb = self.execute_handler_tests('/battles/general/finisher.json', ['play 4 0'], mb)
        self.assertEqual(3, new_mb.memory_general[MemoryItem.ATTACKS_THIS_TURN])

    def test_memory_book_claw_state_persists_when_a_different_card_is_played(self):
        mb = TheBotsMemoryBook.new_default()
        mb.memory_general[MemoryItem.CLAWS_THIS_BATTLE] = 1
        new_mb = self.execute_handler_tests('battles/general/basic_turn_1.json', memory_book=mb)
        self.assertEqual(1, new_mb.memory_general[MemoryItem.CLAWS_THIS_BATTLE])

    def test_memory_book_claw_state_increases_when_claw_is_played(self):
        mb = TheBotsMemoryBook.new_default()
        mb.memory_general[MemoryItem.CLAWS_THIS_BATTLE] = 1
        new_mb = self.execute_handler_tests('battles/general/claw.json', memory_book=mb)
        self.assertEqual(2, new_mb.memory_general[MemoryItem.CLAWS_THIS_BATTLE])

    def test_play_genetic_algorithm_when_nothing_better_to_do(self):
        self.execute_handler_tests('/battles/general/play_genetic_algorithm.json', ['play 1'])

    def test_ritual_dagger_saved_outside_battle(self):
        card_memory = {CardId.RITUAL_DAGGER: {ResetSchedule.GAME: {"test": 4}}}
        final_state = load_resource_state('card_reward/card_reward_take.json',
                                          memory_book=TheBotsMemoryBook(memory_by_card=card_memory))
        self.assertEqual(True, "test" in final_state.the_bots_memory_book.memory_by_card[CardId.RITUAL_DAGGER][
            ResetSchedule.GAME])

    def test_glass_knife_not_saved_outside_battle(self):
        card_memory = {CardId.GLASS_KNIFE: {ResetSchedule.BATTLE: {"test": 4}}}
        final_state = load_resource_state('card_reward/card_reward_take.json',
                                          memory_book=TheBotsMemoryBook(memory_by_card=card_memory))
        self.assertEqual(False, "test" in final_state.the_bots_memory_book.memory_by_card[CardId.GLASS_KNIFE][
            ResetSchedule.BATTLE])

    def test_avoid_playing_steam_barrier_if_not_necessary(self):
        self.execute_handler_tests('/battles/general/avoid_steam_barrier.json', ['play 2'])

    def test_play_claws_to_power_them_up(self):
        self.execute_handler_tests('/battles/general/play_claws_despite_high_block.json', ['play 4 0'])

    def test_discard_bug_case(self):
        self.execute_handler_tests('/other/broken_discard_bug.json', ['choose 1', 'confirm', 'wait 30'])

    def test_memory_book_knows_that_an_attack_was_played_last(self):
        mb = TheBotsMemoryBook.new_default()
        new_mb = self.execute_handler_tests('battles/general/attack.json', memory_book=mb)
        self.assertEqual(CardType.ATTACK, new_mb.memory_general[MemoryItem.TYPE_LAST_PLAYED])

    def test_memory_book_knows_that_a_skill_was_played_last(self):
        mb = TheBotsMemoryBook.new_default()
        new_mb = self.execute_handler_tests('battles/general/skill.json', memory_book=mb)
        self.assertEqual(CardType.SKILL, new_mb.memory_general[MemoryItem.TYPE_LAST_PLAYED])

    def test_memory_book_knows_that_some_irrelevant_type_was_played_last(self):
        mb = TheBotsMemoryBook.new_default()
        mb.memory_general[MemoryItem.TYPE_LAST_PLAYED] = CardType.ATTACK
        new_mb = self.execute_handler_tests('battles/general/power.json', memory_book=mb)
        self.assertEqual(CardType.OTHER, new_mb.memory_general[MemoryItem.TYPE_LAST_PLAYED])
