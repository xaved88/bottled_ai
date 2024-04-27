from rs.calculator.card_cost import Cost
from rs.calculator.enums.card_id import CardId
from rs.calculator.interfaces.card_interface import CardInterface
from rs.game.card import CardType


class Card(CardInterface):
    def __init__(self, card_id: CardId, upgrade: int, cost: int, needs_target: bool, card_type: CardType,
                 ethereal: bool = False, exhausts: bool = False, uuid: str = "default"):
        self.id: CardId = card_id
        self.upgrade: int = upgrade
        self.cost: int = cost  # energy cost. Maybe -1 for no cost and not playable statuses?
        self.needs_target: bool = needs_target
        self.ethereal: bool = ethereal
        self.exhausts: bool = exhausts
        self.type: CardType = card_type
        self.uuid: str = uuid

    def get_state_string(self) -> str:
        return f"{self.id.value}{self.upgrade}{self.cost},"


def get_card(card_id: CardId, cost: int = None, upgrade: int = 0) -> Card:
    if card_id == CardId.STRIKE_R:
        return Card(card_id, upgrade, 1 if cost is None else cost, True, CardType.ATTACK)
    if card_id == CardId.DEFEND_R:
        return Card(card_id, upgrade, 1 if cost is None else cost, False, CardType.SKILL)
    if card_id == CardId.STRIKE_G:
        return Card(card_id, upgrade, 1 if cost is None else cost, True, CardType.ATTACK)
    if card_id == CardId.DEFEND_G:
        return Card(card_id, upgrade, 1 if cost is None else cost, False, CardType.SKILL)
    if card_id == CardId.STRIKE_P:
        return Card(card_id, upgrade, 1 if cost is None else cost, True, CardType.ATTACK)
    if card_id == CardId.DEFEND_P:
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
    if card_id == CardId.FIRE_BREATHING:
        return Card(card_id, upgrade, 1 if cost is None else cost, False, CardType.POWER)
    if card_id == CardId.EVOLVE:
        return Card(card_id, upgrade, 1 if cost is None else cost, False, CardType.POWER)
    if card_id == CardId.BERSERK:
        return Card(card_id, upgrade, 0 if cost is None else cost, False, CardType.POWER)
    if card_id == CardId.DEMON_FORM:
        return Card(card_id, upgrade, 3 if cost is None else cost, False, CardType.POWER)
    if card_id == CardId.INTIMIDATE:
        return Card(card_id, upgrade, 0 if cost is None else cost, False, CardType.SKILL, exhausts=True)
    if card_id == CardId.PUMMEL:
        return Card(card_id, upgrade, 1 if cost is None else cost, True, CardType.ATTACK, exhausts=True)
    if card_id == CardId.SEEING_RED:
        base_cost = 1 if not upgrade else 0
        return Card(card_id, upgrade, base_cost if cost is None else cost, False, CardType.SKILL, exhausts=True)
    if card_id == CardId.SHOCKWAVE:
        return Card(card_id, upgrade, 2 if cost is None else cost, False, CardType.SKILL, exhausts=True)
    if card_id == CardId.WHIRLWIND:
        return Card(card_id, upgrade, Cost.x_cost, False, CardType.ATTACK)
    if card_id == CardId.BLUDGEON:
        return Card(card_id, upgrade, 3 if cost is None else cost, True, CardType.ATTACK)
    if card_id == CardId.FEED:
        return Card(card_id, upgrade, 1 if cost is None else cost, True, CardType.ATTACK, exhausts=True)
    if card_id == CardId.FIEND_FIRE:
        return Card(card_id, upgrade, 2 if cost is None else cost, True, CardType.ATTACK, exhausts=True)
    if card_id == CardId.WOUND:
        return Card(card_id, 0, Cost.unplayable, False, CardType.STATUS)
    if card_id == CardId.DAZED:
        return Card(card_id, 0, Cost.unplayable, False, CardType.STATUS, ethereal=True)
    if card_id == CardId.VOID:
        return Card(card_id, 0, Cost.unplayable, False, CardType.STATUS, ethereal=True)
    if card_id == CardId.SLIMED:
        return Card(card_id, 0, 1 if cost is None else cost, False, CardType.STATUS, exhausts=True)
    if card_id == CardId.IMMOLATE:
        return Card(card_id, upgrade, 2 if cost is None else cost, False, CardType.ATTACK)
    if card_id == CardId.BURN:
        return Card(card_id, upgrade, Cost.unplayable, False, CardType.STATUS)
    if card_id == CardId.IMPERVIOUS:
        return Card(card_id, upgrade, 2 if cost is None else cost, False, CardType.SKILL, exhausts=True)
    if card_id == CardId.LIMIT_BREAK:
        return Card(card_id, upgrade, 1 if cost is None else cost, False, CardType.SKILL, exhausts=not upgrade)
    if card_id == CardId.OFFERING:
        return Card(card_id, upgrade, 0 if cost is None else cost, False, CardType.SKILL, exhausts=True)
    if card_id == CardId.JAX:
        return Card(card_id, upgrade, 0 if cost is None else cost, False, CardType.SKILL)
    if card_id == CardId.DRAW_FREE_EARLY:
        return Card(card_id, 0, Cost.unplayable, False, CardType.FAKE)
    if card_id == CardId.DRAW_FREE:
        return Card(card_id, 0, Cost.unplayable, False, CardType.FAKE)
    if card_id == CardId.DRAW_PAY_EARLY:
        return Card(card_id, 0, Cost.unplayable, False, CardType.FAKE)
    if card_id == CardId.DRAW_PAY:
        return Card(card_id, 0, Cost.unplayable, False, CardType.FAKE)
    if card_id == CardId.BODY_SLAM:
        base_cost = 1 if not upgrade else 0
        return Card(card_id, upgrade, base_cost if cost is None else cost, True, CardType.ATTACK)
    if card_id == CardId.CLASH:
        return Card(card_id, upgrade, 0 if cost is None else cost, True, CardType.ATTACK)
    if card_id == CardId.FLEX:
        return Card(card_id, upgrade, 0 if cost is None else cost, False, CardType.SKILL)
    if card_id == CardId.WILD_STRIKE:
        return Card(card_id, upgrade, 1 if cost is None else cost, True, CardType.ATTACK)
    if card_id == CardId.DOUBLE_TAP:
        return Card(card_id, upgrade, 1 if cost is None else cost, False, CardType.SKILL)
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
    if card_id == CardId.FEEL_NO_PAIN:
        return Card(card_id, upgrade, 1 if cost is None else cost, False, CardType.POWER)
    if card_id == CardId.DARK_EMBRACE:
        base_cost = 2 if not upgrade else 1
        return Card(card_id, upgrade, base_cost if cost is None else cost, False, CardType.POWER)
    if card_id == CardId.CORRUPTION:
        base_cost = 3 if not upgrade else 2
        return Card(card_id, upgrade, base_cost if cost is None else cost, False, CardType.POWER)
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
    if card_id == CardId.RITUAL_DAGGER:
        return Card(card_id, upgrade, 1 if cost is None else cost, True, CardType.ATTACK, exhausts=True)
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
        return Card(card_id, 0, Cost.unplayable, False, CardType.CURSE)
    if card_id == CardId.REGRET:
        return Card(card_id, 0, Cost.unplayable, False, CardType.CURSE)
    if card_id == CardId.DECAY:
        return Card(card_id, 0, Cost.unplayable, False, CardType.CURSE)
    if card_id == CardId.DOUBT:
        return Card(card_id, 0, Cost.unplayable, False, CardType.CURSE)
    if card_id == CardId.SHAME:
        return Card(card_id, 0, Cost.unplayable, False, CardType.CURSE)
    if card_id == CardId.CURSE_OF_THE_BELL:
        return Card(card_id, 0, Cost.unplayable, False, CardType.CURSE)
    if card_id == CardId.PARASITE:
        return Card(card_id, 0, Cost.unplayable, False, CardType.CURSE)
    if card_id == CardId.INJURY:
        return Card(card_id, 0, Cost.unplayable, False, CardType.CURSE)
    if card_id == CardId.ASCENDERS_BANE:
        return Card(card_id, 0, Cost.unplayable, False, CardType.CURSE, ethereal=True)
    if card_id == CardId.CLUMSY:
        return Card(card_id, 0, Cost.unplayable, False, CardType.CURSE, ethereal=True)
    if card_id == CardId.SEVER_SOUL:
        return Card(card_id, upgrade, 2 if cost is None else cost, True, CardType.ATTACK)
    if card_id == CardId.SECOND_WIND:
        return Card(card_id, upgrade, 1 if cost is None else cost, False, CardType.SKILL)

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
        return Card(card_id, upgrade, Cost.unplayable, False, CardType.SKILL)
    if card_id == CardId.REFLEX:
        return Card(card_id, upgrade, Cost.unplayable, False, CardType.SKILL)
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
    if card_id == CardId.GLASS_KNIFE:
        return Card(card_id, upgrade, 1 if cost is None else cost, True, CardType.ATTACK)
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
    if card_id == CardId.CALCULATED_GAMBLE:
        return Card(card_id, upgrade, 0 if cost is None else cost, False, CardType.SKILL,
                    exhausts=True if not upgrade else False)
    if card_id == CardId.BURST:
        return Card(card_id, upgrade, 1 if cost is None else cost, False, CardType.SKILL)

    # defect
    if card_id == CardId.STRIKE_B:
        return Card(card_id, upgrade, 1 if cost is None else cost, True, CardType.ATTACK)
    if card_id == CardId.DEFEND_B:
        return Card(card_id, upgrade, 1 if cost is None else cost, False, CardType.SKILL)
    if card_id == CardId.BEAM_CELL:
        return Card(card_id, upgrade, 0 if cost is None else cost, True, CardType.ATTACK)
    if card_id == CardId.LEAP:
        return Card(card_id, upgrade, 1 if cost is None else cost, False, CardType.SKILL)
    if card_id == CardId.CHARGE_BATTERY:
        return Card(card_id, upgrade, 1 if cost is None else cost, False, CardType.SKILL)
    if card_id == CardId.BUFFER:
        return Card(card_id, upgrade, 2 if cost is None else cost, False, CardType.POWER)
    if card_id == CardId.SKIM:
        return Card(card_id, upgrade, 1 if cost is None else cost, False, CardType.SKILL)
    if card_id == CardId.RIP_AND_TEAR:
        return Card(card_id, upgrade, 1 if cost is None else cost, False, CardType.ATTACK)
    if card_id == CardId.SWEEPING_BEAM:
        return Card(card_id, upgrade, 1 if cost is None else cost, False, CardType.ATTACK)
    if card_id == CardId.CORE_SURGE:
        return Card(card_id, upgrade, 1 if cost is None else cost, True, CardType.ATTACK, exhausts=True)
    if card_id == CardId.BOOT_SEQUENCE:
        return Card(card_id, upgrade, 0 if cost is None else cost, False, CardType.SKILL, exhausts=True)
    if card_id == CardId.STACK:
        return Card(card_id, upgrade, 1 if cost is None else cost, False, CardType.SKILL)
    if card_id == CardId.AUTO_SHIELDS:
        return Card(card_id, upgrade, 1 if cost is None else cost, False, CardType.SKILL)
    if card_id == CardId.STREAMLINE:
        return Card(card_id, upgrade, 2 if cost is None else cost, True, CardType.ATTACK)
    if card_id == CardId.TURBO:
        return Card(card_id, upgrade, 0 if cost is None else cost, False, CardType.SKILL)
    if card_id == CardId.AGGREGATE:
        return Card(card_id, upgrade, 0 if cost is None else cost, False, CardType.SKILL)
    if card_id == CardId.DOUBLE_ENERGY:
        base_cost = 1 if not upgrade else 0
        return Card(card_id, upgrade, base_cost if cost is None else cost, False, CardType.SKILL)
    if card_id == CardId.HEATSINKS:
        return Card(card_id, upgrade, 1 if cost is None else cost, False, CardType.POWER)
    if card_id == CardId.OVERCLOCK:
        return Card(card_id, upgrade, 0 if cost is None else cost, False, CardType.SKILL)
    if card_id == CardId.SELF_REPAIR:
        return Card(card_id, upgrade, 1 if cost is None else cost, False, CardType.POWER)
    if card_id == CardId.HELLO_WORLD:
        return Card(card_id, upgrade, 1 if cost is None else cost, False, CardType.POWER)
    if card_id == CardId.MAGNETISM:
        base_cost = 2 if not upgrade else 1
        return Card(card_id, upgrade, base_cost if cost is None else cost, False, CardType.POWER)
    if card_id == CardId.MACHINE_LEARNING:
        return Card(card_id, upgrade, 1 if cost is None else cost, False, CardType.POWER)
    if card_id == CardId.ELECTRODYNAMICS:
        return Card(card_id, upgrade, 2 if cost is None else cost, False, CardType.POWER)
    if card_id == CardId.DEFRAGMENT:
        return Card(card_id, upgrade, 1 if cost is None else cost, False, CardType.POWER)
    if card_id == CardId.BIASED_COGNITION:
        return Card(card_id, upgrade, 1 if cost is None else cost, False, CardType.POWER)
    if card_id == CardId.CAPACITOR:
        return Card(card_id, upgrade, 1 if cost is None else cost, False, CardType.POWER)
    if card_id == CardId.STORM:
        return Card(card_id, upgrade, 1 if cost is None else cost, False, CardType.POWER)
    if card_id == CardId.LOOP:
        return Card(card_id, upgrade, 1 if cost is None else cost, False, CardType.POWER)
    if card_id == CardId.CREATIVE_AI:
        base_cost = 3 if not upgrade else 2
        return Card(card_id, upgrade, base_cost if cost is None else cost, False, CardType.POWER)
    if card_id == CardId.ZAP:
        base_cost = 1 if not upgrade else 0
        return Card(card_id, upgrade, base_cost if cost is None else cost, False, CardType.SKILL)
    if card_id == CardId.DUALCAST:
        base_cost = 1 if not upgrade else 0
        return Card(card_id, upgrade, base_cost if cost is None else cost, False, CardType.SKILL)
    if card_id == CardId.BALL_LIGHTNING:
        return Card(card_id, upgrade, 1 if cost is None else cost, True, CardType.ATTACK)
    if card_id == CardId.COOLHEADED:
        return Card(card_id, upgrade, 1 if cost is None else cost, False, CardType.SKILL)
    if card_id == CardId.COLD_SNAP:
        return Card(card_id, upgrade, 1 if cost is None else cost, True, CardType.ATTACK)
    if card_id == CardId.DOOM_AND_GLOOM:
        return Card(card_id, upgrade, 2 if cost is None else cost, False, CardType.ATTACK)
    if card_id == CardId.ALL_FOR_ONE:
        return Card(card_id, upgrade, 2 if cost is None else cost, True, CardType.ATTACK)
    if card_id == CardId.GLACIER:
        return Card(card_id, upgrade, 2 if cost is None else cost, False, CardType.SKILL)
    if card_id == CardId.CONSUME:
        return Card(card_id, upgrade, 2 if cost is None else cost, False, CardType.SKILL)
    if card_id == CardId.CHILL:
        return Card(card_id, upgrade, 0 if cost is None else cost, False, CardType.SKILL, exhausts=True)
    if card_id == CardId.RAINBOW:
        return Card(card_id, upgrade, 2 if cost is None else cost, False, CardType.SKILL,
                    exhausts=True if not upgrade else False)
    if card_id == CardId.REPROGRAM:
        return Card(card_id, upgrade, 1 if cost is None else cost, False, CardType.SKILL)
    if card_id == CardId.RECURSION:
        base_cost = 1 if not upgrade else 0
        return Card(card_id, upgrade, base_cost if cost is None else cost, False, CardType.SKILL)
    if card_id == CardId.FUSION:
        base_cost = 2 if not upgrade else 1
        return Card(card_id, upgrade, base_cost if cost is None else cost, False, CardType.SKILL)
    if card_id == CardId.FISSION:
        return Card(card_id, upgrade, 0 if cost is None else cost, False, CardType.SKILL, exhausts=True)
    if card_id == CardId.REBOOT:
        return Card(card_id, upgrade, 0 if cost is None else cost, False, CardType.SKILL, exhausts=True)
    if card_id == CardId.GENETIC_ALGORITHM:
        return Card(card_id, upgrade, 1 if cost is None else cost, False, CardType.SKILL, exhausts=True)
    if card_id == CardId.BARRAGE:
        return Card(card_id, upgrade, 1 if cost is None else cost, True, CardType.ATTACK)
    if card_id == CardId.MELTER:
        return Card(card_id, upgrade, 1 if cost is None else cost, True, CardType.ATTACK)
    if card_id == CardId.METEOR_STRIKE:
        return Card(card_id, upgrade, 5 if cost is None else cost, True, CardType.ATTACK)
    if card_id == CardId.SUNDER:
        return Card(card_id, upgrade, 3 if cost is None else cost, True, CardType.ATTACK)
    if card_id == CardId.HYPERBEAM:
        return Card(card_id, upgrade, 2 if cost is None else cost, False, CardType.ATTACK)
    if card_id == CardId.BULLSEYE:
        return Card(card_id, upgrade, 1 if cost is None else cost, True, CardType.ATTACK)
    if card_id == CardId.COMPILE_DRIVER:
        return Card(card_id, upgrade, 1 if cost is None else cost, True, CardType.ATTACK)
    if card_id == CardId.ECHO_FORM:
        return Card(card_id, upgrade, 3 if cost is None else cost, False, CardType.POWER,
                    ethereal=True if not upgrade else False)
    if card_id == CardId.GO_FOR_THE_EYES:
        return Card(card_id, upgrade, 0 if cost is None else cost, True, CardType.ATTACK)
    if card_id == CardId.AMPLIFY:
        return Card(card_id, upgrade, 1 if cost is None else cost, False, CardType.SKILL)
    if card_id == CardId.CHAOS:
        return Card(card_id, upgrade, 1 if cost is None else cost, False, CardType.SKILL)
    if card_id == CardId.DARKNESS:
        return Card(card_id, upgrade, 1 if cost is None else cost, False, CardType.SKILL)
    if card_id == CardId.EQUILIBRIUM:
        return Card(card_id, upgrade, 2 if cost is None else cost, False, CardType.SKILL)
    if card_id == CardId.CLAW:
        return Card(card_id, upgrade, 0 if cost is None else cost, True, CardType.ATTACK)
    if card_id == CardId.STEAM_BARRIER:
        return Card(card_id, upgrade, 0 if cost is None else cost, False, CardType.SKILL)
    if card_id == CardId.FTL:
        return Card(card_id, upgrade, 0 if cost is None else cost, True, CardType.ATTACK)
    if card_id == CardId.SCRAPE:
        return Card(card_id, upgrade, 1 if cost is None else cost, True, CardType.ATTACK)
    if card_id == CardId.BLIZZARD:
        return Card(card_id, upgrade, 1 if cost is None else cost, False, CardType.ATTACK)
    if card_id == CardId.THUNDER_STRIKE:
        return Card(card_id, upgrade, 3 if cost is None else cost, False, CardType.ATTACK)

    # watcher
    if card_id == CardId.FLYING_SLEEVES:
        return Card(card_id, upgrade, 1 if cost is None else cost, True, CardType.ATTACK)
    if card_id == CardId.ESTABLISHMENT:
        return Card(card_id, upgrade, 1 if cost is None else cost, False, CardType.POWER)
    if card_id == CardId.BOWLING_BASH:
        return Card(card_id, upgrade, 1 if cost is None else cost, True, CardType.ATTACK)
    if card_id == CardId.CONSECRATE:
        return Card(card_id, upgrade, 0 if cost is None else cost, False, CardType.ATTACK)
    if card_id == CardId.CONCLUDE:
        return Card(card_id, upgrade, 1 if cost is None else cost, False, CardType.ATTACK)
    if card_id == CardId.RAGNAROK:
        return Card(card_id, upgrade, 3 if cost is None else cost, False, CardType.ATTACK)
    if card_id == CardId.INSIGHT:
        return Card(card_id, upgrade, 0 if cost is None else cost, False, CardType.SKILL, exhausts=True)
    if card_id == CardId.PROTECT:
        return Card(card_id, upgrade, 2 if cost is None else cost, False, CardType.SKILL)
    if card_id == CardId.SENTINEL:
        return Card(card_id, upgrade, 1 if cost is None else cost, False, CardType.SKILL)
    if card_id == CardId.SMITE:
        return Card(card_id, upgrade, 1 if cost is None else cost, True, CardType.ATTACK, exhausts=True)
