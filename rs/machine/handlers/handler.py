from rs.machine.state import GameState


class Handler:

    def can_handle(self, state: GameState) -> bool:
        return False

    def handle(self, state: GameState) -> str:
        raise Exception("must be implemented by children")
