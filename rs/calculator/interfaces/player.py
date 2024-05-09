from rs.calculator.interfaces.target_interface import TargetInterface


class PlayerInterface(TargetInterface):
    energy: int
    next_turn_hp: int
