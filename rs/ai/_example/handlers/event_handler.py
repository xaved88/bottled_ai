from rs.common.handlers.common_event_handler import CommonEventHandler
from rs.game.event import Event
from rs.machine.state import GameState


class EventHandler(CommonEventHandler):
    def __init__(self, removal_priority_list, cards_desired_for_deck):
        super().__init__(removal_priority_list=removal_priority_list, cards_desired_for_deck=cards_desired_for_deck)

    def find_event_choice(self, state: GameState) -> str | None:
        hp_per = state.get_player_health_percentage() * 100
        event = state.get_event()

        # Custom event handling specifically for this strategy
        match event:
            case Event.THE_DIVINE_FOUNTAIN:
                if hp_per > 50:
                    return "choose 1"  # Do not remove curses - usually a bad play, just done here as an example.

        return super().find_event_choice(state)
