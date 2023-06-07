from ai.common.co_test_handler_fixture import CoTestHandlerFixture
from rs.common.handlers.common_transform_handler import CommonTransformHandler


class TestPurgeHandler(CoTestHandlerFixture):
    handler = CommonTransformHandler

    def test_transform(self):
        self.execute_handler_tests('/other/transform_strike.json', ['wait 30', 'choose 4', 'wait 30', 'proceed', 'wait 30'])
