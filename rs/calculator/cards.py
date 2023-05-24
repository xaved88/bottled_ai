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
    A_THOUSAND_CUTS = 'a thousand cuts'
    ACCURACY = 'accuracy'
    ACROBATICS = 'acrobatics'
    ADRENALINE = 'adrenaline'
    AFTER_IMAGE = 'after image'
    ANGER = 'anger'
    APOTHEOSIS = 'apotheosis'
    APPARITION = 'ghostly'
    ASCENDERS_BANE = 'ascender\u0027s bane'
    BACKFLIP = 'backflip'
    BACKSTAB = 'backstab'
    BANDAGE_UP = 'bandage up'
    BANE = 'bane'
    BASH = 'bash'
    BATTLE_TRANCE = 'battle trance'
    BITE = 'bite'
    BLADE_DANCE = 'blade dance'
    BLIND = 'blind'
    BLOODLETTING = 'bloodletting'
    BLOOD_FOR_BLOOD = 'blood for blood'
    BLUDGEON = 'bludgeon'
    BLUR = 'blur'
    BODY_SLAM = 'body slam'
    BOUNCING_FLASK = 'bouncing flask'
    BULLET_TIME = 'bullet time'
    BURN = 'burn'
    CALTROPS = 'caltrops'
    CARNAGE = 'carnage'
    CATALYST = 'catalyst'
    CHOKE = 'choke'
    CLASH = 'clash'
    CLEAVE = 'cleave'
    CLOAK_AND_DAGGER = 'cloak and dagger'
    CLOTHESLINE = 'clothesline'
    CLUMSY = 'clumsy'
    CONCENTRATE = 'concentrate'
    CORPSE_EXPLOSION = 'corpse explosion'
    CURSE_OF_THE_BELL = 'curseofthebell'  # Weird id alert!
    CRIPPLING_CLOUD = 'crippling poison'
    DAGGER_THROW = 'dagger throw'
    DAGGER_SPRAY = 'dagger spray'
    DARK_SHACKLES = 'dark shackles'
    DASH = 'dash'
    DAZED = 'dazed'
    DEADLY_POISON = 'deadly poison'
    DECAY = 'decay'
    DEEP_BREATH = 'deep breath'
    DEFEND_R = 'defend_r'
    DEFEND_G = 'defend_g'
    DEFLECT = 'deflect'
    DIE_DIE_DIE = 'die die die'
    DISARM = 'disarm'
    DRAMATIC_ENTRANCE = 'dramatic entrance'
    DROPKICK = 'dropkick'
    DODGE_AND_ROLL = 'dodge and roll'
    DOUBT = 'doubt'
    ENDLESS_AGONY = 'endless agony'  # Note: the special bits of this card aren't relevant for our current calculator.
    ENLIGHTENMENT = 'enlightenment'
    ENTRENCH = 'entrench'
    ENVENOM = 'envenom'
    ESCAPE_PLAN = 'escape plan'
    EVISCERATE = 'eviscerate'
    EXPERTISE = 'expertise'
    FEED = 'feed'
    FIEND_FIRE = 'fiend fire'
    FINESSE = 'finesse'
    FINISHER = 'finisher'  # Note: with current bot setup we can't easily remember how many attacks we've played this turn since we recalculate all paths after each card play, so this card is mostly useless as is.
    FLAME_BARRIER = 'flame barrier'
    FLASH_OF_STEEL = 'flash of steel'
    FLECHETTES = 'flechettes'
    FLEX = 'flex'
    FLYING_KNEE = 'flying knee'
    FOOTWORK = 'footwork'
    GHOSTLY_ARMOR = 'ghostly armor'
    GOOD_INSTINCTS = 'good instincts'
    GRAND_FINALE = 'grand finale'
    HAND_OF_GREED = 'handofgreed'  # Weird id alert!
    HEAVY_BLADE = 'heavy blade'
    HEEL_HOOK = 'heel hook'
    HEMOKINESIS = 'hemokinesis'
    IMMOLATE = 'immolate'
    IMPATIENCE = 'impatience'
    IMPERVIOUS = 'impervious'
    INFINITE_BLADES = 'infinite blades'
    INFLAME = 'inflame'
    INJURY = 'injury'
    INTIMIDATE = 'intimidate'
    IRON_WAVE = 'iron wave'
    JAX = 'j.a.x.'
    JUGGERNAUT = 'juggernaut'
    LEG_SWEEP = 'leg sweep'
    LIMIT_BREAK = 'limit break'
    MASTER_OF_STRATEGY = 'master of strategy'
    MAYHEM = 'mayhem'
    METALLICIZE = 'metallicize'
    MIND_BLAST = 'mind blast'
    NEUTRALIZE = 'neutralize'
    NOXIOUS_FUMES = 'noxious fumes'
    OFFERING = 'offering'
    OUTMANEUVER = 'outmaneuver'
    PAIN = 'pain'
    PANACEA = 'panacea'
    PANACHE = 'panache'  # We currently have damage provided by triggering the Panache power hardcoded to 10. It's the first power we've run into that has multiple values associated with it.
    PARASITE = 'parasite'
    PERFECTED_STRIKE = 'perfected strike'
    PHANTASMAL_KILLER = 'phantasmal killer'
    PIERCING_WAIL = 'piercing wail'
    POISONED_STAB = 'poisoned stab'
    POMMEL_STRIKE = 'pommel strike'
    POWER_THROUGH = 'power through'
    PREDATOR = 'predator'
    PREPARED = 'prepared'
    PUMMEL = 'pummel'
    QUICK_SLASH = 'quick slash'
    RAGE = 'rage'
    RAMPAGE = 'rampage'
    REAPER = 'reaper'
    REFLEX = 'reflex'
    REGRET = 'regret'
    RECKLESS_CHARGE = 'reckless charge'
    RIDDLE_WITH_HOLES = 'riddle with holes'
    SADISTIC_NATURE = 'sadistic nature'
    SEEING_RED = 'seeing red'
    SHAME = 'shame'
    SHIV = 'shiv'
    SHOCKWAVE = 'shockwave'
    SHRUG_IT_OFF = 'shrug it off'
    SLICE = 'slice'
    SLIMED = 'slimed'
    SNEAKY_STRIKE = 'underhanded strike'  # Weird id alert!
    SPOT_WEAKNESS = 'spot weakness'
    STORM_OF_STEEL = 'storm of steel'
    STRIKE_R = 'strike_r'
    STRIKE_G = 'strike_g'
    SUCKER_PUNCH = 'sucker punch'
    SURVIVOR = 'survivor'
    SWIFT_STRIKE = 'swift strike'
    SWORD_BOOMERANG = 'sword boomerang'
    TACTICIAN = 'tactician'
    TERROR = 'terror'
    TOOLS_OF_THE_TRADE = 'tools of the trade'
    THUNDERCLAP = 'thunderclap'
    TRIP = 'trip'
    TWIN_STRIKE = 'twin strike'
    UNLOAD = 'unload'
    UPPERCUT = 'uppercut'
    VOID = 'void'
    WILD_STRIKE = 'wild strike'
    WOUND = 'wound'
    WRAITH_FORM = 'wraith form v2'  # Weird id alert!


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
    if card_id == CardId.VOID:
        return Card(card_id, 0, -1, False, CardType.STATUS, ethereal=True)
    if card_id == CardId.SLIMED:
        return Card(card_id, 0, 1 if cost is None else cost, False, CardType.STATUS, exhausts=True)
    if card_id == CardId.IMMOLATE:
        return Card(card_id, upgrade, 2 if cost is None else cost, False, CardType.ATTACK)
    if card_id == CardId.BURN:
        return Card(card_id, upgrade, -1, False, CardType.STATUS)
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
    if card_id == CardId.SWORD_BOOMERANG:
        return Card(card_id, upgrade, 1 if cost is None else cost, False, CardType.ATTACK)
    if card_id == CardId.JUGGERNAUT:
        return Card(card_id, upgrade, 2 if cost is None else cost, False, CardType.POWER)
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
    if card_id == CardId.BLIND:
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
    if card_id == CardId.DEEP_BREATH:
        return Card(card_id, upgrade, 0 if cost is None else cost, False, CardType.SKILL)
    if card_id == CardId.ENLIGHTENMENT:
        return Card(card_id, upgrade, 0 if cost is None else cost, False, CardType.SKILL)
    if card_id == CardId.IMPATIENCE:
        return Card(card_id, upgrade, 0 if cost is None else cost, False, CardType.SKILL)
    if card_id == CardId.MAYHEM:
        base_cost = 2 if not upgrade else 1
        return Card(card_id, upgrade, base_cost if cost is None else cost, False, CardType.POWER)
    if card_id == CardId.PANACHE:
        return Card(card_id, upgrade, 0 if cost is None else cost, False, CardType.POWER)
    if card_id == CardId.SADISTIC_NATURE:
        return Card(card_id, upgrade, 0 if cost is None else cost, False, CardType.POWER)



    if card_id == CardId.PAIN:
        return Card(card_id, 0, -1, False, CardType.CURSE)
    if card_id == CardId.REGRET:
        return Card(card_id, 0, -1, False, CardType.CURSE)
    if card_id == CardId.DECAY:
        return Card(card_id, 0, -1, False, CardType.CURSE)
    if card_id == CardId.DOUBT:
        return Card(card_id, 0, -1, False, CardType.CURSE)
    if card_id == CardId.SHAME:
        return Card(card_id, 0, -1, False, CardType.CURSE)
    if card_id == CardId.CURSE_OF_THE_BELL:
        return Card(card_id, 0, -1, False, CardType.CURSE)
    if card_id == CardId.PARASITE:
        return Card(card_id, 0, -1, False, CardType.CURSE)
    if card_id == CardId.INJURY:
        return Card(card_id, 0, -1, False, CardType.CURSE)
    if card_id == CardId.ASCENDERS_BANE:
        return Card(card_id, 0, -1, False, CardType.CURSE, ethereal=True)
    if card_id == CardId.CLUMSY:
        return Card(card_id, 0, -1, False, CardType.CURSE, ethereal=True)

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
        return Card(card_id, upgrade, 2 if cost is None else cost, True, CardType.SKILL)
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
    if card_id == CardId.DRAMATIC_ENTRANCE:
        return Card(card_id, upgrade, 0 if cost is None else cost, False, CardType.ATTACK)
    if card_id == CardId.POISONED_STAB:
        return Card(card_id, upgrade, 1 if cost is None else cost, True, CardType.ATTACK)
    if card_id == CardId.TOOLS_OF_THE_TRADE:
        base_cost = 1 if not upgrade else 0
        return Card(card_id, upgrade, base_cost if cost is None else cost, False, CardType.POWER)
    if card_id == CardId.STORM_OF_STEEL:
        return Card(card_id, upgrade, 1 if cost is None else cost, False, CardType.SKILL)
    if card_id == CardId.EVISCERATE:
        return Card(card_id, upgrade, 3 if cost is None else cost, True, CardType.ATTACK)
    if card_id == CardId.SNEAKY_STRIKE:
        return Card(card_id, upgrade, 2 if cost is None else cost, True, CardType.ATTACK)
    if card_id == CardId.PREPARED:
        return Card(card_id, upgrade, 0 if cost is None else cost, False, CardType.SKILL)
    if card_id == CardId.DAGGER_THROW:
        return Card(card_id, upgrade, 1 if cost is None else cost, True, CardType.ATTACK)
    if card_id == CardId.UNLOAD:
        return Card(card_id, upgrade, 1 if cost is None else cost, True, CardType.ATTACK)
    if card_id == CardId.FOOTWORK:
        return Card(card_id, upgrade, 1 if cost is None else cost, False, CardType.POWER)
    if card_id == CardId.RIDDLE_WITH_HOLES:
        return Card(card_id, upgrade, 2 if cost is None else cost, True, CardType.ATTACK)
    if card_id == CardId.DEFLECT:
        return Card(card_id, upgrade, 0 if cost is None else cost, False, CardType.SKILL)
    if card_id == CardId.DASH:
        return Card(card_id, upgrade, 2 if cost is None else cost, True, CardType.ATTACK)
    if card_id == CardId.SLICE:
        return Card(card_id, upgrade, 0 if cost is None else cost, True, CardType.ATTACK)
    if card_id == CardId.QUICK_SLASH:
        return Card(card_id, upgrade, 1 if cost is None else cost, True, CardType.ATTACK)
    if card_id == CardId.CRIPPLING_CLOUD:
        return Card(card_id, upgrade, 2 if cost is None else cost, False, CardType.SKILL, exhausts=True)
    if card_id == CardId.BITE:
        return Card(card_id, upgrade, 1 if cost is None else cost, True, CardType.ATTACK)
    if card_id == CardId.PANACEA:
        return Card(card_id, upgrade, 0 if cost is None else cost, False, CardType.SKILL, exhausts=True)
    if card_id == CardId.MIND_BLAST:
        base_cost = 2 if not upgrade else 1
        return Card(card_id, upgrade, base_cost if cost is None else cost, True, CardType.ATTACK)
    if card_id == CardId.GOOD_INSTINCTS:
        return Card(card_id, upgrade, 0 if cost is None else cost, False, CardType.SKILL)
    if card_id == CardId.ACROBATICS:
        return Card(card_id, upgrade, 1 if cost is None else cost, False, CardType.SKILL)
    if card_id == CardId.BACKFLIP:
        return Card(card_id, upgrade, 1 if cost is None else cost, False, CardType.SKILL)
    if card_id == CardId.DEADLY_POISON:
        return Card(card_id, upgrade, 1 if cost is None else cost, True, CardType.SKILL)
    if card_id == CardId.TACTICIAN:
        return Card(card_id, upgrade, -1, False, CardType.SKILL)
    if card_id == CardId.REFLEX:
        return Card(card_id, upgrade, -1, False, CardType.SKILL)
    if card_id == CardId.CONCENTRATE:
        return Card(card_id, upgrade, 0 if cost is None else cost, False, CardType.SKILL)
    if card_id == CardId.FLECHETTES:
        return Card(card_id, upgrade, 1 if cost is None else cost, True, CardType.ATTACK)
    if card_id == CardId.EXPERTISE:
        return Card(card_id, upgrade, 1 if cost is None else cost, False, CardType.SKILL)
    if card_id == CardId.BANE:
        return Card(card_id, upgrade, 1 if cost is None else cost, True, CardType.ATTACK)
    if card_id == CardId.BULLET_TIME:
        base_cost = 3 if not upgrade else 2
        return Card(card_id, upgrade, base_cost if cost is None else cost, False, CardType.SKILL)
    if card_id == CardId.CHOKE:
        return Card(card_id, upgrade, 2 if cost is None else cost, True, CardType.ATTACK)
    if card_id == CardId.FLYING_KNEE:
        return Card(card_id, upgrade, 1 if cost is None else cost, True, CardType.ATTACK)
    if card_id == CardId.PREDATOR:
        return Card(card_id, upgrade, 2 if cost is None else cost, True, CardType.ATTACK)
    if card_id == CardId.DODGE_AND_ROLL:
        return Card(card_id, upgrade, 1 if cost is None else cost, False, CardType.SKILL)
    if card_id == CardId.OUTMANEUVER:
        return Card(card_id, upgrade, 1 if cost is None else cost, False, CardType.SKILL)
    if card_id == CardId.ENVENOM:
        base_cost = 2 if not upgrade else 1
        return Card(card_id, upgrade, base_cost if cost is None else cost, False, CardType.POWER)
    if card_id == CardId.NOXIOUS_FUMES:
        return Card(card_id, upgrade, 1 if cost is None else cost, False, CardType.POWER)
    if card_id == CardId.FINISHER:
        return Card(card_id, upgrade, 1 if cost is None else cost, True, CardType.ATTACK)
    if card_id == CardId.ENDLESS_AGONY:
        return Card(card_id, upgrade, 0 if cost is None else cost, True, CardType.ATTACK, exhausts=True)
    if card_id == CardId.CORPSE_EXPLOSION:
        return Card(card_id, upgrade, 2 if cost is None else cost, True, CardType.SKILL)
    if card_id == CardId.GRAND_FINALE:
        return Card(card_id, upgrade, 0 if cost is None else cost, True, CardType.ATTACK)
    if card_id == CardId.WRAITH_FORM:
        return Card(card_id, upgrade, 3 if cost is None else cost, False, CardType.POWER)
    if card_id == CardId.PIERCING_WAIL:
        return Card(card_id, upgrade, 1 if cost is None else cost, False, CardType.SKILL, exhausts=True)
    if card_id == CardId.BLUR:
        return Card(card_id, upgrade, 1 if cost is None else cost, False, CardType.SKILL)
    if card_id == CardId.CATALYST:
        return Card(card_id, upgrade, 1 if cost is None else cost, True, CardType.SKILL, exhausts=True)
    if card_id == CardId.BOUNCING_FLASK:
        return Card(card_id, upgrade, 2 if cost is None else cost, False, CardType.SKILL)
    if card_id == CardId.PHANTASMAL_KILLER:
        base_cost = 1 if not upgrade else 0
        return Card(card_id, upgrade, base_cost if cost is None else cost, False, CardType.SKILL)
