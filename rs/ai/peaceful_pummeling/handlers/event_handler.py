from rs.common.handlers.common_event_handler import CommonEventHandler
from rs.game.event import Event
from rs.machine.state import GameState


class EventHandler(CommonEventHandler):
    def __init__(self, removal_priority_list, cards_desired_for_deck):
        super().__init__(removal_priority_list=removal_priority_list, cards_desired_for_deck=cards_desired_for_deck)

    def find_event_choice(self, state: GameState) -> str | None:
        hp_per = state.get_player_health_percentage() * 100
        event = state.get_event()

        # Changes vs common handler: mainly a few health thresholds are lower
        match event:
            case Event.HYPNOTIZING_MUSHROOMS:
                if hp_per >= 30:
                    return "choose 0"  # Get 'em!
                return "choose 1"  # Take the heal and curse

            case Event.WING_STATUE:
                if hp_per >= 60:
                    return "choose 0"  # Purge at cost of 7 HP
                return "choose 1"  # Money or leave

            case Event.TRANSMOGRIFIER:
                return "choose 0"  # Take the transform, we have good coverage on Watcher.

            case Event.MASKED_BANDITS:
                if hp_per >= 50:
                    return "choose 1"  # Get 'em!
                return "choose 0"  # Give up all money and leave.

            case Event.THE_NEST:
                if hp_per >= 40:
                    return "choose 1"  # Ritual Dagger and a little damage.
                return "choose 0"  # Free money

        return super().find_event_choice(state)
