from typing import List
import re

from config import presentation_mode, p_delay, p_delay_s
from rs.ai.requested_scaling.synergies.synergy_beneficiaries import synergyBeneficiariesCardIdStrings
from rs.ai.requested_scaling.synergies.synergy_calculator import get_beneficiary_scores
from rs.ai.requested_scaling.synergies.synergy_providers import synergyProviderCardIdStrings
from rs.calculator.cards import CardId
from rs.game.screen_type import ScreenType
from rs.machine.command import Command
from rs.machine.handlers.handler import Handler
from rs.machine.state import GameState


class SynergyCardRewardHandler(Handler):

    def __init__(self):

        self.wanna_skip = False  # boolean to trigger skipping process
        # desired cards will be used for tiebreaks:
        # tiebreaks (if no synergy is clear) and saturation (max number of already owned cards)
        self.desired_cards: dict[str, int] = {
            'limit break': 2,
            'inflame': 2,
            'spot weakness': 1,
            'hemokinesis': 1,
            'immolate': 1,
            'offering': 1,
            'disarm': 2,
            'feel no pain': 3,
            'evolve': 1,
            'power through': 1,
            'battle trance': 1,
            'reaper': 2,
            'twin strike': 2,
            'pommel strike': 2,
            'shockwave': 1,
            'thunderclap': 1,
            'dropkick': 2,
            'flex': 1,
            'shrug it off': 5,
            'impervious': 2,
            'ghostly armor': 1,
            'flame barrier': 2,
            'burning pact': 1,
            'blind': 1,
            'dark embrace': 1,
            'pummel': 1,
            'apotheosis': 1,
            'handofgreed': 1,
            'master of strategy': 1,
            'flash of steel': 1,
            'trip': 1,
            'dark shackles': 1,
            'swift strike': 1,
            'dramatic entrance': 1,
            'fire breathing': 1,
            'cleave': 1,
            'clothesline': 1,
            'heavy blade': 1,
            'finesse': 1
        }
        # general cards. Have preference over desired cards if there is no clear synergy present
        self.universal_picks = {

            'inflame': 1,
            'shockwave': 1,
            'disarm': 1,
            'offering': 1,  # question mark
            'evolve': 1,
            'pommel strike': 1,
            'shrug it off': 1,
            'impervious': 1,
            'feel no pain': 1,
            'flame barrier': 1
        }
        # If there isnt a sinergy present, these cards will be unpickable
        # This should avoid "hope" plays
        self.pickable_only_after_synergy = [
            'heavy blade',
            'power through',
            'wild strike',
            'limit break',
            'entrench',
            'body slam',
            'dark embrace',
            'perfected strike',
            'anger'
        ]
        # Some general good initial damage cards to solve the first floors.
        # These should prevent picking 3 flame barriers in a row and dying to lagavuling or nob
        self.early_damage_solutions = {
            # one of this cards is enough to handle early damage:
            "one_card_solution": [
                'bludgeon',
                'immolate',
                'blood for blood',
                'hemokinesis',
                'uppercut',
                'fiend fire'
            ],

            # need at least 2 of these to fulfill the early damage check
            "two_card_solution": [
                'cleave',
                'inflame',
                'clothesline',
                'twin strike',
                'pommel strike',
                'dropkick',

            ]
        }
        # This will try to make sure that we pick one aoe card, even if it's not synergistic
        self.early_aoe_solutions = [
            'immolate',
            'cleave',
            'thunderclap'
            # whirlwind :(
        ]

    # handler condition
    def can_handle(self, state: GameState) -> bool:
        return state.has_command(Command.CHOOSE) \
                and state.screen_type() == ScreenType.CARD_REWARD.value \
                and (state.game_state()["room_phase"] == "COMPLETE" or state.game_state()["room_phase"] == "EVENT")

    def handle(self, state: GameState) -> List[str]:
        wanna_skip = self.wanna_skip  # importing boolean for skipping action
        current_deck = state.deck.cards
        # importing list of all synergies
        synergy_providers = self.get_synergy_provider_cards(state)
        synergy_beneficiaries = self.get_synergy_beneficiary_cards(state)

        # importing necessary lists of cards for tie breaks as well as checks
        desired_cards = self.desired_cards
        universal_picks = self.universal_picks
        pickable_only_after_synergy = self.pickable_only_after_synergy
        early_damage_solutions = self.early_damage_solutions

        list_of_choices = state.game_state()['screen_state']['cards']

        # convert string in choice_list to lowercase without + or numbers to avoid bugs
        choice_list = state.game_state()["choice_list"]
        not_upgraded_choice_list = []
        for card in choice_list:
            not_upgraded_choice_list.append(re.sub(r'\d+|\+', '', card))

        # Generating a list of allowed choices based on our current card pool in lowercase (non +) format
        allowed_stuff = [e.value for e in CardId]  # our current card_pool
        allowed_choices = [card for card in not_upgraded_choice_list if card in allowed_stuff]

        # Finally, we check if there is any card in the choice list that is already saturated:
        non_saturated_cards = self.get_non_saturated_cards(allowed_choices, desired_cards, current_deck)
        if len(non_saturated_cards) == 0:
            wanna_skip = True

        # We check for synergies in our current Deck:
        # synergies are given by synergy_providers and are applied to synergy_beneficiaries
        beneficiary_synergies: {str: int} = self.calculate_beneficiary_synergies(non_saturated_cards, current_deck)

        # Eliminating any card that has no synergy and is required to have a synergy to be picked
        beneficiary_synergies_only = self.delete_dict_keys_no_sinergy_and_requires_synergy(beneficiary_synergies,
                                                                                           pickable_only_after_synergy)

        # We check if there are any universal picks. If there is, but we already have them, don't consider
        necessary_universal_picks = self.get_necessary_universal_picks(non_saturated_cards, current_deck, universal_picks)

        # Covering checks for our current deck.
        solution_picks = self.get_solution_picks(state, non_saturated_cards, current_deck, early_damage_solutions)

        # Checking if we currently need a new provider in our deck
        new_provider_picks = self.get_new_providers(synergy_providers, non_saturated_cards, current_deck)

        pre_chosen_card = str
        # Setting up the decision-making:
        if solution_picks:
            pre_chosen_card = solution_picks[0]
        elif new_provider_picks:
            pre_chosen_card = new_provider_picks[0]  # first card
        elif necessary_universal_picks:
            pre_chosen_card = necessary_universal_picks[0]
        elif beneficiary_synergies_only:
            pre_chosen_card = self.get_max_key(beneficiary_synergies)

        # we have now assigned a value to pre_chosen_card
        if not pre_chosen_card or pre_chosen_card not in non_saturated_cards:
            wanna_skip = True

        if wanna_skip:
            self.skip_card(choice_list, state)

        else:
            index = not_upgraded_choice_list.index(pre_chosen_card)
            chosen_card = choice_list[index]

            if presentation_mode:
                return [p_delay, "choose " + str(chosen_card), "wait 30"]
            return ["wait 30", "choose " + str(chosen_card), "wait 30"]

    def calculate_beneficiary_synergies(self, non_saturated_cards, current_deck):
        beneficiary_synergies = {}
        for beneficiary_as_string in non_saturated_cards:
            beneficiary_synergies[beneficiary_as_string] = get_beneficiary_scores(CardId(beneficiary_as_string),
                                                                                  [CardId(c.id.lower()) for c in
                                                                                   current_deck])
        self.replace_none_with_zero(beneficiary_synergies)
        return beneficiary_synergies  # replace with your desired return value

    def replace_none_with_zero(self, data):
        if isinstance(data, dict):
            return {k: (v if v is not None else 0) for k, v in data.items()}
        elif isinstance(data, list):
            return [(x if x is not None else 0) for x in data]
        else:
            return data

    def delete_dict_keys_no_sinergy_and_requires_synergy(self, d, keys_to_delete):
        for k in keys_to_delete:
            if k in d and d[k] == 0:
                del d[k]
        if not d:
            return {}
        else:
            return d

    def get_max_key(self, initial_dict):
        # Get the maximum value in the initial dictionary
        max_value = max(initial_dict.values())
        sorted_tiebreaker_keys = self.desired_cards

        # Get all keys in the initial dictionary with the maximum value
        max_keys = [k for k, v in initial_dict.items() if v == max_value]

        # If there is only one key with the maximum value, return it
        if len(max_keys) == 1:
            return max_keys[0]

        # If there are ties, use the tiebreaker dictionary to break them
        else:
            # Get the first key in the sorted tiebreaker dictionary that appears in the list of keys with
            # maximum value in the initial dictionary
            max_tiebreaker_key = next((k for k in sorted_tiebreaker_keys if k in max_keys), None)

            return max_tiebreaker_key

    def skip_card(self, choice_list, state):
        if 'bowl' in choice_list:
            if presentation_mode:
                return [p_delay, "choose bowl", p_delay_s]
            return ["wait 30", "choose bowl"]

        if state.game_state()["room_phase"] == "EVENT":
            if presentation_mode:
                return [p_delay, "skip", p_delay_s]
            return ["skip"]  # There isn't a `proceed` available after skipping Neow's card obtain for example.

        if presentation_mode:
            return [p_delay, "skip", p_delay_s, "proceed"]
        return ["skip", "proceed"]  # This 'proceed' is for avoiding looking at the card rewards again.

    def get_synergy_provider_cards(self, state: GameState):
        scaling_cards = []
        stuff = synergyProviderCardIdStrings()
        allowed_stuff = [e.value for e in CardId]

        for card in state.deck.cards:
            if card.id.lower() in stuff and card.id.lower() in allowed_stuff:
                scaling_cards.append(card.id.lower())
        return scaling_cards

    def get_synergy_beneficiary_cards(self, state: GameState):
        synergy_beneficiaries = []
        stuff = synergyBeneficiariesCardIdStrings()
        allowed_stuff = [e.value for e in CardId]

        for card in state.deck.cards:
            if card.id.lower() in stuff and card.id.lower() in allowed_stuff:
                synergy_beneficiaries.append(card.id.lower())

        return synergy_beneficiaries


    def get_non_saturated_cards(self, allowed_choices, desired_cards, current_deck):
        non_saturated_cards = []
        for card in allowed_choices:
            if card not in desired_cards or current_deck.count(card) < desired_cards[card]:
                non_saturated_cards.append(card)
        return non_saturated_cards


    def get_necessary_universal_picks(self, non_saturated_cards, current_deck, universal_picks):
        necessary_universal_picks = []
        for card in non_saturated_cards:
            count_cards = 0
            if card in universal_picks:
                for current_card in current_deck:
                    if current_card.id.lower() == card:
                        count_cards += 1
                if count_cards < universal_picks[card]:
                    necessary_universal_picks.append(card)
        return necessary_universal_picks

    def get_solution_picks(self, state, non_saturated_cards, current_deck, early_damage_solutions):
        solution_picks = []
        early_damage_check = False
        current_floor = state.game_state()['floor']

        if current_floor <= 14:
            one_card_solution_counter = 0
            two_card_solution_counter = 0
            for current_card in current_deck:
                if current_card.id.lower() in early_damage_solutions["one_card_solution"]:
                    one_card_solution_counter += 1
                if current_card.id.lower() in early_damage_solutions["two_card_solution"]:
                    two_card_solution_counter += 1
                if one_card_solution_counter > 0 or two_card_solution_counter > 1:
                    early_damage_check = True
        else:
            early_damage_check = True

        if not early_damage_check:
            for card in non_saturated_cards:
                if card in early_damage_solutions["one_card_solution"]:
                    solution_picks.append(card)
            for card in non_saturated_cards:
                if card in early_damage_solutions["two_card_solution"]:
                    solution_picks.append(card)

        return solution_picks


    def get_new_providers(self, synergy_providers, non_saturated_cards, current_deck):
        new_providers = []
        # Determine if there are enough synergy providers in the current deck
        if len(synergy_providers) / len(current_deck) < 0.3:
            # Look for cards in non_saturated_cards that are also synergy providers
            for choice in non_saturated_cards:
                if choice in synergy_providers:
                    new_providers.append(choice)
                    """Need to implement better inclusion of providers"""
        return new_providers
