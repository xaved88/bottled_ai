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


        # ACT 1

        if event_name == "Big Fish":
            return ["choose 1", "choose 0"]  # Max health

        # if event_name == "The Cleric":
        #    return ["choose 1"] # Purge at cost of 7 HP
        # dunno how to handle this yet, we theoretically might not have money

        if event_name == "Dead Adventurer":
            return ["choose 1", "choose 0"]  # Escape. Maybe we could take it if we have lots of health.

        if event_name == "Golden Idol":
            return ["choose 1", "choose 0"]  # Leave. Wouldn't mind taking it if it's early and we've got the health.

        if event_name == "Hypnotizing Colored Mushrooms":
            return ["choose 0"]  # Fuck 'em up

        # if event_name == "Living Wall":
        #    return ["choose 2"] # Upgrade Card - needs more logic to not get stuck

        if event_name == "Scrap Ooze":
            return ["choose 1", "choose 0"]  # Leave. Prefer logic for the event repeating, and then take the relic.

        if event_name == "Shining Light":
            return ["choose 1", "choose 0"]  # Leave. Would prefer to take it if health >=50%

        if event_name == "The Ssssserpent":
            return ["choose 1", "choose 0"]  # Leave

        if event_name == "World of Goop":
            return ["choose 1", "choose 0"]  # Leave. Would prefer to take it if health >=70%

        if event_name == "Wing Statue":
            return ["choose 0"]  # Purge at cost of 7 HP


        # ACT 1, 2

        if event_name == "Face Trader":
            return ["choose 2", "choose 0"]  # Leave. Would prefer to take it if health >=70%


        # ACT 1, 2, 3

        if event_name == "A Note For Yourself":
            return ["choose 1", "choose 0"]  # Ignore.

        if event_name == "Bonfire Spirits":
            return ["choose 0"]  # Purge

        if event_name == "The Divine Fountain":
            return ["choose 0", "choose 0"]  # Remove curses!

        if event_name == "Duplicator":
            return ["choose 1", "choose 0"]  # Needs some duplication logic, would be better, but for now leave.

        if event_name == "Golden Shrine":
            return ["choose 0", "choose 0"]  # Free money

        if event_name == "Lab":
            return ["choose 0"]  # Free potions

        # if event_name == "Match and Keep":
        #    return ["choose 0"]  # Existing logic just tries the first stuff over and over, fine.

        if event_name == "Ominous Forge":
            return ["choose 1", "choose 0"]  # I love the Warped Tongs relic.

        if event_name == "Purifier":
            return ["choose 0"]  # Purge

        if event_name == "Transmogrifier":
            return ["choose 1", "choose 0"]  # Avoid transforms, many cards are just kind of a curse for us.

        if event_name == "Upgrade Shrine":
            return ["choose 0"]  # Free upgrade

        # if event_name == "We Meet Again!":
        #    return ["choose 1", "choose 0"]  # Don't know how to make sure we avoid losing a card. Need to check.

        # if event_name == "The Woman in Blue":
        #    return ["choose 0", "choose 0"]  # Misbehaves in StS run display currently, will double-check still.


        # ACT 2

        if event_name == "Ancient Writing":
            return ["choose 1", "choose 0"]  # Upgrade all strikes and defends

        if event_name == "Augmenter":
            return ["choose 2", "choose 0"]  # Take the Mutagenic Strength relic.

        # if event_name == "The Colosseum":
        #    return ["choose 2", "choose 0"] # This event is weird, I'll just let the current logic handle this.

        if event_name == "Council of Ghosts":
            return ["choose 0", "choose 0"]  # Become a spooky ghost!

        if event_name == "Cursed Tome":
            return ["choose 1", "choose 0"]  # Leave, we don't currently make good use of the possible relics.

        # if event_name == "Forgotten Altar":
        #    return ["choose 2", "choose 0"] # Don't know how to handle this event.

        if event_name == "The Joust":
            return ["choose 1", "choose 0"]  # Slightly more expected value. ^^

        if event_name == "Knowing Skull":
            return ["choose 3", "choose 0"]  # Leave (also lol we probably would suicide on this without this decision.)

        if event_name == "The Library":
            return ["choose 1", "choose 0"]  # Heal, because heal, but also because I don't know if we handle this.

        if event_name == "Masked Bandits":
            return ["choose 1"]  # Fuck 'em up!!

        if event_name == "The Mausoleum":
            return ["choose 1", "choose 0"]  # Leave, we don't like curses and aren't good with relics.

        if event_name == "The Nest":
            return ["choose 0", "choose 0"]  # Take money over Dagger, I guess.

        if event_name == "N'loth":
            return ["choose 2", "choose 0"]  # Leave, wouldn't do well with the rare cards anyway.

        if event_name == "Old Beggar":
            return ["choose 0"]  # Cheap purge.

        # if event_name == "Pleading Vagrant":
        #    return ["choose 1", "choose 0"]  # Leave. Prefer the relic but money logic. Actually, needs testing.

        # if event_name == "Vampires(?)":
        #    return ["choose 0", "choose 0"]  # Want no bites but I need to have a look at the logs.


        # Act 2, 3

        # if event_name == "Designer In-Spire":
        #    return ["choose 0", "choose 0"]  # Just let default handling do this, it'll do reasonable things.


        # Act 3

        if event_name == "Falling":
            return ["choose 0", "choose 0"]  # Prefer losing skill, then power, then attack.

        if event_name == "Mind Bloom":
            return ["choose 0"]  # Fight an Act 1 boss for a relic.

        # if event_name == "The Moai Head":
        #    return ["choose 1", "choose 0"]  # Don't know how to make sure we leave yet.

        if event_name == "Mysterious Sphere":
            return ["choose 1", "choose 0"]  # Dangerous fight, avoid until we can add health logic.

        if event_name == "Secret Portal":
            return ["choose 1", "choose 0"]  # Nope - we want the rest of Act 3 to not screw up our stats.

        if event_name == "Sensory Stone":
            return ["choose 0"]  # Add 1 colorless Card but not really.

        # if event_name == "Tomb of Lord Red Mask":
        #    return ["choose 1", "choose 0"]  # Needs logic

        if event_name == "Winding Halls":
            return ["choose 2", "choose 0"]  # Lose Max HP to avoid dealing with complexity.

        return ["choose 0", "wait 30"]
