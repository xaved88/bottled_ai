from typing import List

from rs.calculator.cards import CardId
from rs.calculator.synergies.synergy_tags import SynergyTag

SynergyProviders = {

    CardId.INFLAME: [SynergyTag.STRENGTH],
    CardId.JAX: [SynergyTag.STRENGTH],
    CardId.LIMIT_BREAK: [SynergyTag.STRENGTH],
    CardId.SPOT_WEAKNESS: [SynergyTag.STRENGTH],
    CardId.BASH: [SynergyTag.STRENGTH],

}

def synergyProviderCardIdStrings() -> List[str]:
    return [v.value for v in SynergyProviders.keys()]
