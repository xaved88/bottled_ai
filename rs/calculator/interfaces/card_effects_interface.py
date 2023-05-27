from rs.calculator.powers import Powers


class CardEffectsInterface:
    damage: int
    hits: int
    blockable: bool
    block: int
    applies_powers: Powers
    energy_gain: int
    draw: int
