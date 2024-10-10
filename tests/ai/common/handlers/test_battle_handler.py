import os
import sys
import time
import unittest

from ai.common.co_test_handler_fixture import CoTestHandlerFixture
from rs.calculator.enums.card_id import CardId
from rs.calculator.interfaces.memory_items import MemoryItem, ResetSchedule, StanceType
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
        self.execute_handler_tests('battles/general/burns.json', ['play 2 0'])

    @unittest.skipUnless(os.environ.get('EXTENSIVE_TESTS'), "we only want to run this expensive test occasionally")
    def test_complex_case_does_not_timeout(self):
        start = time.perf_counter()
        self.execute_handler_tests('battles/general/complex_case.json', ['play 7'])
        end = time.perf_counter()
        if end > start + 40:
            self.fail("Process took too long!")

    def test_another_simple_case(self):
        self.execute_handler_tests('battles/general/another_simple.json', ['play 5'])

    def test_discard_works_correctly(self):
        self.execute_handler_tests('/battles/general/discard.json', ['choose 1', 'confirm', 'wait 30'])

    def test_discard_is_okay_with_no_cards(self):
        self.execute_handler_tests('/battles/general/discard_no_cards.json', [])

    def test_exhaust_screen_is_handled(self):
        self.execute_handler_tests('/battles/exhaust/exhaust_a_card.json', ['choose 1', 'confirm', 'wait 30'])

    def test_exhaust_screen_is_okay_with_no_cards(self):
        self.execute_handler_tests('/battles/exhaust/exhaust_no_cards.json', [])

    def test_exhaust_prefer_to_exhaust_curse(self):
        self.execute_handler_tests('/battles/exhaust/exhaust_the_curse.json', ['choose 2', 'confirm', 'wait 30'])

    def test_attacks_into_block_when_barricade_is_up(self):
        self.execute_handler_tests('/battles/general/attack_barricade.json', ['play 1'])

    def test_plays_powers_when_nothing_better_to_do(self):
        self.execute_handler_tests('/battles/general/play_powers.json', ['play 3'])

    def test_do_not_expect_thorns_to_kill_debuffing_enemy(self):
        self.execute_handler_tests(
            '/battles/general/manual_kill_when_enemy_not_attacking_into_thorns.json', ['play 1 0'])

    def test_attack_to_kill_even_though_thorns_kills(self):
        self.execute_handler_tests(
            '/battles/powers/play_around_us_dying_if_we_kill_with_thorns_here.json', ['play 1 0'])

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

    def test_play_survivor_to_be_able_to_discard_doubt(self):
        self.execute_handler_tests('/battles/general/play_survivor_to_discard_doubt_specifically.json', ['play 1'])

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

    def test_three_sentries_turn_1_can_kill(self):
        self.execute_handler_tests('battles/specific_comparator_cases/three_sentries/sentry_turn_1_can_kill.json',
                                   ['play 1 1'])

    def test_three_sentries_kill_edge_over_middle(self):
        mb = TheBotsMemoryBook.new_default()
        mb.memory_general[MemoryItem.STANCE] = StanceType.WRATH
        self.execute_handler_tests('battles/specific_comparator_cases/three_sentries/sentry_kill_edge_over_middle.json',
                                   ['play 1 0'], memory_book=mb)

    def test_do_not_attack_escaped_mugger(self):
        self.execute_handler_tests('/battles/general/escaped_mugger.json', ['play 2 1'])

    def test_waiting_lagavulin_wait_for_powers(self):
        self.execute_handler_tests(
            '/battles/specific_comparator_cases/waiting_lagavulin/waiting_lagavulin_turn_1_with_powers_in_deck.json',
            ['end'])

    def test_waiting_lagavulin_use_power(self):
        self.execute_handler_tests(
            '/battles/specific_comparator_cases/waiting_lagavulin/waiting_lagavulin_turn_1_with_powers_in_hand.json',
            ['play 1'])

    def test_waiting_lagavulin_use_terror(self):
        self.execute_handler_tests(
            '/battles/specific_comparator_cases/waiting_lagavulin/waiting_lagavulin_turn_1_with_terror_in_hand.json',
            ['play 1 0'])

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
            ['play 2 0'])

    def test_waiting_lagavulin_no_powers_but_relic(self):
        self.execute_handler_tests(
            '/battles/specific_comparator_cases/waiting_lagavulin/waiting_lagavulin_turn_1_without_powers_but_relic.json',
            ['end'])

    def test_waiting_lagavulin_wait_for_talk_to_the_hand(self):
        self.execute_handler_tests(
            '/battles/specific_comparator_cases/waiting_lagavulin/waiting_lagavulin_turn_1_with_talk_to_the_hand_in_deck.json',
            ['end'])

    def test_waiting_lagavulin_use_talk_to_the_hand(self):
        self.execute_handler_tests(
            '/battles/specific_comparator_cases/waiting_lagavulin/waiting_lagavulin_turn_1_with_talk_to_the_hand_in_hand.json',
            ['play 1 0'])

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
        new_mb = self.execute_handler_tests('/battles/memory/powered_up_ritual_dagger.json', ['play 3 0'], mb)
        self.assertEqual(6, new_mb.memory_by_card[CardId.RITUAL_DAGGER][reset_schedule][card_uuid])

    def test_prefer_killing_with_ritual_dagger(self):
        self.execute_handler_tests('/battles/memory/kill_with_ritual_dagger.json', ['play 3 0'])

    def test_memory_book_attacks_per_turn_is_updated(self):
        mb = TheBotsMemoryBook.new_default(last_known_turn=1)
        mb.memory_general[MemoryItem.ATTACKS_THIS_TURN] = 2
        new_mb = self.execute_handler_tests('/battles/memory/finisher.json', ['play 4 0'], mb)
        self.assertEqual(3, new_mb.memory_general[MemoryItem.ATTACKS_THIS_TURN])

    def test_memory_book_claw_state_persists_when_a_different_card_is_played(self):
        mb = TheBotsMemoryBook.new_default()
        mb.memory_general[MemoryItem.CLAWS_THIS_BATTLE] = 1
        new_mb = self.execute_handler_tests('battles/memory/basic_turn_1.json', memory_book=mb)
        self.assertEqual(1, new_mb.memory_general[MemoryItem.CLAWS_THIS_BATTLE])

    def test_memory_book_claw_state_increases_when_claw_is_played(self):
        mb = TheBotsMemoryBook.new_default()
        mb.memory_general[MemoryItem.CLAWS_THIS_BATTLE] = 1
        new_mb = self.execute_handler_tests('battles/memory/claw.json', memory_book=mb)
        self.assertEqual(2, new_mb.memory_general[MemoryItem.CLAWS_THIS_BATTLE])

    def test_play_genetic_algorithm_when_nothing_better_to_do(self):
        self.execute_handler_tests('/battles/memory/play_genetic_algorithm.json', ['play 1'])

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
        self.execute_handler_tests('/battles/memory/play_claws_despite_high_block.json', ['play 4 0'])

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
        new_mb = self.execute_handler_tests('battles/general/play_slimed.json', memory_book=mb)
        self.assertEqual(CardType.OTHER, new_mb.memory_general[MemoryItem.TYPE_LAST_PLAYED])

    def test_prefer_removing_more_plated_armor(self):
        self.execute_handler_tests('/battles/with_orbs/remove_plated_armor.json', ['play 1'])

    def test_do_not_waste_time_on_generating_more_energy_when_winning_battle(self):
        self.execute_handler_tests('/battles/general/do_not_waste_time_generating_more_energy.json', ['play 3 0'])

    def test_do_not_end_when_we_can_still_generate_energy_for_plays(self):
        self.execute_handler_tests('/battles/general/no_energy_but_can_generate_some.json', ['play 3'])

    def test_prefer_ending_in_calm(self):
        self.execute_handler_tests('/battles/stances/vigilance_only_useful_for_calm.json', ['play 1'])

    def test_prefer_exiting_wrath(self):
        mb = TheBotsMemoryBook.new_default()
        mb.memory_general[MemoryItem.STANCE] = StanceType.WRATH
        self.execute_handler_tests('/battles/stances/prefer_exiting_wrath.json', memory_book=mb,
                                   expected=['play 1 0'])

    def test_stay_in_wrath_safely(self):
        mb = TheBotsMemoryBook.new_default()
        mb.memory_general[MemoryItem.STANCE] = StanceType.WRATH
        self.execute_handler_tests('/battles/stances/stay_in_wrath_safely.json', memory_book=mb,
                                   expected=['end'])

    def test_prefer_generating_card_over_not(self):
        self.execute_handler_tests('/battles/general/play_carve_reality.json', ['play 1 0'])

    def test_we_do_not_play_blasphemy_usually(self):
        self.execute_handler_tests('/battles/powers/blasphemy_just_helps_damage.json', ['play 2 0'])

    def test_we_play_blasphemy_if_we_can_win_with_it(self):
        self.execute_handler_tests('/battles/powers/play_blasphemy_to_win.json', ['play 1 0'])

    def test_we_do_not_play_blasphemy_when_unawakened_present(self):
        self.execute_handler_tests('/battles/powers/do_not_blaspheme_unawakened_bird.json', ['play 2 0'])

    def test_prefer_killing_with_lesson_learned(self):
        self.execute_handler_tests('/battles/memory/kill_with_lesson_learned.json', ['play 1 0'])

    def test_prefer_having_enemy_talking_to_hand(self):
        self.execute_handler_tests('/battles/general/kill_not_with_talk_to_hand.json', ['play 2 0'])

    def test_do_not_break_when_no_monsters_alive_to_be_vulnerable(self):
        self.execute_handler_tests('/battles/general/breaks_when_no_monsters_alive_but_not_won.json', ['play 2 2'])

    def test_big_fight_do_not_pass_just_to_save_vigor(self):
        mb = TheBotsMemoryBook.new_default()
        mb.memory_general[MemoryItem.STANCE] = StanceType.CALM
        self.execute_handler_tests('/battles/specific_comparator_cases/big_fight/big_fight_do_not_pass.json',
                                   memory_book=mb, expected=['play 1 0'])

    def test_do_not_bother_attacking_when_enemy_will_die_anyway_to_fading(self):
        self.execute_handler_tests('/battles/powers/transient_dying_to_fading.json', ['end'])

    def test_better_to_save_tranquility_than_trigger_letter_opener(self):
        self.execute_handler_tests('/battles/general/save_tranquility.json', ['end'])

    def test_better_to_save_crescendo_than_hurt_monster_some_more(self):
        self.execute_handler_tests('/battles/specific_comparator_cases/big_fight/big_fight_save_crescendo.json',
                                   ['play 2 0'])

    def test_do_not_save_crescendo_outside_big_fight(self):
        self.execute_handler_tests('/battles/general/do_not_save_crescendo.json', ['play 1'])

    def test_use_tranquility_to_trigger_letter_opener(self):
        self.execute_handler_tests('/battles/general/use_tranquility.json', ['play 1'])

    def test_transient_do_not_bother_attacking_since_no_damage(self):
        self.execute_handler_tests('/battles/specific_comparator_cases/transient/do_not_bother_attacking_anymore.json',
                                   ['end'])

    def test_transient_still_attack_to_reduce_damage(self):
        self.execute_handler_tests('/battles/specific_comparator_cases/transient/still_attack_to_reduce_damage.json',
                                   ['play 1 0'])

    def test_play_more_block_because_barricade(self):
        self.execute_handler_tests('/battles/powers/play_more_block_because_barricade.json',
                                   ['play 1'])

    def test_play_more_block_because_calipers(self):
        self.execute_handler_tests('/battles/powers/play_more_block_because_calipers.json',
                                   ['play 1'])

    def test_do_not_use_perseverance_to_block_2_damage(self):
        self.execute_handler_tests('/battles/general/do_not_use_perseverance_to_prevent_2_damage.json', ['end'])

    def test_intangible_but_should_still_block(self):
        self.execute_handler_tests('/battles/powers/intangible_but_should_still_block.json', ['play 1'])

    def test_play_core_surge_first_to_block_bias(self):
        self.execute_handler_tests('/battles/powers/play_core_surge_first_to_block_bias.json', ['play 3 0'])

    def test_save_expensive_sands_of_time(self):
        self.execute_handler_tests('battles/general/save_expensive_sands_of_time.json', ['end'])

    def test_use_expensive_sands_of_time(self):
        self.execute_handler_tests('battles/general/play_expensive_sands_of_time_to_get_kill.json', ['play 1 0'])

    def test_we_know_we_do_not_die_if_we_have_lizard_tail(self):
        self.execute_handler_tests('battles/reviving/keep_trying_we_have_lizard_tail.json', ['play 1'])

    def test_we_know_we_do_not_die_if_we_have_fairy_in_a_bottle(self):
        self.execute_handler_tests('battles/reviving/keep_trying_we_have_fairy_in_a_bottle.json', ['play 1'])

    def test_do_not_die_even_though_it_would_give_you_health(self):
        mb = TheBotsMemoryBook.new_default()
        mb.memory_general[MemoryItem.STANCE] = StanceType.NO_STANCE
        self.execute_handler_tests('battles/reviving/do_not_die_just_because_it_will_heal.json', ['end'], mb)

    def test_we_play_free_early_draw(self):
        self.execute_handler_tests('battles/draw/free_early_draw.json', ['play 1'])

    def test_we_like_paid_draw_via_rushdown(self):
        self.execute_handler_tests('battles/draw/play_rushdown_early_to_benefit_from_the_draw.json', ['play 2'])

    def test_play_more_to_avoid_awkward_time_warp(self):
        self.execute_handler_tests(
            'battles/specific_comparator_cases/big_fight/time_eater_play_more_to_avoid_inconvenient_time_warp.json',
            ['play 1 0'])

    def test_play_less_to_avoid_awkward_time_warp(self):
        self.execute_handler_tests(
            'battles/specific_comparator_cases/big_fight/time_eater_play_less_to_avoid_inconvenient_time_warp.json',
            ['end'])

    def test_prefer_going_after_spear(self):
        self.execute_handler_tests('battles/specific_comparator_cases/shield_and_spear/shield_and_spear_go_after_spear.json',
                                   ['play 1 1'])

    def test_heart_uses_big_fight_comparator(self):
        self.execute_handler_tests(
            'battles/specific_comparator_cases/big_fight/big_fight_heart_prioritize_power_over_damage.json', ['play 1'])

    def test_end_turn_after_excessive_amount_of_cards_played(self):
        mb = TheBotsMemoryBook.new_default()
        mb.memory_general[MemoryItem.CARDS_THIS_TURN] = 55
        self.execute_handler_tests('battles/memory/excessive_amount_of_cards_played.json', ['end'], mb)

    def test_end_turn_after_excessive_amount_of_cards_played_even_if_we_can_draw_more(self):
        mb = TheBotsMemoryBook.new_default()
        mb.memory_general[MemoryItem.CARDS_THIS_TURN] = 55
        self.execute_handler_tests('battles/memory/excessive_amount_of_cards_played_can_still_draw_with_rushdown.json', ['end'], mb)

    def test_keep_playing_usefully_after_excessive_amount_of_cards_played(self):
        mb = TheBotsMemoryBook.new_default()
        mb.memory_general[MemoryItem.CARDS_THIS_TURN] = 55
        self.execute_handler_tests('battles/memory/excessive_amount_of_cards_played_but_can_still_damage_enemy.json',
                                   ['play 1 0'], mb)
