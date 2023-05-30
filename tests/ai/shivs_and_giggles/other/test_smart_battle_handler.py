from ai.shivs_and_giggles.sg_test_handler_fixture import SgTestHandlerFixture
from rs.common.handlers.common_battle_handler import CommonBattleHandler


class SmartBattleHandlerTestCase(SgTestHandlerFixture):
    handler = CommonBattleHandler

    def test_discard_works_correctly(self):
        self.execute_handler_tests('/battles/smart_battle/smart_battle_discard.json',
                                   ['choose 1', 'confirm', 'wait 30'])

    def test_discard_is_okay_with_no_cards(self):
        self.execute_handler_tests('/battles/smart_battle/smart_battle_discard_no_cards.json', [])

    def test_attacks_into_block_when_barricade_is_up(self):
        self.execute_handler_tests('/battles/smart_battle/smart_battle_attack_barricade.json', ['play 1'])

    def test_plays_powers_when_nothing_better_to_do(self):
        self.execute_handler_tests('/battles/smart_battle/smart_battle_play_powers.json', ['play 3'])

    def test_do_not_expect_thorns_to_kill_debuffing_enemy(self):
        self.execute_handler_tests(
            '/battles/smart_battle/smart_battle_manual_kill_when_enemy_not_attacking_into_thorns.json', ['play 1 0'])

    def test_do_not_block_against_non_attack_even_though_enemy_is_strong(self):
        self.execute_handler_tests('/battles/smart_battle/smart_battle_monster_not_attacking_but_has_strength_up.json', ['play 2 1'])

    def test_plays_slimeds_when_nothing_better_to_do(self):
        self.execute_handler_tests('/battles/smart_battle/smart_battle_play_slimed.json', ['play 1'])

    def test_do_not_discard_bad_ethereal_cards(self):
        self.execute_handler_tests('/battles/smart_battle/smart_battle_hold_on_to_bad_ethereals.json',
                                   ['choose 2', 'confirm', 'wait 30'])

    def test_save_unnecessary_apparition_for_later(self):
        self.execute_handler_tests('/battles/smart_battle/smart_battle_save_unnecessary_apparition_for_later.json',
                                   ['choose 1', 'confirm', 'wait 30'])

    def test_avoid_shivs_in_discard_play_shiv_despite_high_block(self):
        self.execute_handler_tests('/battles/smart_battle/smart_battle_play_shivs_despite_high_block.json', ['play 4'])

    def test_avoid_shivs_in_discard_play_storm_of_steel_later(self):
        self.execute_handler_tests('/battles/smart_battle/smart_battle_play_storm_of_steel_later.json', ['play 1'])

    def test_discard_doubt(self):
        self.execute_handler_tests('/battles/smart_battle/smart_battle_discard_doubt_specifically.json', ['play 1'])

    def test_gremlin_nob_defensive_skill_not_worth_it(self):
        self.execute_handler_tests('battles/smart_battle/gremlin_nob/smart_battle_gremlin_nob_defend_early.json', ['end'])

    def test_gremlin_nob_defensive_skill_worth_it(self):
        self.execute_handler_tests('battles/smart_battle/gremlin_nob/smart_battle_gremlin_nob_defend_late.json', ['play 5'])

    def test_gremlin_nob_damaging_skill_not_worth_it(self):
        self.execute_handler_tests('battles/smart_battle/gremlin_nob/smart_battle_gremlin_nob_cloak_and_dagger_early.json', ['end'])

    def test_gremlin_nob_indirectly_damaging_skill_not_worth_it(self):
        self.execute_handler_tests('battles/smart_battle/gremlin_nob/smart_battle_gremlin_nob_terror_and_thousand_cuts_late.json', ['end'])

    def test_gremlin_nob_damaging_skill_worth_it(self):
        self.execute_handler_tests('battles/smart_battle/gremlin_nob/smart_battle_gremlin_nob_cloak_and_dagger_late.json', ['play 1'])

    def test_gremlin_nob_avoid_prepared_draw_free_early(self):
        self.execute_handler_tests('battles/smart_battle/gremlin_nob/smart_battle_gremlin_nob_prepared.json', ['play 5'])

    def test_prefer_multiple_vulnerable_over_straight_damage(self):
        self.execute_handler_tests('battles/smart_battle/smart_battle_terror_vs_strike.json', ['play 1 0'])

    def test_general_artifact_prio(self):  # We might want soon want to generally get more aggressive on these though
        self.execute_handler_tests('battles/smart_battle/smart_battle_normal_artifact_removal.json', ['play 2 1'])

    def test_big_fight_higher_prio_remove_artifacts(self):
        self.execute_handler_tests('battles/smart_battle/big_fight/smart_battle_big_fight_prioritize_artifact_removal_over_damage.json', ['play 1 0'])

    def test_big_fight_higher_prio_powers(self):
        self.execute_handler_tests('battles/smart_battle/big_fight/smart_battle_big_fight_prioritize_power_over_damage.json', ['play 1'])

    def test_some_powers_higher_prio_than_others(self):
        self.execute_handler_tests('battles/smart_battle/smart_battle_prioritize_accuracy_over_energized.json', ['play 2'])

    def test_three_sentries_attacks_edge_sentry_even_when_mid_is_lower_health(self):
        self.execute_handler_tests('battles/smart_battle/three_sentries/smart_battle_sentry_low_middle_health.json', ['play 4 0'])

    def test_three_sentries_aggression_over_defense(self):
        self.execute_handler_tests('battles/smart_battle/three_sentries/smart_battle_sentry_yolo_state_with_three.json', ['play 4 0'])

    def test_three_sentries_use_normal_comparator_priorities_when_one_dead(self):
        self.execute_handler_tests('battles/smart_battle/three_sentries/smart_battle_sentry_one_dead.json', ['play 6'])

    def test_do_not_attack_escaped_mugger(self):
        self.execute_handler_tests('/battles/smart_battle/smart_battle_escaped_mugger.json', ['play 2 1'])

    def test_waiting_lagavulin_wait_for_powers(self):
        self.execute_handler_tests('/battles/smart_battle/waiting_lagavulin/smart_battle_waiting_lagavulin_turn_1_with_powers_in_deck.json', ['end'])

    def test_waiting_lagavulin_use_power(self):
        self.execute_handler_tests('/battles/smart_battle/waiting_lagavulin/smart_battle_waiting_lagavulin_turn_1_with_powers_in_hand.json', ['play 4'])

    def test_waiting_lagavulin_use_terror(self):
        self.execute_handler_tests('/battles/smart_battle/waiting_lagavulin/smart_battle_waiting_lagavulin_turn_1_with_terror_in_hand.json', ['play 3 0'])

    def test_waiting_lagavulin_no_powers(self):
        self.execute_handler_tests('/battles/smart_battle/waiting_lagavulin/smart_battle_waiting_lagavulin_turn_1_without_powers.json', ['play 3 0'])

    def test_waiting_lagavulin_turn_4(self):
        self.execute_handler_tests('/battles/smart_battle/waiting_lagavulin/smart_battle_waiting_lagavulin_turn_4_with_powers.json', ['play 3 0'])

    def test_waiting_lagavulin_event_lagavulin(self):
        self.execute_handler_tests('/battles/smart_battle/waiting_lagavulin/smart_battle_waiting_lagavulin_event_lagavulin_with_powers.json', ['play 3 0'])

    def test_waiting_lagavulin_no_powers_but_relic(self):
        self.execute_handler_tests('/battles/smart_battle/waiting_lagavulin/smart_battle_waiting_lagavulin_turn_1_without_powers_but_relic.json', ['end'])

    def test_playing_random_damage_is_desirable(self):
        self.execute_handler_tests('/battles/smart_battle/smart_battle_play_random_damage_card.json', ['play 1'])

    def test_playing_random_poison_is_desirable(self):
        self.execute_handler_tests('/battles/smart_battle/smart_battle_play_bouncing_flask.json', ['play 1'])
