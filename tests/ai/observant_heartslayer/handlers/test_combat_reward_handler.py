from ai.observant_heartslayer.oh_test_handler_fixture import OhTestHandlerFixture
from rs.common.handlers.common_combat_reward_handler import CommonCombatRewardHandler


class CombatRewardHandlerTestCase(OhTestHandlerFixture):
    handler = CommonCombatRewardHandler

    def test_pick_up_emerald_key_because_slay_heart(self):
        self.execute_handler_tests('/combat_reward/combat_reward_emerald_key.json', ['choose emerald_key'])

    def test_pick_up_sapphire_key_because_slay_heart(self):
        self.execute_handler_tests('/combat_reward/combat_reward_sapphire_key_floor_43.json', ['choose sapphire_key'])

    def test_skip_sapphire_key_because_not_act_3(self):
        self.execute_handler_tests('/combat_reward/combat_reward_sapphire_key_not_floor_43.json', ['choose relic'])