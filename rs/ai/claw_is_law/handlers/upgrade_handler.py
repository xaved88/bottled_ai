from rs.common.handlers.common_upgrade_handler import CommonUpgradeHandler


class UpgradeHandler(CommonUpgradeHandler):

    def __init__(self):
        super().__init__(priorities=[
            'apotheosis',
            'reprogram',
            'fission',
            'streamline',
            'hyperbeam',
            'all for one',
            'go for the eyes',
            'beam cell',
            'reinforced body',
            'scrape',
            'reboot',
            'steam barrier',
            'equilibrium'
            'ftl',
            'ball lightning',
            'claw',
            'zap',
            'boot sequence',
        ])
