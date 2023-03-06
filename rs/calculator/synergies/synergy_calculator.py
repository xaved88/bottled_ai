from rs.calculator.cards import CardId
from rs.calculator.synergies.synergy_beneficiaries import SynergyBeneficiaries
from rs.calculator.synergies.synergy_providers import SynergyProviders


def getSynergy(card, deck):

    deck_length = len(deck)
    if card in SynergyProviders:
        tags = SynergyProviders[card]

        # Count the number of times each tag appears in the beneficiaries
        final_count = {}
        for tag in tags:
            final_count[tag] = 0
            element_count = 0
            for element in deck:
                #print(element)
                if element in SynergyBeneficiaries:
                    for synergy in SynergyBeneficiaries.get(element):
                        #print(synergy)
                        if synergy == tag:
                            element_count += 1
                final_count[tag] = element_count
                #print(final_count)

        # Sum up the tag counts and return the result
        return sum(final_count.values()) / deck_length

