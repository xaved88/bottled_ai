from ai.requested_strike.rs_test_handler_fixture import RsTestHandlerFixture
from rs.ai.requested_strike.handlers.shop_purchase_handler import ShopPurchaseHandler


class ShopPurchaseHandlerTestCase(RsTestHandlerFixture):
    handler = ShopPurchaseHandler

    def test_buy_perfected_strike(self):
        self.execute_handler_tests('/shop/shop_buy_perfected_strike.json', ['choose 1', 'wait 30'])

    def test_handles_purge_already_used(self):
        self.execute_handler_tests('/shop/shop_purge_used.json', ['return', 'proceed'])

    def test_cant_afford_anything(self):
        self.execute_handler_tests('/shop/shop_nothing_to_buy.json', ['return', 'proceed'])

    def test_buy_upgraded_cards(self):
        self.execute_handler_tests('/shop/shop_buy_perfected_strike+.json', ['choose 1', 'wait 30'])

