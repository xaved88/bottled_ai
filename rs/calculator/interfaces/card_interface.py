import abc

from rs.calculator.enums.card_id import CardId
from rs.game.card import CardType


class CardInterface(metaclass=abc.ABCMeta):
    id: CardId
    upgrade: int
    cost: int  # energy cost. Maybe -1 for no cost and not playable statuses?
    needs_target: bool
    ethereal: bool
    exhausts: bool
    type: CardType

    @abc.abstractmethod
    def get_state_string(self) -> str:
        # must be implemented by children
        pass
