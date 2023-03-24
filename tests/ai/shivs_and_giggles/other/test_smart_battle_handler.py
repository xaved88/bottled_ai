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