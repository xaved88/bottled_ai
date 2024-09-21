from enum import Enum


# NOT IMPLEMENTED
# 'blue candle' # we seem to play this correctly without it being implemented because game adjusts the state correctly.
# we should adjust the comparisons a bit to make sure we're more aggressively exhausting curses when this is available.
# 'centennial puzzle'
# 'dead branch'
# 'ectoplasm'  could take it into account when we do clever finishers for not caring about hand of gold
# 'meat on the bone'
# 'melange' # there would suddenly be a bunch of 'shuffle the draw pile' actions from e.g. cards to suddenly take into account
# 'mummified hand'
# 'runic cube'
# 'sacred bark'
# 'dolly's mirror'
# 'ssserpent head' should go into map handler I guess
# 'brimstone' - probably need to be more aggressive when we have this
# and several others that aren't listed yet


class RelicId(Enum):
    FAKE = 'fake'  # We make anything we don't know into this "fake" type

    AKABEKO = 'akabeko'                             # Covered by Vigor power
    ANCHOR = 'anchor'                               # We know current block
    ANCIENT_TEA_SET = 'ancient tea set'             # N/A to battle calculations
    ART_OF_WAR = 'art of war'                       # We only look at current turn so far, so get this as bonus.
    ASTROLABE = 'astrolabe'                         # N/A
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
    CALIPERS = 'calipers'
    CALLING_BELL = 'calling bell'                   # N/A
    CAPTAINS_WHEEL = 'captain\u0027s wheel'         # We know current block
    CAULDRON = 'cauldron'                           # N/A
    CERAMIC_FISH = 'ceramic fish'                   # N/A
    CHAMPION_BELT = 'champion belt'
    CHARONS_ASHES = 'charon\u0027s ashes'
    CHEMICAL_X = 'chemical x'
    CIRCLET = 'circlet'                             # N/A
    CLOAK_CLASP = 'cloak clasp'                     # N/A
    CLOCKWORK_SOUVENIR = 'clockwork souvenir'       # N/A
    COFFEE_DRIPPER = 'coffee dripper'               # N/A
    CULTIST_HEADPIECE = 'cultist headpiece'         # N/A
    CRACKED_CORE = 'cracked core'
    CURSED_KEY = 'cursed key'                       # N/A
    DAMARU = 'damaru'
    DARKSTONE_PERIAPT = 'darkstone periapt'         # N/A
    DATA_DISK = 'data disk'                         # N/A
    DREAM_CATCHER = 'dream catcher'                 # N/A
    DUALITY = 'duality'
    DU_VU_DOLL = 'du-vu doll'                       # Covered by Strength
    ENCHIRIDION = 'enchiridion'                     # N/A
    EMPTY_CAGE = 'empty cage'                       # N/A
    EMOTION_CHIP = 'emotion chip'                   # N/A unless we choose to care about it in a comparator
    ETERNAL_FEATHER = 'eternal feather'             # N/A
    FACE_OF_CLERIC = 'face of cleric'               # N/A
    FOSSILIZED_HELIX = 'fossilized helix'
    FROZEN_CORE = 'frozen core'
    FROZEN_EGG = 'frozen egg'                       # N/A
    FUSION_HAMMER = 'fusion hammer'                 # N/A
    GAMBLING_CHIP = 'gambling chip'                 # Handled outside of calculator by a Discard Handler
    GINGER = 'ginger'                               # N/A
    GIRYA = 'girya'                                 # Covered by Strength
    GOLD_PLATED_CABLES = 'gold-plated cables'
    GOLDEN_EYE = 'golden eye'
    GOLDEN_IDOL = 'golden idol'                     # N/A
    GREMLIN_HORN = 'gremlin horn'
    GREMLIN_VISAGE = 'gremlin visage'               # N/A
    HAPPY_FLOWER = 'happy flower'                   # We only look at current turn so far, so get this as bonus.
    HAND_DRILL = 'hand drill'
    HOLY_WATER = 'holy water'                       # N/A
    HORN_CLEAT = 'horn cleat'                       # We get block from state
    HOVERING_KITE = 'hovering kite'
    ICE_CREAM = 'ice cream'
    INCENSE_BURNER = 'incense burner'               # We know about Intangible
    INK_BOTTLE = 'ink bottle'
    INSERTER = 'inserter'                           # N/A (triggers at start of turn)
    JUZU_BRACELET = 'juzu bracelet'                 # N/A
    KUNAI = 'kunai'
    LANTERN = 'lantern'                             # N/A
    LEES_WAFFLE = 'lee\u0027s waffle'               # N/A
    LETTER_OPENER = 'letter opener'
    LIZARD_TAIL = 'lizard tail'
    MAGIC_FLOWER = 'magic flower'
    MANGO = 'mango'                                 # N/A
    MARK_OF_PAIN = 'mark of pain'                   # N/A
    MARK_OF_THE_BLOOM = 'mark of the bloom'
    MATRYOSHKA = 'matryoshka'                       # N/A
    MAW_BANK = 'maw bank'                           # N/A
    MEAL_TICKET = 'meal ticket'                     # N/A
    MEDICAL_KIT = 'medical kit'
    MEMBERSHIP_CARD = 'membership card'             # N/A
    MERCURY_HOURGLASS = 'mercury hourglass'         # We only look at current turn so far, so get this as bonus.
    MOLTEN_EGG = 'molten egg'                       # N/A
    MUTAGENIC_STRENGTH = 'mutagenic strength'       # Covered by Strength
    NECRONOMICON = 'necronomicon'
    NINJA_SCROLL = 'ninja scroll'                   # N/A
    NLOTHS_HUNGRY_FACE = 'n\u0027loth\u0027s hungry face' # N/A
    NUCLEAR_BATTERY = 'nuclear battery'             # N/A
    NUNCHAKU = 'nunchaku'
    ODD_MUSHROOM = 'odd mushroom'
    ODDLY_SMOOTH_STONE = 'oddly smooth stone'       # Covered by Dexterity
    OLD_COIN = 'old coin'                           # N/A
    OMAMORI = 'omamori'                             # N/A
    ORANGE_PELLETS = 'orange pellets'
    ORICHALCUM = 'orichalcum'
    ORNAMENTAL_FAN = 'ornamental fan'
    ORREY = 'orrey'                                 # N/A
    PANDORAS_BOX = 'pandora\u0027s box'             # N/A
    PANTOGRAPH = 'pantograph'                       # N/A
    PAPER_KRANE = 'paper krane'
    PAPER_PHROG = 'paper phrog'
    PEAR = 'pear'                                   # N/A
    PEACE_PIPE = 'peace pipe'                       # N/A
    PEN_NIB = 'pen nib'
    PHILOSOPHERS_STONE = 'philosopher\u0027s stone' # N/A
    POTION_BELT = 'potion belt'                     # N/A
    PRESERVED_INSECT = 'preserved insect'           # N/A
    PRISMATIC_SHARD = 'prismatic shard'             # N/A
    PURE_WATER = 'pure water'                       # N/A
    QUESTION_CARD = 'question card'                 # N/A
    RED_MASK = 'red mask'                           # N/A
    REGAL_PILLOW = 'regal pillow'                   # N/A
    RING_OF_THE_SERPENT = 'ring of the serpent'     # N/A
    RING_OF_THE_SNAKE = 'ring of the snake'         # N/A
    RUNIC_CAPACITOR = 'runic capacitor'             # N/A
    RUNIC_DOME = 'runic dome'                       # We see 0 incoming damage so we yolo attack
    RUNIC_PYRAMID = 'runic pyramid'
    SHOVEL = 'shovel'                               # N/A
    SHURIKEN = 'shuriken'
    SINGING_BOWL = 'singing bowl'                   # N/A
    SLAVERS_COLLAR = 'slaver\u0027s collar'         # N/A
    SLING_OF_COURAGE = 'sling of courage'           # N/A
    SMILING_MASK = 'smiling mask'                   # N/A
    SNECKO_EYE = 'snecko eye'
    SNECKO_SKULL = 'snecko skull'
    SPIRIT_POOP = 'spirit poop'                     # N/A
    STONE_CALENDAR = 'stone calendar'
    STRAWBERRY = 'strawberry'                       # N/A
    STRIKE_DUMMY = 'strike dummy'
    SUNDIAL = 'sundial'
    SYMBIOTIC_VIRUS = 'symbiotic virus'             # N/A
    TEARDROP_LOCKET = 'teardrop locket'
    THE_ABACUS = 'the abacus'
    THE_BOOT = 'the boot'
    THE_COURIER = 'the courier'                     # N/A
    THREAD_AND_NEEDLE = 'thread and needle'         # Covered by Plated Armor
    TINGSHA = 'tingsha'
    TINY_CHEST = 'tiny chest'                       # N/A
    TINY_HOUSE = 'tiny house'                       # N/A
    TORII = 'torii'
    TOUGH_BANDAGES = 'tough bandages'
    TOXIC_EGG = 'toxic egg'                         # N/A
    TUNGSTEN_ROD = 'tungsten rod'
    TURNIP = 'turnip'                               # N/A
    TWISTED_FUNNEL = 'twisted funnel'               # N/A
    UNCEASING_TOP = 'unceasing top'
    VAJRA = 'vajra'                                 # Covered by Strength
    VELVET_CHOKER = 'velvet choker'
    VIOLET_LOTUS = 'violet lotus'
    WAR_PAINT = 'war paint'                         # N/A
    WARPED_TONGS = 'warped tongs'                   # Not relevant within a single turn
    WHETSTONE = 'whetstone'                         # N/A
    WHITE_BEAST_STATUE = 'white beast statue'       # N/A
    WRIST_BLADE = 'wrist blade'
