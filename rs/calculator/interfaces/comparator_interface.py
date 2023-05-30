import abc

from rs.calculator.battle_state import BattleState


class ComparatorInterface(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def does_challenger_defeat_the_best(self, best: BattleState, challenger: BattleState,
                                        original: BattleState) -> bool:
        # must be implemented by children
        pass
