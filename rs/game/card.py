from enum import Enum


class Card:
    def __init__(self, json_map):
        self.exhausts: bool = json_map["exhausts"]
        self.is_playable: bool = False if "is_playable" not in json_map else json_map["is_playable"]
        self.cost: int = json_map["cost"]
        self.name: str = json_map["name"]
        self.id: str = json_map["id"]
        self.type: CardType = CardType(json_map["type"])
        self.ethereal: bool = json_map["ethereal"]
        self.uuid: str = json_map["uuid"]
        self.upgrades: int = json_map["upgrades"]
        self.rarity: CardRarity = CardRarity(json_map["rarity"])
        self.has_target: bool = json_map["has_target"]


class CardType(Enum):
    SKILL = "SKILL"
    ATTACK = "ATTACK"
    POWER = "POWER"
    STATUS = "STATUS"
    CURSE = "CURSE"
    FAKE = "FAKE"
    OTHER = "OTHER"


class CardRarity(Enum):
    BASIC = "BASIC"
    COMMON = "COMMON"
    UNCOMMON = "UNCOMMON"
    RARE = "RARE"
    SPECIAL = "SPECIAL"
    CURSE = "CURSE"
