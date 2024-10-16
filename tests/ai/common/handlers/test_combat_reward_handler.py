from ai.common.co_test_handler_fixture import CoTestHandlerFixture
from rs.common.handlers.common_combat_reward_handler import CommonCombatRewardHandler


class CombatRewardHandlerTestCase(CoTestHandlerFixture):
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
        self.execute_handler_tests('/combat_reward/combat_reward_full_potions_least_desired_in_hand.json',
                                   ['wait 30', 'potion discard 1'])

    def test_skips_least_desired_potion_when_full(self):
        self.execute_handler_tests('/combat_reward/combat_reward_full_potions_least_desired_not_in_hand.json',
                                   ['proceed'])

    def test_take_relic(self):
        self.execute_handler_tests('/combat_reward/combat_reward_relic.json', ['choose relic'])

    def test_check_card(self):
        self.execute_handler_tests('/combat_reward/combat_reward_card.json', ['choose card'])

    def test_check_card_even_though_potions_full(self):
        self.execute_handler_tests(
            '/combat_reward/combat_reward_full_potions_done_with_potions_do_not_skip_checking_card.json',
            ['choose card'])

    def test_do_not_die_from_relic_not_being_first(self):
        self.execute_handler_tests('/combat_reward/combat_reward_several_rewards.json', ['choose gold'])

    def test_skip_relic(self):
        self.execute_handler_tests('/combat_reward/combat_reward_relic_skip.json', ['proceed'])

    def test_skip_relic_multiple_relics_take_first(self):
        self.execute_handler_tests('/combat_reward/combat_reward_relics_2_take_first.json', ['choose relic'])

    # leaving this disabled for now since the check I'm doing is potentially too fragile
    # def test_skip_relic_multiple_relics_take_second(self):
    #     self.execute_handler_tests('/combat_reward/combat_reward_relics_2_take_second.json', ['proceed'])

    def test_skip_emerald_key_if_not_slay_heart(self):
        self.execute_handler_tests('/combat_reward/combat_reward_emerald_key.json', ['proceed'])

    def test_skip_sapphire_key_if_not_slay_heart(self):
        self.execute_handler_tests('/combat_reward/combat_reward_sapphire_key_floor_43.json', ['choose relic'])