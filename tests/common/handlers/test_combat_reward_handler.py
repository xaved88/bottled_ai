from ai.shivs_and_giggles.sg_test_handler_fixture import SgTestHandlerFixture
from common.co_test_handler_fixture import CoTestHandlerFixture
from rs.ai.shivs_and_giggles.handlers.combat_reward_handler import CombatRewardHandler
from rs.common.handlers.common_combat_reward_handler import CommonCombatRewardHandler


class CardRewardHandlerTestCase(CoTestHandlerFixture):
    handler = CommonCombatRewardHandler

    def test_chug_fruit_juice(self):
        self.execute_handler_tests('/combat_reward/combat_reward_fruit_juice.json', ["wait 30", "potion use 1"])

    def test_take_gold(self):
        self.execute_handler_tests('/combat_reward/combat_reward_gold.json', ['choose gold'])

    def test_take_stolen_gold(self):
        self.execute_handler_tests('/combat_reward/combat_reward_stolen_gold.json', ['choose stolen_gold'])

    def test_take_potion(self):
        self.execute_handler_tests('/combat_reward/combat_reward_potion.json', ['choose potion'])

    def test_discards_least_desired_potion_when_full(self):
        self.execute_handler_tests('/combat_reward/combat_reward_full_potions_least_desired_in_hand.json', ['wait 30', 'potion discard 1'])

    def test_skips_least_desired_potion_when_full(self):
        self.execute_handler_tests('/combat_reward/combat_reward_full_potions_least_desired_not_in_hand.json', ['proceed'])

    def test_take_relic(self):
        self.execute_handler_tests('/combat_reward/combat_reward_relic.json', ['choose relic'])

    def test_check_card(self):
        self.execute_handler_tests('/combat_reward/combat_reward_card.json', ['choose card'])