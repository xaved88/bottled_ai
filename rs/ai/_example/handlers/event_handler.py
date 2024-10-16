from typing import List

from presentation_config import presentation_mode, p_delay, p_delay_s, slow_events
from rs.ai._example.config import CARD_REMOVAL_PRIORITY_LIST, DESIRED_CARDS_FOR_DECK
from rs.game.screen_type import ScreenType
from rs.helper.logger import log_missing_event
from rs.machine.command import Command
from rs.machine.handlers.handler import Handler
from rs.machine.handlers.handler_action import HandlerAction
from rs.machine.state import GameState


class EventHandler(Handler):

    def can_handle(self, state: GameState) -> bool:
        return state.screen_type() == ScreenType.EVENT.value and state.has_command(Command.CHOOSE)

    def handle(self, state: GameState, slay_heart: bool) -> HandlerAction:

        if len(state.get_choice_list()) == 1:  # If there's just one option, take it.
            if presentation_mode or slow_events:
                return HandlerAction(commands=[p_delay, "choose 0", "wait 30"])
            return HandlerAction(commands=["choose 0", "wait 30"])

        if self.find_event_choice(state):  # Otherwise figure out what to do below!
            if presentation_mode or slow_events:
                return HandlerAction(commands=[p_delay, self.find_event_choice(state), p_delay_s])
            return HandlerAction(commands=[self.find_event_choice(state), "wait 30"])

    def find_event_choice(self, state: GameState) -> str:
        hp_per = state.get_player_health_percentage() * 100
        event_name = state.game_state()['screen_state']['event_name']

        # ACT 1

        if event_name == "Big Fish":
            if hp_per <= 30:
                return "choose 0"  # heal
            if state.get_relic_counter("Omamori") >= 1:
                return "choose 2"  # relic and curse
            return "choose 1"  # max health up

        if event_name == "The Cleric":
            if hp_per <= 65 and 'heal' in state.get_choice_list():
                return "choose heal"
            if 'purify' in state.get_choice_list():
                return "choose purify"  # Purge
            if hp_per >= 90:
                return "choose leave"  # Heal not worth the money and can't purify apparently
            return "choose 0"

        if event_name == "Dead Adventurer":
            return "choose 1"  # Escape. Could do: Add logic for sometimes taking the fight.

        if event_name == "Golden Idol":
            if state.has_relic("Ectoplasm"):
                return "choose 1"  # Leave!
            if len(state.get_choice_list()) == 2:
                return "choose 0"  # Take it!
            if len(state.get_choice_list()) == 3:
                if state.get_relic_counter("Omamori") >= 1:
                    return "choose 0"  # curse
                if hp_per >= 90:
                    return "choose 1"  # 25% (35%) damage
                return "choose 2"  # max hp loss

        if event_name == "Mushrooms":
            if hp_per >= 40:
                return "choose 0"  # Get 'em!
            return "choose 1" # Take the heal and curse

        if event_name == "Living Wall":
            return "choose 2"  # Upgrade

        if event_name == "Scrap Ooze":
            return "choose 0"  # Yolo. We'll probably get it after a few tries? If not, we don't deserve to live!!

        if event_name == "Shining Light":
            if hp_per >= 70:
                return "choose 0"  # Take the 2 random upgrades.
            return "choose 1"  # Leave.

        if event_name == "The Ssssserpent":
            if state.get_relic_counter("Omamori") >= 1 and not state.has_relic("Ectoplasm"):
                return "choose 0"  # Money in exchange for a curse
            return "choose 1"  # Leave

        if event_name == "World of Goop":
            if hp_per >= 80 and not state.has_relic("Ectoplasm"):
                return "choose 0"  # Take the money and lose a little HP.
            return "choose 1"  # Leave

        if event_name == "Wing Statue":
            if hp_per >= 70:
                return "choose 0"  # Purge at cost of 7 HP
            return "choose 1"  # Money or leave

        # ACT 1, 2

        if event_name == "Face Trader":
            if hp_per >= 75 and not state.has_relic("Ectoplasm"):
                return "choose 0"
            return "choose 2"  # Leave.

        # ACT 1, 2, 3

        if event_name == "A Note For Yourself":
            return "choose 1"  # Ignore.

        if event_name == "Bonfire Spirits":
            return "choose 0"  # Purge

        if event_name == "The Divine Fountain":
            return "choose 0"  # Remove curses!

        if event_name == "Duplicator":
            return "choose 1"  # Needs some duplication logic, would be better, but for now leave.

        if event_name == "Golden Shrine":
            if state.get_relic_counter("Omamori") >= 1 and not state.has_relic("Ectoplasm"):
                return "choose 1"  # More free money!
            return "choose 0"  # Free money

        if event_name == "Lab":
            return "choose 0"  # Free potions

        if event_name == "Match and Keep":
            return "choose 0"  # Just keep clicking

        if event_name == "Ominous Forge":
            if state.get_relic_counter("Omamori") >= 1:
                return "choose 1"  # Warped tongs!
            if state.floor() >= 30:
                return "choose 0"  # Might not be able to reasonably get rid of the curse anymore
            return "choose 1"  # I love the Warped Tongs relic.

        if event_name == "Purifier":
            return "choose 0"  # Purge

        if event_name == "Transmogrifier":
            return "choose 1"  # Ignore the transform since we don't know all cards (depending on character)

        if event_name == "Upgrade Shrine":
            return "choose 0"  # Free upgrade

        # if event_name == "We Meet Again!"

        if event_name == "The Woman in Blue":
            return "choose 0"  # Grab 1 potion, or if we don't have enough money, leave.

        # ACT 2

        if event_name == "Ancient Writing":
            return "choose 1"  # Upgrade all strikes and defends always because we currently can't tell the difference between card selection and purging in a grid event.

        if event_name == "Augmenter":
            return "choose 2"  # Take the Mutagenic Strength relic.

        # if event_name == "The Colosseum"

        if event_name == "Council of Ghosts":
            if state.has_relic("Snecko Eye") or state.deck.contains_cards(["Bite"]):  # Not amazing combos:
                return "choose refuse"
            return "choose accept"  # Become a spooky ghost!

        if event_name == "Cursed Tome":
            return "choose 1"  # Leave, we don't currently make good use of the possible relics.

        # if event_name == "Forgotten Altar"

        if event_name == "The Joust":
            return "choose 0"  # Be conservative

        if event_name == "Knowing Skull":
            return "choose 3"  # Leave

        if event_name == "The Library":
            return "choose sleep"  # Heal, because we currently can't tell the difference between card selection and purging in a grid event.

        if event_name == "Masked Bandits":
            if hp_per >= 65:
                return "choose 1"  # Get 'em!
            return "choose 0"  # Give up all money and leave.

        if event_name == "The Mausoleum":
            if state.get_relic_counter("Omamori") >= 1:
                return "choose 0"
            return "choose 1"  # Leave, we don't like curses.

        if event_name == "The Nest":
            if hp_per >= 50:
                return "choose 1"  # Ritual Dagger and a little damage.
            return "choose 0"  # Free money

        if event_name == "N'loth":
            return "choose 2"  # Leave, hard to statically make a good choice here.

        if event_name == "Old Beggar":
            return "choose 0"  # Cheap purge.

        if event_name == "Pleading Vagrant":
            if state.get_relic_counter("Omamori") >= 1:
                return "choose rob"  # Get curse and relic
            elif "offer gold" in state.get_choice_list():
                return "choose offer gold"  # 85 gold for random relic
            else:
                return "choose leave"

        if event_name == "Vampires(?)":
            if state.deck.contains_cards(["Apparition"]):
                return "choose refuse"
            if state.has_relic("Strike Dummy"):
                return "choose refuse"
            if state.deck.contains_card_amount("strike") >= 3:  # note: these are specifically un-upgraded strikes
                if state.has_relic("Blood Vial"):
                    return "choose 1"  # Nom the Spire
                else:
                    return "choose accept"
            return "choose refuse"

        # Act 2, 3

        if event_name == "Designer In-Spire":
            return "choose 0"  # It'll do reasonable things like upgrading and removing.

        # Act 3

        if event_name == "Falling":
            options = state.get_falling_event_options()

            # check for stuff we want to purge
            for least_desired in CARD_REMOVAL_PRIORITY_LIST:
                if least_desired in options:
                    for idx, card in enumerate(options):
                        if card == least_desired:
                            return "choose " + str(idx)

            # check for cards not in the pickup list
            for idx, option in enumerate(options):
                if option not in DESIRED_CARDS_FOR_DECK:
                    return "choose " + str(idx)

            # check for lowest card on the pickup list
            pickup_prios = list(DESIRED_CARDS_FOR_DECK.keys())
            pickup_prios.reverse()

            for least_desired in pickup_prios:
                if least_desired in options:
                    for idx, card in enumerate(options):
                        if card == least_desired:
                            return "choose " + str(idx)

        if event_name == "Mind Bloom":
            return "choose 0"  # Fight an Act 1 boss for a relic.

        if event_name == "The Moai Head":
            return "choose 1"  # Get a bunch of money or leave

        if event_name == "Mysterious Sphere":
            if hp_per >= 70:
                return "choose 0"  # Get 'em!
            else:
                return "choose 1"  # Leave

        if event_name == "Secret Portal":
            return "choose 1"  # Nope - we want the rest of Act 3 to not screw up our stats.

        if event_name == "Sensory Stone":
            return "choose 0"  # Get a free colorless obtain

        if event_name == "Tomb of Lord Red Mask":
            if state.has_relic("Red Mask") or state.game_state()['gold'] <= 130:
                return "choose 0"  # Either free money or cheap.
            else:
                return "choose 1"  # Leave

        if event_name == "Winding Halls":
            if state.get_relic_counter("Omamori") >= 1 and hp_per < 75:
                return "choose 1"  # Take the curse and heal
            if hp_per <= 10:
                return "choose 1"  # Take the curse and heal
            return "choose 2"  # Lose Max HP

        log_missing_event(event_name)
        return "choose 0"