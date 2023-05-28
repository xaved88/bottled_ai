from rs.common.handlers.common_neow_handler import CommonNeowHandler


class NeowHandler(CommonNeowHandler):

    def __init__(self):
        super().__init__(desired_choices=[
            'upgrade a card',
            'obtain a random common relic',
            'obtain 100 gold',
            'choose a card to obtain',
            'obtain 3 random potions',
            'choose a colorless card to obtain',
            'max hp +8',
            'obtain a random rare card',
            'enemies in your next three combats have 1 hp',
            'remove a card from your deck',
            'transform a card',
            'lose your starting relic obtain a random boss relic',
        ])
