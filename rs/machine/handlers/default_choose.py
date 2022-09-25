from rs.machine.command import Command
from rs.machine.handlers.handler import Handler
from rs.machine.state import GameState


class DefaultChooseHandler(Handler):

    def can_handle(self, state: GameState) -> bool:
        return state.has_command(Command.CHOOSE)

    def handle(self, state: GameState) -> str:
        # TODO -> if potion is choice and slots are full then discard.
        if state.get_choice_list()[0] == "potion" and state.are_potions_full():
            return "potion discard 0"

        return "choose 0"
