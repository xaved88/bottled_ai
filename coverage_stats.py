from rs.calculator.enums.card_id import CardId
from rs.calculator.enums.power_id import PowerId
from rs.calculator.enums.relic_id import RelicId
from rs.machine.character import Character

characters_implemented = len(Character)
cards_implemented = len(CardId)
powers_implemented = len(PowerId)
relics_implemented = len(RelicId)

characters_total = 4

cards_per_character = 75
colorless_cards = 45
cards_total = cards_per_character * characters_total + colorless_cards

powers_total = 133
relics_total = 177

print("\n")
print("Implementation status:")
print(f"Chars:    {characters_implemented} ({int(characters_implemented/characters_total*100)}%)")
print(f"Cards:  {cards_implemented} ({int(cards_implemented/cards_total*100)}%)")
print(f"Powers: {powers_implemented} ({int(powers_implemented/powers_total*100)}%)")
print(f"Relics: {relics_implemented} ({int(relics_implemented/relics_total*100)}%)")
