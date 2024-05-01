from rs.common.handlers.common_upgrade_handler import CommonUpgradeHandler


class UpgradeHandler(CommonUpgradeHandler):

    def __init__(self):
        super().__init__(priorities=[
            'apotheosis',
            'vigilance',
            'eruption',
            'crescendo',
            'tranquility',
            'master reality',
            'wreath of flame',
            'evaluate',
            'deceive reality',
            'like water',
            'empty body',
            'empty fist',
            'empty mind',
            'indignation',
            'rushdown',
            'tantrum',
            'mental fortress',
            'fear no evil',
            'halt',
            'inner peace',
            'flurry of blows',
            'prostrate',
            'worship',
            'pray',
            'prostrate',
        ])
