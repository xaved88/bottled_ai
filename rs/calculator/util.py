from rs.calculator.enums.relic_id import RelicId
from rs.calculator.interfaces.player import PlayerInterface


def get_x_trigger_amount(player: PlayerInterface) -> int:
    amount = player.energy
    if player.relics.get(RelicId.CHEMICAL_X):
        amount += 2
    return amount
