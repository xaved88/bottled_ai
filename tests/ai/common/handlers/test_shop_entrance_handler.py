from ai.common.co_test_handler_fixture import CoTestHandlerFixture
from rs.common.handlers.common_shop_entrance_handler import CommonShopEntranceHandler


class TestShopEntranceHandler(CoTestHandlerFixture):
    handler = CommonShopEntranceHandler

    def test_shop_entrance(self):
        self.execute_handler_tests('/shop/shop_entrance.json', ['choose shop', 'wait 30'])
