from rs.calculator.enums.card_id import CardId
from rs.calculator.powers import PowerId
from rs.calculator.relics import RelicId
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
print("Chars:    " + str(characters_implemented) + " (" + str(int(characters_implemented/characters_total*100)) + "%)")
print("Cards:  " + str(cards_implemented) + " (" + str(int(cards_implemented/cards_total*100)) + "%)" + " (for implemented chars: " + str(int(cards_implemented/(cards_per_character*characters_implemented+colorless_cards)*100)) + "%)")
print("Powers:  " + str(powers_implemented) + " (" + str(int(powers_implemented/powers_total*100)) + "%)")
print("Relics: " + str(relics_implemented) + " (" + str(int(relics_implemented/relics_total*100)) + "%)")
