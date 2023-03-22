from enum import Enum


# NOT IMPLEMENTED
# 'blue candle'
# 'centennial puzzle'
# 'ectoplasm'  could take it into account when we do clever finishers
# 'gremlin horn'
# 'hovering kite'
# 'ink bottle'
# 'mercury hourglass'
# 'runic cube'
# 'sacred bark'
# 'tingsha'
# 'tough bandages'
# 'unceasing top'
# and several others that aren't listed yet


class RelicId(Enum):
    FAKE = 'fake'  # We make anything we don't know into this "fake" type

    ANCHOR = 'anchor'                               # We get block from state
    ART_OF_WAR = 'art of war'                       # We only look at current turn so far, so get this as bonus.
    BAG_OF_MARBLES = 'bag of marbles'               # N/A to battle calculations
    BLACK_STAR = 'black star'                       # N/A
    BLOOD_VIAL = 'blood vial'                       # N/A
    BLOODY_IDOL = 'bloody idol'                     # N/A (except for rare combo with hand of gold)
    BOTTLED_FLAME = 'bottled flame'                 # N/A
    BOTTLED_LIGHTNING = 'bottled lightning'         # N/A
    BOTTLED_TORNADO = 'bottled tornado'             # N/A
    BUSTED_CROWN = 'busted crown'                   # N/A
    CALLING_BELL = 'calling bell'                   # N/A
    CAPTAINS_WHEEL = 'captain\u0027s wheel'         # We get block from state
    CHAMPION_BELT = 'champion belt'
    COFFEE_DRIPPER = 'coffee dripper'               # N/A
    CURSED_KEY = 'cursed key'                       # N/A
    DREAM_CATCHER = 'dream catcher'                 # N/A
    DU_VU_DOLL = 'du-vu doll'                       # Covered by Strength knowledge
    EMPTY_CAGE = 'empty cage'                       # N/A
    ETERNAL_FEATHER = 'eternal feather'             # N/A
    FOSSILIZED_HELIX = 'fossilized helix'
    FROZEN_EGG = 'frozen egg'                       # N/A
    FUSION_HAMMER = 'fusion hammer'                 # N/A
    GOLDEN_IDOL = 'golden idol'                     # N/A
    HAPPY_FLOWER = 'happy flower'                   # We only look at current turn so far, so get this as bonus.
    HORN_CLEAT = 'horn cleat'                       # We get block from state
    ICE_CREAM = 'ice cream'                         # We only look at current turn so far, so get this as bonus.
    LETTER_OPENER = 'letter opener'
    LIZARD_TAIL = 'lizard tail'                     # N/A
    MANGO = 'mango'                                 # N/A
    MARK_OF_PAIN = 'mark of pain'                   # N/A
    MAW_BANK = 'maw bank'                           # N/A
    MEAL_TICKET = 'meal ticket'                     # N/A
    MOLTEN_EGG = 'molten egg'                       # N/A
    NUNCHAKU = 'nunchaku'
    PAPER_PHROG = 'paper phrog'
    PEAR = 'pear'                                   # N/A
    PHILOSOPHERS_STONE = 'philosopher\u0027s stone' # N/A
    PRESERVED_INSECT = 'preserved insect'           # N/A
    ODD_MUSHROOM = 'odd mushroom'
    ORICHALCUM = 'orichalcum'
    ORNAMENTAL_FAN = 'ornamental fan'
    PAPER_KRANE = 'paper krane'
    PEN_NIB = 'pen nib'
    RED_MASK = 'red mask'                           # N/A
    RING_OF_THE_SNAKE = 'ring of the snake'         # We know how many cards we've got
    RUNIC_DOME = 'runic dome'                       # We yolo everything since we see 0 incoming damage
    RUNIC_PYRAMID = 'runic pyramid'                 # But we don't keep in mind the implications for next turn
    SHOVEL = 'shovel'                               # N/A
    SINGING_BOWL = 'singing bowl'                   # N/A
    SLAVERS_COLLAR = 'slaver\u0027s collar'         # N/A
    SMILING_MASK = 'smiling mask'                   # N/A
    SNECKO_EYE = 'snecko eye'                       # Calculator reads the costs itself
    STRAWBERRY = 'strawberry'                       # N/A
    STRIKE_DUMMY = 'strike dummy'
    SUNDIAL = 'sundial'                             # We only look at current turn so far, so get this as bonus.
    THE_BOOT = 'the boot'
    TINY_CHEST = 'tiny chest'                       # N/A
    TORII = 'torii'
    TOXIC_EGG = 'toxic egg'                         # N/A
    TUNGSTEN_ROD = 'tungsten rod'
    VAJRA = 'vajra'                                 # Covered by Strength knowledge
    VELVET_CHOKER = 'velvet choker'
    WAR_PAINT = 'war paint'                         # N/A
    WARPED_TONGS = 'warped tongs'                   # Not relevant within a single turn
    WHITE_BEAST_STATUE = 'white beast statue'       # N/A
    WRIST_BLADE = 'wrist blade'


Relics = dict[RelicId: int]