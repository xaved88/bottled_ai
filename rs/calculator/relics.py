from enum import Enum


# NOT IMPLEMENTED
# 'blue candle' # uh we seem to use this one already despite not having it implemented, i guess because cost changes to 0 or so when we've got it. make sure comparator likes exhausting curses when we add this
# 'calipers'
# 'centennial puzzle'
# 'dead branch'
# 'ectoplasm'  could take it into account when we do clever finishers for not caring about hand of gold
# 'meat on the bone'
# 'mercury hourglass'
# 'mummified hand'
# 'runic cube'
# 'sacred bark'
# 'tingsha'
# and several others that aren't listed yet


class RelicId(Enum):
    FAKE = 'fake'  # We make anything we don't know into this "fake" type

    AKABEKO = 'akabeko'                             # Covered by Vigor
    ANCHOR = 'anchor'                               # We know current block
    ANCIENT_TEA_SET = 'ancient tea set'             # N/A to battle calculations
    ART_OF_WAR = 'art of war'                       # We only look at current turn so far, so get this as bonus.
    BAG_OF_MARBLES = 'bag of marbles'               # N/A
    BAG_OF_PREPARATION = 'bag of preparation'       # N/A
    BIRD_FACED_URN = 'bird-faced urn'
    BLACK_STAR = 'black star'                       # N/A
    BLOOD_VIAL = 'blood vial'                       # N/A
    BLOODY_IDOL = 'bloody idol'                     # N/A (except for rare combo with hand of gold)
    BOTTLED_FLAME = 'bottled flame'                 # N/A
    BOTTLED_LIGHTNING = 'bottled lightning'         # N/A
    BOTTLED_TORNADO = 'bottled tornado'             # N/A
    BRONZE_SCALES = 'bronze scales'                 # Covered by Thorns
    BURNING_BLOOD = 'burning blood'                 # N/A
    BUSTED_CROWN = 'busted crown'                   # N/A
    CALLING_BELL = 'calling bell'                   # N/A
    CAPTAINS_WHEEL = 'captain\u0027s wheel'         # We know current block
    CERAMIC_FISH = 'ceramic fish'                   # N/A
    CHAMPION_BELT = 'champion belt'
    COFFEE_DRIPPER = 'coffee dripper'               # N/A
    CURSED_KEY = 'cursed key'                       # N/A
    DARKSTONE_PERIAPT = 'darkstone periapt'         # N/A
    DREAM_CATCHER = 'dream catcher'                 # N/A
    DU_VU_DOLL = 'du-vu doll'                       # Covered by Strength
    EMPTY_CAGE = 'empty cage'                       # N/A
    ETERNAL_FEATHER = 'eternal feather'             # N/A
    FOSSILIZED_HELIX = 'fossilized helix'
    FROZEN_EGG = 'frozen egg'                       # N/A
    FUSION_HAMMER = 'fusion hammer'                 # N/A
    GAMBLING_CHIP = 'gambling chip'                 # Handled outside of calculator by a Discard Handler
    GINGER = 'ginger'                               # N/A
    GIRYA = 'girya'                                 # Covered by Strength
    GOLDEN_IDOL = 'golden idol'                     # N/A
    GREMLIN_HORN = 'gremlin horn'
    HAPPY_FLOWER = 'happy flower'                   # We only look at current turn so far, so get this as bonus.
    HORN_CLEAT = 'horn cleat'                       # We get block from state
    HOVERING_KITE = 'hovering kite'
    ICE_CREAM = 'ice cream'                         # We only look at current turn so far, so get this as bonus.
    INCENSE_BURNER = 'incense burner'               # We know about Intangible
    INK_BOTTLE = 'ink bottle'
    JUZU_BRACELET = 'juzu bracelet'                 # N/A
    KUNAI = 'kunai'
    LANTERN = 'lantern'                             # N/A
    LETTER_OPENER = 'letter opener'
    LIZARD_TAIL = 'lizard tail'                     # N/A
    MANGO = 'mango'                                 # N/A
    MARK_OF_PAIN = 'mark of pain'                   # N/A
    MATRYOSHKA = 'matryoshka'                       # N/A
    MAW_BANK = 'maw bank'                           # N/A
    MEAL_TICKET = 'meal ticket'                     # N/A
    MEMBERSHIP_CARD = 'membership card'             # N/A
    MOLTEN_EGG = 'molten egg'                       # N/A
    MUTAGENIC_STRENGTH = 'mutagenic strength'       # Covered by Strength
    NINJA_SCROLL = 'ninja scroll'                   # N/A
    NUNCHAKU = 'nunchaku'
    ODD_MUSHROOM = 'odd mushroom'
    ODDLY_SMOOTH_STONE = 'oddly smooth stone'       # Covered by Dexterity
    OLD_COIN = 'old coin'                           # N/A
    OMAMORI = 'omamori'                             # N/A
    ORICHALCUM = 'orichalcum'
    ORNAMENTAL_FAN = 'ornamental fan'
    PANTOGRAPH = 'pantograph'                       # N/A
    PAPER_KRANE = 'paper krane'
    PAPER_PHROG = 'paper phrog'
    PEAR = 'pear'                                   # N/A
    PEACE_PIPE = 'peace pipe'                       # N/A
    PEN_NIB = 'pen nib'
    PHILOSOPHERS_STONE = 'philosopher\u0027s stone' # N/A
    POTION_BELT = 'potion belt'                     # N/A
    PRAYER_WHEEL = 'prayer wheel'                   # N/A
    PRESERVED_INSECT = 'preserved insect'           # N/A
    QUESTION_CARD = 'question card'                 # N/A
    RED_MASK = 'red mask'                           # N/A
    REGAL_PILLOW = 'regal pillow'                   # N/A
    RING_OF_THE_SERPENT = 'ring of the serpent'     # N/A
    RING_OF_THE_SNAKE = 'ring of the snake'         # N/A
    RUNIC_DOME = 'runic dome'                       # We see 0 incoming damage so we yolo attack
    RUNIC_PYRAMID = 'runic pyramid'                 # N/A
    SHOVEL = 'shovel'                               # N/A
    SHURIKEN = 'shuriken'
    SINGING_BOWL = 'singing bowl'                   # N/A
    SLAVERS_COLLAR = 'slaver\u0027s collar'         # N/A
    SMILING_MASK = 'smiling mask'                   # N/A
    SNECKO_EYE = 'snecko eye'
    SNECKO_SKULL = 'snecko skull'
    SPIRIT_POOP = 'spirit poop'                     # N/A
    STONE_CALENDAR = 'stone calendar'
    STRAWBERRY = 'strawberry'                       # N/A
    STRIKE_DUMMY = 'strike dummy'
    SUNDIAL = 'sundial'                             # N/A
    THE_BOOT = 'the boot'
    THE_COURIER = 'the courier'                     # N/A
    THREAD_AND_NEEDLE = 'thread and needle'         # Covered by Plated Armor
    TINY_CHEST = 'tiny chest'                       # N/A
    TORII = 'torii'
    TOUGH_BANDAGES = 'tough bandages'
    TOXIC_EGG = 'toxic egg'                         # N/A
    TOY_ORNITHOPTER = 'toy ornithopter'             # N/A
    TUNGSTEN_ROD = 'tungsten rod'
    TURNIP = 'turnip'                               # N/A
    UNCEASING_TOP = 'unceasing top'
    VAJRA = 'vajra'                                 # Covered by Strength
    VELVET_CHOKER = 'velvet choker'
    WAR_PAINT = 'war paint'                         # N/A
    WARPED_TONGS = 'warped tongs'                   # Not relevant within a single turn
    WHETSTONE = 'whetstone'                         # N/A
    WHITE_BEAST_STATUE = 'white beast statue'       # N/A
    WRIST_BLADE = 'wrist blade'


Relics = dict[RelicId: int]