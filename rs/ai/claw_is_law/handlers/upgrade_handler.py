from rs.common.handlers.common_upgrade_handler import CommonUpgradeHandler


class UpgradeHandler(CommonUpgradeHandler):

    def __init__(self):
        super().__init__(priorities=[
            'apotheosis',
            'streamline',
            'all for one',
            'go for the eyes',
            'beam cell',
            'reboot',
            'steam barrier',
            'claw',
            'zap',
        ])
