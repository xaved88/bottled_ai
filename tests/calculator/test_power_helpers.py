from calculator.calculator_test_fixture import CalculatorTestFixture
from rs.calculator.powers import PowerId, get_power_count


class CalculatorPowersHelperTest(CalculatorTestFixture):

    def test_get_power_count(self):
        # given
        powers = dict()
        powers[PowerId.FLAME_BARRIER] = 2
        powers[PowerId.ACCURACY] = 3
        powers[PowerId.ANGRY] = 4
        # when
        count = get_power_count(powers, [PowerId.FLAME_BARRIER, PowerId.ACCURACY, PowerId.ARTIFACT])
        # then
        self.assertEqual(5, count)
