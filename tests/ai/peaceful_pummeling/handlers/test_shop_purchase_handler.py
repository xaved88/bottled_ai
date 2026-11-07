from ai.peaceful_pummeling.pp_test_handler_fixture import PpTestHandlerFixture
from rs.ai.peaceful_pummeling.handlers.shop_purchase_handler import ShopPurchaseHandler


class ShopPurchaseHandlerTestCase(PpTestHandlerFixture):
    handler = ShopPurchaseHandler

    def test_buy_lantern_in_localized_shop(self):
        # zh UI: names in choice_list are unusable ("??"); the purchase target must be
        # located by numeric index (purge slot + affordable-items order), not by name.
        self.execute_handler_tests('shop/shop_zh_buy_lantern.json', ['choose 9', 'wait 30'])
