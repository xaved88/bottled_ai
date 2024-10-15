from presentation_config import presentation_mode, p_delay, p_delay_s, slow_events
from rs.game.event import Event
from rs.game.screen_type import ScreenType
from rs.helper.logger import log_missing_event
from rs.machine.command import Command
from rs.machine.handlers.handler import Handler
from rs.machine.handlers.handler_action import HandlerAction
from rs.machine.state import GameState


class CommonEventHandler(Handler):

    def __init__(self, removal_priority_list, cards_desired_for_deck):
        self.removal_priority_list = removal_priority_list.copy()
        self.cards_desired_for_deck = cards_desired_for_deck.copy()

    def can_handle(self, state: GameState) -> bool:
        return state.screen_type() == ScreenType.EVENT.value and state.has_command(Command.CHOOSE)

    def handle(self, state: GameState) -> HandlerAction:

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
        event = state.get_event()

        match event:

            case Event.BIG_FISH:
                if hp_per <= 30:
                    return "choose 0"  # heal
                if state.get_relic_counter("Omamori") >= 1:
                    return "choose 2"  # relic and curse
                return "choose 1"  # max health up

            case Event.THE_CLERIC:
                if hp_per <= 65 and 'heal' in state.get_choice_list():
                    return "choose heal"
                if 'purify' in state.get_choice_list():
                    return "choose purify"  # Purge
                if hp_per >= 90:
                    return "choose leave"  # Heal not worth the money and can't purify apparently
                return "choose 0"

            case Event.DEAD_ADVENTURER:
                return "choose 1"  # Escape. Could do: Add logic for sometimes taking the fight.

            case Event.GOLDEN_IDOL:
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

            case Event.HYPNOTIZING_MUSHROOMS:
                if hp_per >= 40:
                    return "choose 0"  # Get 'em!
                return "choose 1" # Take the heal and curse

            case Event.LIVING_WALL:
                return "choose 2"  # Upgrade

            case Event.SCRAP_OOZE:
                return "choose 0"  # Yolo. We'll probably get it after a few tries? If not, we don't deserve to live!!

            case Event.SHINING_LIGHT:
                if hp_per >= 70:
                    return "choose 0"  # Take the 2 random upgrades.
                return "choose 1"  # Leave.

            case Event.THE_SSSSSERPENT:
                if state.get_relic_counter("Omamori") >= 1 and not state.has_relic("Ectoplasm"):
                    return "choose 0"  # Money in exchange for a curse
                return "choose 1"  # Leave

            case Event.WORLD_OF_GOOP:
                if hp_per >= 80 and not state.has_relic("Ectoplasm"):
                    return "choose 0"  # Take the money and lose a little HP.
                return "choose 1"  # Leave

            case Event.WING_STATUE:
                if hp_per >= 70:
                    return "choose 0"  # Purge at cost of 7 HP
                return "choose 1"  # Money or leave

            # ACT 1, 2

            case Event.FACE_TRADER:
                if hp_per >= 75 and not state.has_relic("Ectoplasm"):
                    return "choose 0"
                return "choose 2"  # Leave.

            # ACT 1, 2, 3

            case Event.A_NOTE_FOR_YOURSELF:
                return "choose 1"  # Ignore.

            case Event.BONFIRE_SPIRITS:
                return "choose 0"  # Purge

            case Event.THE_DIVINE_FOUNTAIN:
                return "choose 0"  # Remove curses!

            case Event.DUPLICATOR:
                return "choose 1"  # Needs some duplication logic, would be better, but for now leave.

            case Event.GOLDEN_SHRINE:
                if state.get_relic_counter("Omamori") >= 1 and not state.has_relic("Ectoplasm"):
                    return "choose 1"  # More free money!
                return "choose 0"  # Free money

            case Event.LAB:
                return "choose 0"  # Free potions

            case Event.MATCH_AND_KEEP:
                return "choose 0"  # Just keep clicking

            case Event.OMINOUS_FORGE:
                if state.get_relic_counter("Omamori") >= 1:
                    return "choose 1"  # Warped tongs!
                if state.floor() >= 30:
                    return "choose 0"  # Might not be able to reasonably get rid of the curse anymore
                return "choose 1"  # I love the Warped Tongs relic.

            case Event.PURIFIER:
                return "choose 0"  # Purge

            case Event.TRANSMOGRIFIER:
                return "choose 1"  # Ignore the transform since we don't know all cards (depending on character)

            case Event.UPGRADE_SHRINE:
                return "choose 0"  # Free upgrade

            case Event.WE_MEET_AGAIN:
                return "choose 0" # Todo

            case Event.THE_WOMAN_IN_BLUE:
                return "choose 0"  # Grab 1 potion, or if we don't have enough money, leave.

            # ACT 2

            case Event.ANCIENT_WRITING:
                return "choose 1"  # Upgrade all strikes and defends always because we currently can't tell the difference between card selection and purging in a grid event.

            case Event.AUGMENTER:
                return "choose 2"  # Take the Mutagenic Strength relic.

            case Event.THE_COLOSSEUM:
                return "choose 0" # todo

            case Event.COUNCIL_OF_GHOSTS:
                if state.has_relic("Snecko Eye") or state.deck.contains_cards(["Bite"]):  # Not amazing combos:
                    return "choose refuse"
                return "choose accept"  # Become a spooky ghost!

            case Event.CURSED_TOME:
                return "choose 1"  # Leave, we don't currently make good use of the possible relics.

            case Event.FORGOTTEN_ALTAR:
                return "choose 0" # todo

            case Event.THE_JOUST:
                return "choose 0"  # Be conservative

            case Event.KNOWING_SKULL:
                return "choose 3"  # Leave

            case Event.THE_LIBRARY:
                return "choose sleep"  # Heal, because we currently can't tell the difference between card selection and purging in a grid event.

            case Event.MASKED_BANDITS:
                if hp_per >= 65:
                    return "choose 1"  # Get 'em!
                return "choose 0"  # Give up all money and leave.

            case Event.THE_MAUSOLEUM:
                if state.get_relic_counter("Omamori") >= 1:
                    return "choose 0"
                return "choose 1"  # Leave, we don't like curses.

            case Event.THE_NEST:
                return "choose 0"  # Free money. 1 would be Ritual Dagger and a little damage.

            case Event.NLOTH:
                return "choose 2"  # Leave, hard to statically make a good choice here.

            case Event.OLD_BEGGAR:
                return "choose 0"  # Cheap purge.

            case Event.PLEADING_VAGRANT:
                if state.get_relic_counter("Omamori") >= 1:
                    return "choose rob"  # Get curse and relic
                elif "offer gold" in state.get_choice_list():
                    return "choose offer gold"  # 85 gold for random relic
                else:
                    return "choose leave"

            case Event.VAMPIRES:
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

            case Event.DESIGNER_IN_SPIRE:
                return "choose 0"  # It'll do reasonable things like upgrading and removing.

            # Act 3

            case Event.FALLING:
                options = state.get_falling_event_options()

                # check for stuff we want to purge
                for least_desired in self.removal_priority_list:
                    if least_desired in options:
                        for idx, card in enumerate(options):
                            if card == least_desired:
                                return "choose " + str(idx)

                # check for cards not in the pickup list
                for idx, option in enumerate(options):
                    if option not in self.cards_desired_for_deck:
                        return "choose " + str(idx)

                # check for lowest card on the pickup list
                pickup_prios = list(self.cards_desired_for_deck.keys())
                pickup_prios.reverse()

                for least_desired in pickup_prios:
                    if least_desired in options:
                        for idx, card in enumerate(options):
                            if card == least_desired:
                                return "choose " + str(idx)

            case Event.MIND_BLOOM:
                return "choose 0"  # Fight an Act 1 boss for a relic.

            case Event.MIND_BLOOM:
                return "choose 1"  # Get a bunch of money or leave

            case Event.MYSTERIOUS_SPHERE:
                if hp_per >= 70:
                    return "choose 0"  # Get 'em!
                else:
                    return "choose 1"  # Leave

            case Event.SECRET_PORTAL:
                return "choose 1"  # Nope - we want the rest of Act 3 to not screw up our stats.

            case Event.SENSORY_STONE:
                return "choose 0"  # Get a free colorless obtain

            case Event.TOMB_OF_LORD_RED_MASK:
                if state.has_relic("Red Mask") or state.game_state()['gold'] <= 130:
                    return "choose 0"  # Either free money or cheap.
                else:
                    return "choose 1"  # Leave

            case Event.WINDING_HALLS:
                if state.get_relic_counter("Omamori") >= 1 and hp_per < 75:
                    return "choose 1"  # Take the curse and heal
                if hp_per <= 10:
                    return "choose 1"  # Take the curse and heal
                return "choose 2"  # Lose Max HP

            case _:
                log_missing_event(str(event))
                return "choose 0"
