from ai.shivs_and_giggles.sg_test_handler_fixture import SgTestHandlerFixture
from rs.ai.shivs_and_giggles.handlers.smart_battle_handler import SmartBattleHandler


class SmartBattleHandlerTestCase(SgTestHandlerFixture):
    handler = SmartBattleHandler

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
        self.execute_handler_tests('/battles/smart_battle/smart_battle_manual_kill_when_enemy_not_attacking_into_thorns.json', ['play 1 0'])

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

    def test_against_gremlin_nob_defensive_skill_not_worth_it(self):
        self.execute_handler_tests('battles/smart_battle/smart_battle_gremlin_nob_defend_early.json', ['end'])

    def test_against_gremlin_nob_defensive_skill_worth_it(self):
        self.execute_handler_tests('battles/smart_battle/smart_battle_gremlin_nob_defend_late.json', ['play 5'])

    def test_against_gremlin_nob_damaging_skill_not_worth_it(self):
        self.execute_handler_tests('battles/smart_battle/smart_battle_gremlin_nob_cloak_and_dagger_early.json', ['end'])

    def test_against_gremlin_nob_indirectly_damaging_skill_not_worth_it(self):
        self.execute_handler_tests('battles/smart_battle/smart_battle_gremlin_nob_terror_and_thousand_cuts_late.json', ['end'])

    def test_against_gremlin_nob_damaging_skill_worth_it(self):
        self.execute_handler_tests('battles/smart_battle/smart_battle_gremlin_nob_cloak_and_dagger_late.json', ['play 1'])

    def test_multiple_vulnerable_over_straight_damage(self):
        self.execute_handler_tests('battles/smart_battle/smart_battle_terror_vs_strike.json', ['play 1 0'])

    def test_remove_artifacts_aggressively_against_donu_deca(self):
        self.execute_handler_tests('battles/smart_battle/smart_battle_donu_deca_prioritize_artifact_removal.json', ['play 1 0'])

    def test_normal_artifact_aggression(self):  # We might want soon want to generally get more aggressive on these though
        self.execute_handler_tests('battles/smart_battle/smart_battle_normal_artifact_removal.json', ['play 2 1'])
