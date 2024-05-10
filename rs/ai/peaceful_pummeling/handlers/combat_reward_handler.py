from rs.common.handlers.common_combat_reward_handler import CommonCombatRewardHandler


class CombatRewardHandler(CommonCombatRewardHandler):

    def __init__(self):
        super().__init__(undesired_relics=[
            'Dead Branch',
            'Bottled Flame',
        ], desired_potions=[
            'fruit juice',
            'fairy in a bottle',
            'cultist potion',
            'power potion',
            'duplication potion',
            'distilled chaos',
            'blessing of the forge',
            'attack potion',
            'dexterity potion',
            'ambrosia',
            'fear potion',
            'essence of steel',
            'strength potion',
            'regen potion',
            'blood potion',
            'entropic brew',
            'liquid bronze',
            'energy potion',
            'skill potion',
            'ancient potion',
            'weak potion',
            'gambler\u0027s brew',
            'colorless potion',
            'flex potion',
            'swift potion',
            'bottled miracle',
            'fire potion',
            'explosive potion',
            'speed potion',
            'block potion',
            'cunning potion',
            'ghost in a jar',
            'smoke bomb',
            'elixir potion',
            'liquid memories',
            'snecko oil',
            'stance potion',  # We might not know how to use it yet
        ])
