from rs.common.handlers.common_neow_handler import CommonNeowHandler


class NeowHandler(CommonNeowHandler):

    def __init__(self):
        super().__init__(desired_choices=[
            'upgrade a card',
            'obtain a random common relic',
            'choose a card to obtain',
            'transform a card',
            'remove a card from your deck',
            'obtain 100 gold',
            'obtain 3 random potions',
            'enemies in your next three combats have 1 hp',
            'lose your starting relic obtain a random boss relic',
            'max hp +8',
            'obtain a random rare card',
            'choose a colorless card to obtain',
        ])

