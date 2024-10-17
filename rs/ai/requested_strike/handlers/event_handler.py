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
            case Event.GOLDEN_IDOL:
                if state.has_relic("Ectoplasm"):
                    return "choose 1"  # Leave!
                if len(state.get_choice_list()) == 2:
                    return "choose 0"  # Take it!
                if len(state.get_choice_list()) == 3:
                    if state.get_relic_counter("Omamori") >= 1:
                        return "choose 0"  # curse
                    if hp_per >= 50:
                        return "choose 1"  # 25% (35%) damage
                    return "choose 2"  # max hp loss

            case Event.WORLD_OF_GOOP:
                if hp_per >= 70 and not state.has_relic("Ectoplasm"):
                    return "choose 0"  # Take the money and lose a little HP.
                return "choose 1"  # Leave

            case Event.WING_STATUE:
                if hp_per >= 60:
                    return "choose 0"  # Purge at cost of 7 HP
                return "choose 1"  # Money or leave

            case Event.SHINING_LIGHT:
                if hp_per >= 50:
                    return "choose 0"  # Take the 2 random upgrades.
                return "choose 1"  # Leave.

        return super().find_event_choice(state)