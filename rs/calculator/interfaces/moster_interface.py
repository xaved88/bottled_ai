from rs.calculator.interfaces.target_interface import TargetInterface


class MonsterInterface(TargetInterface):
    damage: int
    hits: int
    is_gone: bool
