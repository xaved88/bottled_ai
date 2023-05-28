from rs.common.handlers.common_combat_reward_handler import CommonCombatRewardHandler


class CombatRewardHandler(CommonCombatRewardHandler):

    def __init__(self):
        super().__init__(undesired_relics=[
            'Dead Branch',
            'Bottled Flame',
        ])
