from rs.calculator.cards import CardId
from rs.calculator.synergies.synergy_beneficiaries import SynergyBeneficiaries
from rs.calculator.synergies.synergy_providers import SynergyProviders


def getSynergy(card):
    if card in SynergyProviders:
        tags = SynergyProviders[card]

        # Count the number of times each tag appears in the beneficiaries
        tag_counts = {}
        for tag in tags:
            tag_counts[tag] = 0
            for beneficiary_tags in SynergyBeneficiaries.values():
                tag_counts[tag] += beneficiary_tags.count(tag)

        # Sum up the tag counts and return the result
        print(sum(tag_counts.values()))

