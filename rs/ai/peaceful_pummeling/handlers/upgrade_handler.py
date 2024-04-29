from rs.common.handlers.common_upgrade_handler import CommonUpgradeHandler


class UpgradeHandler(CommonUpgradeHandler):

    def __init__(self):
        super().__init__(priorities=[
            'apotheosis',
            'vigilance',
            'eruption',
            'crescendo',
            'tranquility',
            'prostrate',
        ])
