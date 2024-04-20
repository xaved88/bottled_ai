from typing import List

from rs.calculator.cards import Card
from rs.calculator.enums.card_id import CardId
from rs.calculator.battle_state import BattleState
from rs.calculator.enums.orb_id import OrbId
from rs.calculator.interfaces.card_interface import CardInterface
from rs.calculator.interfaces.powers import Powers
from rs.calculator.enums.power_id import PowerId
from rs.calculator.interfaces.relics import Relics
from rs.calculator.enums.relic_id import RelicId
from rs.calculator.player import Player
from rs.calculator.monster import Monster
from rs.game.card import CardType, Card as GameCard
from rs.helper.logger import log_calculator_missing_relic, log_calculator_missing_power, log_calculator_missing_card
from rs.machine.state import GameState

possible_card_ids = set(item.value for item in CardId)


def make_card(card: GameCard) -> CardInterface:
    card_id = card.id.lower()
    if card_id not in possible_card_ids:
        log_calculator_missing_card(card_id)
        return Card(CardId.FAKE, 0, -1, False, CardType.FAKE)
    return Card(
        card_id=CardId(card.id.lower()),
        # todo - some sort of logging here for ones we don't know. treat as wounds maybe? What about battle trance?
        upgrade=card.upgrades,
        cost=card.cost if card.is_playable else -1,
        needs_target=card.has_target,
        card_type=card.type,
        ethereal=card.ethereal,
        exhausts=card.exhausts,
        uuid=card.uuid,
    )


possible_relic_ids = set(item.value for item in RelicId)


def make_relic_id(relic_id: str) -> RelicId:
    if relic_id not in possible_relic_ids:
        log_calculator_missing_relic(relic_id)
        return RelicId.FAKE
    return RelicId(relic_id)


possible_power_ids = set(item.value for item in PowerId)


def make_power_id(power_id: str) -> PowerId:
    if power_id not in possible_power_ids:
        log_calculator_missing_power(power_id)
        return PowerId.FAKE
    return PowerId(power_id)


def make_powers(powers: List[dict]) -> Powers:
    out = {make_power_id(power['id'].lower()): (power['amount']) for power in powers}

    # custom counters
    echo_form_charge = [p['misc'] for p in powers if p['id'].lower() == "echo form" and 'misc' in p and p['misc'] > 0]
    if len(echo_form_charge):
        out[PowerId.INTERNAL_ECHO_FORM_READY] = echo_form_charge[0]

    return out


def create_battle_state(game_state: GameState) -> BattleState:
    # make sure it's in a usable battle state
    if not game_state.combat_state():
        return None

    cs = game_state.combat_state()

    # get relics
    relics: Relics = {
        make_relic_id(relic['name'].lower()): (relic['counter'])
        for relic in game_state.game_state()['relics']
    }

    # get player status
    player = Player(
        is_player=True,
        current_hp=cs['player']['current_hp'],
        max_hp=cs['player']['max_hp'],
        powers=make_powers(cs['player']['powers']),
        block=cs['player']['block'],
        energy=cs['player']['energy'],
        relics=relics,
    )

    # get enemies
    monsters = [
        Monster(
            is_player=False,
            current_hp=monster['current_hp'],
            max_hp=monster['max_hp'],
            block=monster['block'],
            powers=make_powers(monster['powers']),
            damage=monster['move_base_damage'] if 'move_base_damage' in monster else 0,
            hits=monster['move_hits'] if 'move_hits' in monster else 0,
            is_gone=False if not monster['is_gone'] else True,
        )
        for monster in cs['monsters']
    ]

    # get cards
    hand = [make_card(card) for card in game_state.hand.cards]
    draw_pile = [make_card(card) for card in game_state.draw_pile.cards]
    discard_pile = [make_card(card) for card in game_state.discard_pile.cards]
    exhaust_pile = [make_card(card) for card in game_state.exhaust_pile.cards]

    # get discard action state
    amount_to_discard = game_state.screen_state_max_cards()
    cards_discarded_this_turn = game_state.get_cards_discarded_this_turn()

    # get orbs
    orbs = [(OrbId(o.value), a) for o, a in game_state.get_player_orbs()]
    orb_slots = game_state.get_player_orb_slots()

    # get custom state
    memory_by_card = game_state.memory_by_card.copy()
    memory = game_state.memory.copy()

    return BattleState(player, hand, discard_pile, exhaust_pile, draw_pile, monsters, relics, amount_to_discard,
                       cards_discarded_this_turn, orbs=orbs, orb_slots=orb_slots, memory=memory,
                       memory_by_card=memory_by_card)
