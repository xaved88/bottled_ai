from rs.common.handlers.card_reward.common_grouped_card_reward_handler import CommonGroupedCardRewardHandler, \
    CardPriorityGroup

priorities = [
    # the great cards we always want
    CardPriorityGroup([
        ('electrodynamics', 1),
        ('echo form', 2),
        ('defragment', 5),
        ('biased cognition', 5),
        ('capacitor', 2),
        # ('seek', 2),
        ('loop', 2),
        ('core surge', 2),
        ('fission', 1),
        ('buffer', 1),
        ('skim', 1),
    ]),
    # orb attack cards
    CardPriorityGroup([
        ('ball lightning', 2),
        ('cold snap', 2),
        ('doom and gloom', 1),
    ], 3),
    # general attack cards
    CardPriorityGroup([
        ('sunder', 1),
        ('ball lightning', 1),
        ('cold snap', 1),
        ('doom and gloom', 1),
        ('streamline', 1),
        ('ftl', 1),
        ('sweeping beam', 1),
        ('bullseye', 1),
        ('compile driver', 2),
    ], 5),
    # frost orbs
    CardPriorityGroup([
        ('cold snap', 2),
        ('glacier', 1),
        ('coolheaded', 5),
        ('chill', 1),
    ], 5),
    # general defend
    CardPriorityGroup([
        ('charge battery', 2),
        #('hologram', 2),
        ('autoshields', 1),
        ('equilibrium', 1),
        #('genetic algorithm', 2),
        ('reinforced body', 2),
        ('glacier', 2),
    ], 5),
]


class CardRewardHandler(CommonGroupedCardRewardHandler):

    def __init__(self):
        super().__init__(priorities)
