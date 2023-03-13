
from rs.calculator.cards import CardId
from rs.calculator.synergies.synergy_tags import SynergyTag

SynergyProviders = {

    CardId.INFLAME: [SynergyTag.STRENGTH, SynergyTag.DEXTERITY],
    CardId.JAX: [SynergyTag.STRENGTH, SynergyTag.STRENGTH],
    CardId.SPOT_WEAKNESS: [SynergyTag.STRENGTH, SynergyTag.STRENGTH],
    CardId.LIMIT_BREAK: [SynergyTag.STRENGTH],

    CardId.FEEL_NO_PAIN: [SynergyTag.EXHAUST, SynergyTag.EXHAUST, SynergyTag.EXHAUST, SynergyTag.EXHAUST],
    CardId.DARK_EMBRACE: [SynergyTag.EXHAUST, SynergyTag.EXHAUST, SynergyTag.EXHAUST],

    CardId.DISARM: [SynergyTag.DISARM, SynergyTag.EXHAUST, SynergyTag.EXHAUST, SynergyTag.EXHAUST],

    CardId.EVOLVE: [SynergyTag.STATUS, SynergyTag.STATUS],

    CardId.ACCURACY: [SynergyTag.SHIVS]

}

def synergyProviderCardIdStrings():
    return [v.value for v in SynergyProviders.keys()]
