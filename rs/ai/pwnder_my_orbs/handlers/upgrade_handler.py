from rs.common.handlers.common_upgrade_handler import CommonUpgradeHandler


class UpgradeHandler(CommonUpgradeHandler):

    def __init__(self):
        super().__init__(priorities=[
            'apotheosis',
            'fission',
            'defragment',
            'biased cognition',
            'capacitor',
            'loop',
            'buffer',
            'electrodynamics',
            'genetic algorithm',
            'doom and gloom',
            'sunder',
            'coolheaded',
            'reinforced body',
            'equilibrium',
            'charge battery',
            'hologram',
            'core surge',
            'skim',
            'streamline',
            'ftl',
            'sweeping beam',
            'compile driver',
            'ball lightning',
            'cold snap',
            'glacier',
            'chill',
            'autoshields',
            'glacier',
        ])
