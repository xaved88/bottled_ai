from typing import List
import re

from rs.game.card import Card, CardType

from config import presentation_mode, p_delay, p_delay_s
from rs.calculator.cards import CardId
from rs.calculator.synergies.synergy_beneficiaries import SynergyBeneficiaries, synergyBeneficiariesCardIdStrings
from rs.calculator.synergies.synergy_calculator import get_beneficiary_scores, get_provider_scores
from rs.calculator.synergies.synergy_providers import SynergyProviders, synergyProviderCardIdStrings
from rs.calculator.synergies.synergy_tags import SynergyTag
from rs.game.screen_type import ScreenType
from rs.machine.command import Command
from rs.machine.handlers.handler import Handler
from rs.machine.state import GameState
from rs.game.card import CardRarity


class SynergyCardRewardHandler(Handler):

    desired_cards: dict[str, int] = {
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

    universal_picks = {

        'inflame': 1,
        'shockwave': 1,
        'disarm': 1,
        'offering': 1, #question mark
        'evolve': 1,
        'pommel strike': 1,
        'shrug it off': 1,
        'impervious': 1,
        'feel no pain': 1,
        'flame barrier': 1
    }

    pickable_only_after_synergy = [
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

    early_damage_solutions = {
        #one of this cards is more than enough to handle early damage:
        "one_card_solution": [
            'bludgeon',
            'immolate',
            'blood for blood',
            'hemokinesis',
            'uppercut',
            'fiend fire'
        ],

        #need at least 2 of these to fulfill the early damage check
        "two_card_solution": [
            'cleave',
            'inflame',
            'clothesline',
            'twin strike',
            'pommel strike',
            'dropkick',

        ]
    }


    early_aoe_solutions = [
        'immolate',
        'cleave',
        'thunderclap'
        # whirlwind :(
    ]



    def can_handle(self, state: GameState) -> bool:
        return state.has_command(Command.CHOOSE) \
            and state.screen_type() == ScreenType.CARD_REWARD.value \
            and (state.game_state()["room_phase"] == "COMPLETE" or state.game_state()["room_phase"] == "EVENT")

    def handle(self, state: GameState) -> List[str]:

        current_deck = state.deck.cards
        synergy_providers = self.get_synergy_provider_cards(state)
        synergy_beneficiaries = self.get_synergy_beneficiary_cards(state)
        deck_attributes = self.getDeck_attributes(current_deck)
        desired_cards = self.desired_cards

        list_of_choices = state.game_state()['screen_state']['cards']

        new_deck_1 = current_deck.copy()
        new_deck_2 = current_deck.copy()
        new_deck_3 = current_deck.copy()

        new_deck_1.append(Card(list_of_choices[0]))
        new_deck_2.append(Card(list_of_choices[1]))
        new_deck_3.append(Card(list_of_choices[2]))

        prev_score = self.getScore(current_deck)
        after_score_1 = self.getScore(new_deck_1)
        after_score_2 = self.getScore(new_deck_2)
        after_score_3 = self.getScore(new_deck_3)

        choice_list = state.game_state()["choice_list"]
        not_upgraded_choice_list = []
        for card in choice_list:
            not_upgraded_choice_list.append(re.sub(r'\d+|\+', '', card))

        allowed_stuff = [e.value for e in CardId]
        allowed_choices = [card for card in not_upgraded_choice_list if card in allowed_stuff]

        """
        Here we will be avoinding any innecessary card saturation. Meaning multiple choices of a same card...
        For example, multiple copies of cleave, or clothesline, could be detremental. 
        """


        non_saturated_cards = []
        for card in allowed_choices:
            count_cards = 0
            if card in desired_cards:
                for current_card in current_deck:
                    if current_card.id.lower() == card:
                        count_cards += 1
                if count_cards < desired_cards[card]:
                    non_saturated_cards.append(card)
            else:
                non_saturated_cards.append(card)


        if len(non_saturated_cards) == 0:

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

        beneficiary_synergies: [str, float] = {}
        for beneficiary_as_string in non_saturated_cards:
            beneficiary_synergies[beneficiary_as_string] = get_beneficiary_scores(CardId(beneficiary_as_string),
                                                                                  [CardId(c.id.lower())
                                                                                   for c in current_deck])
        self.replace_none_with_zero(beneficiary_synergies)

        """
        Sinergy Required cards are removed at this point.
        Card like, wild strike or power through, even though they have big numbers, they can lead
        to difficult handling of wounds, if no synergy is available in the current deck (evolve...)
        Here we are telling the bot that any card inside this list will require any amount of synergy before it's chosen
        """
        pickable_only_after_synergy = self.pickable_only_after_synergy
        beneficiary_synergies_only = self.delete_dict_keys_no_sinergy_and_requires_synergy(beneficiary_synergies, pickable_only_after_synergy)


        """
        check for universal picks first.
        general good cards. Mostly supportive cards, like shrug it off.
        If we currently own the card, it will skip this. If it ends up choosing it, it's because it might be sinergistic.
        """
        universal_picks = self.universal_picks
        necessary_universal_picks = []
        for card in non_saturated_cards:
            count_cards = 0
            if card in universal_picks:
                for current_card in current_deck:
                    if current_card.id.lower() == card:
                        count_cards += 1
                if count_cards < universal_picks[card]:
                    necessary_universal_picks.append(card)

        """
        Check for solutions in the current act situation.
        We will, in order of appearance try to make sure that all these needs are covered, 
        before we attempt to use synergies as our driver for card choosing
        """

        # early_damage_solutions -> tries to make sure you have a good attack before first elites in act 1
        # early_aoe_solutions ->
        # first_boss_solutions -> tries to identify specific solutions that could be considered a major help for act 1 boss
            #we could later specify for every boss
        # second_act_aoe_solutions ->
        # scaling_solutions ->
        # energy_solutions -> this will apply only in act 2 and 3, and will check if we are still at 3 energy. If so, it will look for any energy generating card.
        # draw_solutions -> maybe include. For now, it won't be applying

        solution_picks = []

        early_damage_check = False
        #early_aoe_check = False
        #first_boss_check = False
        #second_act_aoe_check = False
        #scaling_check = False
        #energy_check = False
        #draw_check = False

        """early_damage_check:"""
        early_damage_solutions = self.early_damage_solutions
        # first check if we have any card in the dictionary:
        one_card_solution_counter = 0
        two_card_solution_counter = 0
        current_act = state.game_state()['act']
        current_floor = state.game_state()['floor']
        for current_card in current_deck:
            if current_floor <= 14:
                if current_card.id.lower() in early_damage_solutions["one_card_solution"]:
                    one_card_solution_counter += 1
                if current_card.id.lower() in early_damage_solutions["two_card_solution"]:
                    two_card_solution_counter += 1
                if one_card_solution_counter > 0 or two_card_solution_counter > 1:
                    early_damage_check = True
            else:
                early_damage_check = True

        if not early_damage_check: #early damage is not fulfilled:
            for card in non_saturated_cards:
                if card in early_damage_solutions["one_card_solution"]:
                    solution_picks.append(card)
            for card in non_saturated_cards:
                if card in early_damage_solutions["two_card_solution"]:
                    solution_picks.append(card)


        """
        This will check at any given moment if our current deck has no synergy providers.
        If we don't have enough, it will try to prioritize synergy providers to start scaling.
        """

        if len(synergy_providers) / len(current_deck) < 0.3:
            new_providers = []
            for choice in non_saturated_cards:
                if choice in synergy_providers:
                    new_providers.append(choice)
                    """Need to implement better inclusion of providers"""
            if len(new_providers) > 0:
                pre_chosen_card = new_providers[0]
                if pre_chosen_card:
                    index = not_upgraded_choice_list.index(pre_chosen_card)
                    chosen_card = choice_list[index]
                else:
                    chosen_card = "No Card"

            else:
                if len(beneficiary_synergies) == 0:
                    chosen_card = "No Card"
                else:
                    pre_chosen_card = self.get_max_key(beneficiary_synergies, desired_cards)
                    if pre_chosen_card:
                        index = not_upgraded_choice_list.index(pre_chosen_card)
                        chosen_card = choice_list[index]
                    else:
                        chosen_card = "No Card"


        else:
            pre_chosen_card = self.get_max_key(beneficiary_synergies, desired_cards)
            if pre_chosen_card:
                index = not_upgraded_choice_list.index(pre_chosen_card)
                chosen_card = choice_list[index]
            else:
                chosen_card = "No Card"

        """There is no chosen card"""
        if chosen_card == "No Card":

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

        """check for any universal picks"""
        if len(necessary_universal_picks) > 0:
            pre_chosen_card = necessary_universal_picks[0]
            if pre_chosen_card:
                index = not_upgraded_choice_list.index(pre_chosen_card)
                chosen_card = choice_list[index]


        """finally, remove everything above if there is one solution card needed at this point"""
        if len(solution_picks) > 0:
            pre_chosen_card = solution_picks[0]
            if pre_chosen_card:
                index = not_upgraded_choice_list.index(pre_chosen_card)
                chosen_card = choice_list[index]


        """There is a card chosen"""
        for card in self.desired_cards.keys():
            if card not in non_saturated_cards:
                continue
            if presentation_mode:
                return [p_delay, "choose " + str(choice_list[index]), "wait 30"]
            return ["wait 30", "choose " + str(choice_list[index]), "wait 30"]

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


    def getDeck_attributes(self, deck):
        deck_attributes = {
            "DECK_LENGTH": 0,
            "FLOWING_DECK_LENGTH": 0,
            "ATTACK": 0,
            "SKILL": 0,
            "POWER": 0,
            "BASICS_AMOUNT": 0,
            "UPGRADE_DENSITY": 0,
            "TOTAL_COST": 0,
            "AVERAGE_COST": 0

        }

        deck_attributes["DECK_LENGTH"] = len(deck)
        for card in deck:
            if not card.exhausts and not card.type == CardType.POWER:
                deck_attributes["FLOWING_DECK_LENGTH"] += 1
            if card.type == CardType.ATTACK:
                deck_attributes["ATTACK"] += 1
            if card.type == CardType.SKILL:
                deck_attributes["SKILL"] += 1
            if card.type == CardType.POWER:
                deck_attributes["POWER"] += 1
            if card.rarity == CardRarity.BASIC:
                deck_attributes["BASICS_AMOUNT"] += 1
            if card.upgrades > 0:
                deck_attributes["UPGRADE_DENSITY"] += 1
            deck_attributes["TOTAL_COST"] += card.cost

            deck_attributes["AVERAGE_COST"] = round(deck_attributes["TOTAL_COST"] / deck_attributes["DECK_LENGTH"],2)



        return deck_attributes

    def get_synergy_provider_cards(self, state: GameState):
        scaling_cards = []
        stuff = synergyProviderCardIdStrings()
        allowed_stuff = [e.value for e in CardId]

        for card in state.deck.cards:
            if card.id.lower() in stuff and card.id.lower() in allowed_stuff:
                scaling_cards.append(card.id.lower())
        return scaling_cards

    def get_synergy_beneficiary_cards(self, state: GameState):
        current_deck = [card for card in state.deck.cards]
        synergy_beneficiaries = []
        stuff = synergyBeneficiariesCardIdStrings()
        allowed_stuff = [e.value for e in CardId]

        for card in state.deck.cards:
            if card.id.lower() in stuff and card.id.lower() in allowed_stuff:
                synergy_beneficiaries.append(card.id.lower())

        return synergy_beneficiaries

    def get_max_key(self, initial_dict, tiebreaker_dict):
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
            # Get the first key in the sorted tiebreaker dictionary that appears in the list of keys with maximum value in the initial dictionary
            max_tiebreaker_key = next((k for k in sorted_tiebreaker_keys if k in max_keys), None)

            return max_tiebreaker_key

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



    def getScore(self, deck):
        score = 0
        deck_attributes = self.getDeck_attributes(deck)

        # Scoring for FLOWING_DECK_LENGTH
        if deck_attributes["FLOWING_DECK_LENGTH"] < 20:
            score += 0
        elif deck_attributes["FLOWING_DECK_LENGTH"] >= 50:
            score -= 3
        else:
            score += round(3 - ((deck_attributes["FLOWING_DECK_LENGTH"] - 20) / 10), 2)

        # Scoring for BASICS_AMOUNT
        basics_amount_score = round(3 - ((deck_attributes["BASICS_AMOUNT"] * 3) / 10), 2)
        score += basics_amount_score

        # Scoring for BASIC_RATIO
        basic_amount = deck_attributes["BASICS_AMOUNT"]
        deck_length = deck_attributes["DECK_LENGTH"]

        basic_ratio = basic_amount / deck_length

        basic_ratio_score = round(3 - (basic_ratio * 6), 2)
        score += basic_ratio_score

        # Scoring for CARD_TYPES
        attacks_percentage = deck_attributes["ATTACK"] / deck_attributes["DECK_LENGTH"]
        if attacks_percentage >= 0.7:
            score -= 3

        skills_percentage = deck_attributes["SKILL"] / deck_attributes["DECK_LENGTH"]
        if skills_percentage >= 0.6:
            score -= 3

        powers_percentage = deck_attributes["POWER"] / deck_attributes["DECK_LENGTH"]
        if powers_percentage >= 0.3:
            score -= 3

        # Scoring for UPGRADE_DENSITY
        upgrade_density_percentage = deck_attributes["UPGRADE_DENSITY"] / deck_attributes["DECK_LENGTH"]
        if upgrade_density_percentage == 1:
            score += 5
        elif upgrade_density_percentage == 0:
            score -= 5
        else:
            score += round(5 - (upgrade_density_percentage * 10), 2)

        if deck_attributes["AVERAGE_COST"] == 0:
            score += 2
        elif deck_attributes["AVERAGE_COST"] < 3:
            score += round(2 - (deck_attributes["AVERAGE_COST"] * 2 / 3), 2)
        else:
            score -= 2

        return round(score,2)



