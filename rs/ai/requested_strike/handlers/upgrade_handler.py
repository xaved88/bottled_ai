from rs.common.handlers.common_upgrade_handler import CommonUpgradeHandler


class UpgradeHandler(CommonUpgradeHandler):

    def __init__(self):
        super().__init__(priorities=[
            'apotheosis',
            'perfected strike',
            'bash',
            'shockwave',
            'uppercut',  # Not in pickup list at time of writing
            'battle trance',
            'offering',
            'blind',
            'seeing red',  # Not in pickup list at time of writing
            'dropkick',
            'flame barrier',
            'twin strike',
            'pommel strike',
            'handofgreed',
            'thunderclap',
            'shrug it off',
            'impervious',
            'ghostly armor',
            'master of strategy',
            'flash of steel',
            'trip',
            'dark shackles',
            'swift strike',
            'dramatic entrance',
            'finesse',
        ])
