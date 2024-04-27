from rs.calculator.interfaces.player import PlayerInterface


def get_x_trigger_amount(player: PlayerInterface) -> int:
    return player.energy #todo -> include the chemical x here
