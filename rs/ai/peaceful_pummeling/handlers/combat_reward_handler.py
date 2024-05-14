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
            'blessing of the forge',
            'attack potion',
            'dexterity potion',
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
            'distilled chaos',  # Might play Blasphemy
            'ambrosia',  # We don't know that we go into Divinity
            'stance potion',  # We might not know how to use it yet
        ])
