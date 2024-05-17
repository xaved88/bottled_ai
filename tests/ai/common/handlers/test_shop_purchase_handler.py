from ai.common.co_test_handler_fixture import CoTestHandlerFixture
from rs.ai._example.handlers.shop_purchase_handler import ShopPurchaseHandler


class ShopPurchaseHandlerTestCase(CoTestHandlerFixture):
    handler = ShopPurchaseHandler

    def test_buy_perfected_strike(self):
        self.execute_handler_tests('/shop/shop_buy_perfected_strike.json', ['choose 1', 'wait 30'])

    def test_handles_purge_already_used(self):
        self.execute_handler_tests('/shop/shop_purge_used.json', ['return', 'proceed'])

    def test_cant_afford_anything(self):
        self.execute_handler_tests('/shop/shop_nothing_to_buy.json', ['return', 'proceed'])

    def test_buy_upgraded_cards(self):
        self.execute_handler_tests('/shop/shop_buy_perfected_strike+.json', ['choose 1', 'wait 30'])

    def test_do_not_purge_because_no_removable_curses(self):
        self.execute_handler_tests('/shop/shop_do_not_purge_because_no_removable_curses.json', ['choose 9', 'wait 30'])

    def test_purge_even_though_first_curse_is_not_removable(self):
        self.execute_handler_tests('/shop/shop_purge_because_one_removable_curse_among_not_removable.json',
                                   ['choose 0', 'wait 30'])
