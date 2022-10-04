from typing import List

from rs.game.screen_type import ScreenType
from rs.machine.command import Command
from rs.machine.handlers.handler import Handler
from rs.machine.state import GameState


class EventHandler(Handler):

    def can_handle(self, state: GameState) -> bool:
        return state.screen_type() == ScreenType.EVENT.value and state.has_command(Command.CHOOSE)

    def handle(self, state: GameState) -> List[str]:
        event_name = state.game_state()['screen_state']['event_name']

        # Act 1

        if event_name == "Big Fish":
            return ["choose 1", "choose 0"] # Max health

        # if event_name == "The Cleric":
        #    return ["choose 1"] # Purge at cost of 7 HP
        # dunno how to handle this yet, we theoretically might not have money

        # if event_name == "Dead Adventurer":
        #    return ["choose 1", "choose 0"] # Escape
        # currently untested

        if event_name == "Golden Idol":
            return ["choose 1", "choose 0"] # Leave. Wouldn't mind taking it if it's early and we've got the health.

        if event_name == "Hypnotizing Colored Mushrooms":
            return ["choose 0"] # Fuck 'em up

        # if event_name == "Living Wall":
        #    return ["choose 2", "choose 0"] # Upgrade Card
        # we need to do extra handling to make sure we're not always upgrading the first card here. example seed with this event (

        if event_name == "Scrap Ooze":
            return ["choose 1", "choose 0"] # Leave. Add some logic for the event repeating maybe, and then take the relic.

        if event_name == "Shining Light":
            return ["choose 1", "choose 0"] # Leave. Would prefer to take it if health >=50%

        if event_name == "The Ssssserpent":
            return ["choose 1", "choose 0"] # Leave

        if event_name == "World of Goop":
            return ["choose 1", "choose 0"] # Leave. Would prefer to take it if health >=70%

        if event_name == "Wing Statue":
            return ["choose 0"] # Purge at cost of 7 HP


        # Act 2

        # if event_name == "Augmenter":
        #    return ["choose 2","choose 0"] # Take the Mutagenic Strength relic.
        # currently untested


        return ["choose 0", "wait 30"]
