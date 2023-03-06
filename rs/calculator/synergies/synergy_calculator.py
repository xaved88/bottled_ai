from rs.calculator.cards import CardId
from synergy_providers import SinergyProviders
from synergy_beneficiaries import SinergyBeneficiaries


def getSinergy(card):
    if card in SinergyProviders:
        tags = SinergyProviders[card]

        # Count the number of times each tag appears in the beneficiaries
        tag_counts = {}
        for tag in tags:
            tag_counts[tag] = 0
            for beneficiary_tags in SinergyBeneficiaries.values():
                tag_counts[tag] += beneficiary_tags.count(tag)

        # Sum up the tag counts and return the result
        print(sum(tag_counts.values()))


getSinergy(CardId.INFLAME)
