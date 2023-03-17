from enum import Enum

from rs.game.card import CardType


class CardId(Enum):
    # PLACEHOLDER/LOGIC CARDS
    FAKE = 'fake'  # temp fake card for all the ones we don't know yet in game. Basically, treat like a wound.
    DRAW_FREE_EARLY = 'draw free early'
    DRAW_FREE = 'draw free'
    DRAW_PAY_EARLY = 'draw pay early'
    DRAW_PAY = 'draw pay'

    # REAL CARDS
    ANGER = 'anger'
    APOTHEOSIS = 'apotheosis'
    APPARITION = 'ghostly'
    BANDAGE_UP = 'bandage up'
    BASH = 'bash'
    BATTLE_TRANCE = 'battle trance'
    BLOODLETTING = 'bloodletting'
    BLOOD_FOR_BLOOD = 'blood for blood'
    BLUDGEON = 'bludgeon'
    BODY_SLAM = 'body slam'
    BURN = 'burn'
    BURNING_PACT = 'burning pact'
    CARNAGE = 'carnage'
    CLASH = 'clash'
    CLEAVE = 'cleave'
    CLOTHESLINE = 'clothesline'
    CLUMSY = 'clumsy'
    CURSEOFTHEBELL = 'curseofthebell'
    DARK_EMBRACE = 'dark embrace'
    DARK_SHACKLES = 'dark shackles'
    DAZED = 'dazed'
    DECAY = 'decay'
    DISARM = 'disarm'
    DRAMATIC_ENTRANCE = 'dramatic entrance'
    DROPKICK = 'dropkick'
    DEFEND_R = 'defend_r'
    DEFEND_G = 'defend_g'
    DOUBT = 'doubt'
    ENTRENCH = 'entrench'
    EVOLVE = 'evolve'
    FEED = 'feed'
    FIEND_FIRE = 'fiend fire'
    FIRE_BREATHING = 'fire breathing'
    FLAME_BARRIER = 'flame barrier'
    FLASH_OF_STEEL = 'flash of steel'
    FLEX = 'flex'
    GHOSTLY_ARMOR = 'ghostly armor'
    HAND_OF_GREED = 'handofgreed'
    HEAVY_BLADE = 'heavy blade'
    HEMOKINESIS = 'hemokinesis'
    IMMOLATE = 'immolate'
    IMPERVIOUS = 'impervious'
    INFLAME = 'inflame'
    INTIMIDATE = 'intimidate'
    IRON_WAVE = 'iron wave'
    INJURY = 'injury'
    JAX = 'j.a.x.'
    LIMIT_BREAK = 'limit break'
    MASTER_OF_STRATEGY = 'master of strategy'
    METALLICIZE = 'metallicize'
    NEUTRALIZE = 'neutralize'
    OFFERING = 'offering'
    PAIN = 'pain'
    PARASITE = 'parasite'
    PERFECTED_STRIKE = 'perfected strike'
    POISONED_STAB = 'poisoned stab'
    POMMEL_STRIKE = 'pommel strike'
    POWER_THROUGH = 'power through'
    PUMMEL = 'pummel'
    RAGE = 'rage'
    RAMPAGE = 'rampage'
    REAPER = 'reaper'
    REGRET = 'regret'
    RECKLESS_CHARGE = 'reckless charge'
    SEEING_RED = 'seeing red'
    SHOCKWAVE = 'shockwave'
    SHAME = 'shame'
    SHRUG_IT_OFF = 'shrug it off'
    SLIMED = 'slimed'
    SPOT_WEAKNESS = 'spot weakness'
    STRIKE_R = 'strike_r'
    STRIKE_G = 'strike_g'
    SURVIVOR = 'survivor'
    SWIFT_STRIKE = 'swift strike'
    THUNDERCLAP = 'thunderclap'
    TRIP = 'trip'
    TWIN_STRIKE = 'twin strike'
    UPPERCUT = 'uppercut'
    WILD_STRIKE = 'wild strike'
    WOUND = 'wound'

    """Adding New Ironclad cards for Synergy testing"""
    FEEL_NO_PAIN = 'feel no pain'

    """New Cards added"""

    SHIV = 'shiv'
    TERROR = 'terror'
    ADRENALINE = 'adrenaline'
    DIE_DIE_DIE = 'die die die'
    BLADE_DANCE = 'blade dance'
    CLOAK_AND_DAGGER = 'cloak and dagger'
    LEG_SWEEP = 'leg sweep'
    SUCKER_PUNCH = 'sucker punch'
    ESCAPE_PLAN = 'escape plan'
    HEEL_HOOK = 'heel hook'
    DAGGER_SPRAY = 'dagger spray'
    BACKSTAB = 'backstab'
    CALTROPS = 'caltrops'
    A_THOUSAND_CUTS = 'a thousand cuts'
    ACCURACY = 'accuracy'
    INFINITE_BLADES = 'infinite blades'
    AFTER_IMAGE = 'after image'

    FINESSE = 'finesse'


class Card:
    def __init__(self, card_id: CardId, upgrade: int, cost: int, needs_target: bool, card_type: CardType,
                 ethereal: bool = False, exhausts: bool = False):
        self.id: CardId = card_id
        self.upgrade: int = upgrade
        self.cost: int = cost  # energy cost. Maybe -1 for no cost and not playable statuses?
        self.needs_target: bool = needs_target
        self.ethereal: bool = ethereal
        self.exhausts: bool = exhausts
        self.type: CardType = card_type

    def get_state_string(self) -> str:
        return f"{self.id.value}+{self.upgrade}+{self.cost},"


def get_card(card_id: CardId, cost: int = None, upgrade: int = 0) -> Card:
    if card_id == CardId.DRAMATIC_ENTRANCE:
        return Card(card_id, upgrade, 0 if cost is None else cost, False, CardType.ATTACK)
    if card_id == CardId.STRIKE_R:
        return Card(card_id, upgrade, 1 if cost is None else cost, True, CardType.ATTACK)
    if card_id == CardId.DEFEND_R:
        return Card(card_id, upgrade, 1 if cost is None else cost, False, CardType.SKILL)
    if card_id == CardId.STRIKE_G:
        return Card(card_id, upgrade, 1 if cost is None else cost, True, CardType.ATTACK)
    if card_id == CardId.DEFEND_G:
        return Card(card_id, upgrade, 1 if cost is None else cost, False, CardType.SKILL)
    if card_id == CardId.BASH:
        return Card(card_id, upgrade, 2 if cost is None else cost, True, CardType.ATTACK)
    if card_id == CardId.ANGER:
        return Card(card_id, upgrade, 0 if cost is None else cost, True, CardType.ATTACK)
    if card_id == CardId.CLEAVE:
        return Card(card_id, upgrade, 1 if cost is None else cost, True, CardType.ATTACK)
    if card_id == CardId.CLOTHESLINE:
        return Card(card_id, upgrade, 2 if cost is None else cost, True, CardType.ATTACK)
    if card_id == CardId.HEAVY_BLADE:
        return Card(card_id, upgrade, 2 if cost is None else cost, True, CardType.ATTACK)
    if card_id == CardId.IRON_WAVE:
        return Card(card_id, upgrade, 1 if cost is None else cost, True, CardType.ATTACK)
    if card_id == CardId.PERFECTED_STRIKE:
        return Card(card_id, upgrade, 2 if cost is None else cost, True, CardType.ATTACK)
    if card_id == CardId.POMMEL_STRIKE:
        return Card(card_id, upgrade, 1 if cost is None else cost, True, CardType.ATTACK)
    if card_id == CardId.SHRUG_IT_OFF:
        return Card(card_id, upgrade, 1 if cost is None else cost, False, CardType.SKILL)
    if card_id == CardId.THUNDERCLAP:
        return Card(card_id, upgrade, 1 if cost is None else cost, True, CardType.ATTACK)
    if card_id == CardId.TWIN_STRIKE:
        return Card(card_id, upgrade, 1 if cost is None else cost, True, CardType.ATTACK)
    if card_id == CardId.BLOODLETTING:
        return Card(card_id, upgrade, 0 if cost is None else cost, False, CardType.SKILL)
    if card_id == CardId.BLOOD_FOR_BLOOD:
        base_cost = 4 if not upgrade else 3
        return Card(card_id, upgrade, base_cost if cost is None else cost, True, CardType.ATTACK)
    if card_id == CardId.CARNAGE:
        return Card(card_id, upgrade, 2 if cost is None else cost, True, CardType.ATTACK, ethereal=True)
    if card_id == CardId.UPPERCUT:
        return Card(card_id, upgrade, 2 if cost is None else cost, True, CardType.ATTACK)
    if card_id == CardId.DISARM:
        return Card(card_id, upgrade, 1 if cost is None else cost, True, CardType.SKILL, exhausts=True)
    if card_id == CardId.DROPKICK:
        return Card(card_id, upgrade, 1 if cost is None else cost, True, CardType.ATTACK)
    if card_id == CardId.ENTRENCH:
        base_cost = 2 if not upgrade else 1
        return Card(card_id, upgrade, base_cost if cost is None else cost, False, CardType.SKILL)
    if card_id == CardId.FLAME_BARRIER:
        return Card(card_id, upgrade, 2 if cost is None else cost, False, CardType.SKILL)
    if card_id == CardId.GHOSTLY_ARMOR:
        return Card(card_id, upgrade, 1 if cost is None else cost, False, CardType.SKILL, ethereal=True)
    if card_id == CardId.HEMOKINESIS:
        return Card(card_id, upgrade, 1 if cost is None else cost, True, CardType.ATTACK)
    if card_id == CardId.INFLAME:
        return Card(card_id, upgrade, 1 if cost is None else cost, False, CardType.POWER)
    if card_id == CardId.INTIMIDATE:
        return Card(card_id, upgrade, 0 if cost is None else cost, False, CardType.SKILL, exhausts=True)
    if card_id == CardId.PUMMEL:
        return Card(card_id, upgrade, 1 if cost is None else cost, True, CardType.ATTACK, exhausts=True)
    if card_id == CardId.SEEING_RED:
        base_cost = 1 if not upgrade else 0
        return Card(card_id, upgrade, base_cost if cost is None else cost, False, CardType.SKILL, exhausts=True)
    if card_id == CardId.SHOCKWAVE:
        return Card(card_id, upgrade, 2 if cost is None else cost, False, CardType.SKILL, exhausts=True)
    if card_id == CardId.BLUDGEON:
        return Card(card_id, upgrade, 3 if cost is None else cost, True, CardType.ATTACK)
    if card_id == CardId.FEED:
        return Card(card_id, upgrade, 1 if cost is None else cost, True, CardType.ATTACK, exhausts=True)
    if card_id == CardId.FIEND_FIRE:
        return Card(card_id, upgrade, 2 if cost is None else cost, True, CardType.ATTACK, exhausts=True)
    if card_id == CardId.WOUND:
        return Card(card_id, 0, -1, False, CardType.STATUS)
    if card_id == CardId.DAZED:
        return Card(card_id, 0, -1, False, CardType.STATUS, ethereal=True)
    if card_id == CardId.SLIMED:
        return Card(card_id, 0, 1 if cost is None else cost, False, CardType.STATUS, exhausts=True)
    if card_id == CardId.IMMOLATE:
        return Card(card_id, upgrade, 2 if cost is None else cost, False, CardType.ATTACK)
    if card_id == CardId.BURN:
        return Card(card_id, 0, -1, False, CardType.STATUS)
    if card_id == CardId.IMPERVIOUS:
        return Card(card_id, upgrade, 2 if cost is None else cost, False, CardType.SKILL, exhausts=True)
    if card_id == CardId.LIMIT_BREAK:
        return Card(card_id, upgrade, 1 if cost is None else cost, False, CardType.SKILL, exhausts=not upgrade)
    if card_id == CardId.OFFERING:
        return Card(card_id, upgrade, 0 if cost is None else cost, False, CardType.SKILL, exhausts=True)
    if card_id == CardId.JAX:
        return Card(card_id, upgrade, 0 if cost is None else cost, False, CardType.SKILL)
    if card_id == CardId.DRAW_FREE_EARLY:
        return Card(card_id, 0, -1, False, CardType.FAKE)
    if card_id == CardId.DRAW_FREE:
        return Card(card_id, 0, -1, False, CardType.FAKE)
    if card_id == CardId.DRAW_PAY_EARLY:
        return Card(card_id, 0, -1, False, CardType.FAKE)
    if card_id == CardId.DRAW_PAY:
        return Card(card_id, 0, -1, False, CardType.FAKE)
    if card_id == CardId.BODY_SLAM:
        base_cost = 1 if not upgrade else 0
        return Card(card_id, upgrade, base_cost if cost is None else cost, True, CardType.ATTACK)
    if card_id == CardId.CLASH:
        return Card(card_id, upgrade, 0 if cost is None else cost, True, CardType.ATTACK)
    if card_id == CardId.FLEX:
        return Card(card_id, upgrade, 0 if cost is None else cost, False, CardType.SKILL)
    if card_id == CardId.WILD_STRIKE:
        return Card(card_id, upgrade, 1 if cost is None else cost, True, CardType.ATTACK)
    if card_id == CardId.BATTLE_TRANCE:
        return Card(card_id, upgrade, 0 if cost is None else cost, False, CardType.SKILL)
    if card_id == CardId.RAGE:
        return Card(card_id, upgrade, 0 if cost is None else cost, False, CardType.SKILL)
    if card_id == CardId.RAMPAGE:
        return Card(card_id, upgrade, 1 if cost is None else cost, True, CardType.ATTACK)
    if card_id == CardId.METALLICIZE:
        return Card(card_id, upgrade, 1 if cost is None else cost, False, CardType.POWER)
    if card_id == CardId.RECKLESS_CHARGE:
        return Card(card_id, upgrade, 0 if cost is None else cost, True, CardType.ATTACK)
    if card_id == CardId.POWER_THROUGH:
        return Card(card_id, upgrade, 1 if cost is None else cost, False, CardType.SKILL)
    if card_id == CardId.SPOT_WEAKNESS:
        return Card(card_id, upgrade, 1 if cost is None else cost, True, CardType.SKILL)
    if card_id == CardId.REAPER:
        return Card(card_id, upgrade, 2 if cost is None else cost, False, CardType.ATTACK)
    if card_id == CardId.BANDAGE_UP:
        return Card(card_id, upgrade, 0 if cost is None else cost, False, CardType.SKILL)
    if card_id == CardId.DARK_SHACKLES:
        return Card(card_id, upgrade, 0 if cost is None else cost, False, CardType.SKILL, exhausts=True)
    if card_id == CardId.FLASH_OF_STEEL:
        return Card(card_id, upgrade, 0 if cost is None else cost, True, CardType.ATTACK)
    if card_id == CardId.SWIFT_STRIKE:
        return Card(card_id, upgrade, 0 if cost is None else cost, True, CardType.ATTACK)
    if card_id == CardId.TRIP:
        return Card(card_id, upgrade, 0 if cost is None else cost, True if not upgrade else False, CardType.SKILL)
    if card_id == CardId.APOTHEOSIS:
        base_cost = 2 if not upgrade else 1
        return Card(card_id, upgrade, base_cost if cost is None else cost, False, CardType.SKILL, exhausts=True)
    if card_id == CardId.HAND_OF_GREED:
        return Card(card_id, upgrade, 2 if cost is None else cost, True, CardType.ATTACK)
    if card_id == CardId.MASTER_OF_STRATEGY:
        return Card(card_id, upgrade, 0 if cost is None else cost, False, CardType.SKILL, exhausts=True)
    if card_id == CardId.APPARITION:
        return Card(card_id, upgrade, 1 if cost is None else cost, False, CardType.SKILL,
                    ethereal=True if not upgrade else False, exhausts=True)
    if card_id == CardId.PAIN:
        return Card(card_id, 0, -1, False, CardType.CURSE)
    if card_id == CardId.REGRET:
        return Card(card_id, 0, -1, False, CardType.CURSE)

    # Silent
    if card_id == CardId.NEUTRALIZE:
        return Card(card_id, upgrade, 0 if cost is None else cost, True, CardType.ATTACK)
    if card_id == CardId.SURVIVOR:
        return Card(card_id, upgrade, 1 if cost is None else cost, False, CardType.SKILL)
    if card_id == CardId.SHIV:
        return Card(card_id, upgrade, 0 if cost is None else cost, True, CardType.ATTACK, exhausts=True)
    if card_id == CardId.TERROR:
        base_cost = 1 if not upgrade else 0
        return Card(card_id, upgrade, base_cost if cost is None else cost, False, CardType.SKILL, exhausts=True)
    if card_id == CardId.ADRENALINE:
        return Card(card_id, upgrade, 0 if cost is None else cost, False, CardType.SKILL, exhausts=True)
    if card_id == CardId.DIE_DIE_DIE:
        return Card(card_id, upgrade, 1 if cost is None else cost, True, CardType.ATTACK, exhausts=True)
    if card_id == CardId.BLADE_DANCE:
        return Card(card_id, upgrade, 1 if cost is None else cost, False, CardType.SKILL)
    if card_id == CardId.CLOAK_AND_DAGGER:
        return Card(card_id, upgrade, 1 if cost is None else cost, False, CardType.SKILL)
    if card_id == CardId.LEG_SWEEP:
        return Card(card_id, upgrade, 2 if cost is None else cost, False, CardType.SKILL)
    if card_id == CardId.SUCKER_PUNCH:
        return Card(card_id, upgrade, 1 if cost is None else cost, True, CardType.ATTACK)
    if card_id == CardId.ESCAPE_PLAN:
        return Card(card_id, upgrade, 0 if cost is None else cost, False, CardType.SKILL)
    if card_id == CardId.HEEL_HOOK:
        return Card(card_id, upgrade, 1 if cost is None else cost, True, CardType.ATTACK)
    if card_id == CardId.DAGGER_SPRAY:
        return Card(card_id, upgrade, 1 if cost is None else cost, True, CardType.ATTACK)
    if card_id == CardId.BACKSTAB:
        return Card(card_id, upgrade, 0 if cost is None else cost, True, CardType.ATTACK, exhausts=True)
    if card_id == CardId.CALTROPS:
        return Card(card_id, upgrade, 1 if cost is None else cost, False, CardType.POWER)
    if card_id == CardId.A_THOUSAND_CUTS:
        return Card(card_id, upgrade, 2 if cost is None else cost, False, CardType.POWER)
    if card_id == CardId.ACCURACY:
        return Card(card_id, upgrade, 1 if cost is None else cost, False, CardType.POWER)
    if card_id == CardId.INFINITE_BLADES:
        return Card(card_id, upgrade, 1 if cost is None else cost, False, CardType.POWER)
    if card_id == CardId.AFTER_IMAGE:
        return Card(card_id, upgrade, 1 if cost is None else cost, False, CardType.POWER)
    if card_id == CardId.FINESSE:
        return Card(card_id, upgrade, 0 if cost is None else cost, False, CardType.SKILL)
    if card_id == CardId.FEEL_NO_PAIN:
        return Card(card_id, upgrade, 1 if cost is None else cost, False, CardType.POWER)
    if card_id == CardId.DARK_EMBRACE:
        base_cost = 2 if not upgrade else 1
        return Card(card_id, upgrade, base_cost if cost is None else cost, False, CardType.POWER)
    if card_id == CardId.BURNING_PACT:
        return Card(card_id, upgrade, 1 if cost is None else cost, False, CardType.SKILL)
    if card_id == CardId.EVOLVE:
        return Card(card_id, upgrade, 1 if cost is None else cost, False, CardType.POWER)
    if card_id == CardId.FIRE_BREATHING:
        return Card(card_id, upgrade, 1 if cost is None else cost, False, CardType.POWER)
    if card_id == CardId.INJURY:
        return Card(card_id, 0, -1, False, CardType.CURSE)
    if card_id == CardId.SHAME:
        return Card(card_id, 0, -1, False, CardType.CURSE)
    if card_id == CardId.DECAY:
        return Card(card_id, 0, -1, False, CardType.CURSE)
    if card_id == CardId.PARASITE:
        return Card(card_id, 0, -1, False, CardType.CURSE)
    if card_id == CardId.DOUBT:
        return Card(card_id, 0, -1, False, CardType.CURSE)
    if card_id == CardId.CURSEOFTHEBELL:
        return Card(card_id, 0, -1, False, CardType.CURSE)
    if card_id == CardId.CLUMSY:
        return Card(card_id, 0, -1, False, CardType.CURSE)
    if card_id == CardId.POISONED_STAB:
        return Card(card_id, upgrade, 1 if cost is None else cost, False, CardType.ATTACK)
