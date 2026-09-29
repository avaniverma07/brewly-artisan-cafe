import unittest
from brewly.models import MenuItem
from brewly import cart, checkout


class TestCheckout(unittest.TestCase):

    def setUp(self):
        self.mocha = MenuItem("MOC01", "Mocha", "Mocha", 209, 4.8, "Choco espresso")
        self.cart_dicts = []
        cart.add_to_cart(self.cart_dicts, self.mocha, 3)  # subtotal = 627

    def test_totals_without_promo(self):
        totals = checkout.compute_totals(self.cart_dicts)
        self.assertEqual(totals["subtotal"], 627)
        self.assertEqual(totals["discount"], 0.0)
        self.assertEqual(totals["delivery_fee"], 0)    # 627 already crosses the Rs.500 free-delivery mark
        self.assertEqual(totals["total"], 627)

    def test_totals_with_percent_promo(self):
        totals = checkout.compute_totals(self.cart_dicts, "BREW10")
        self.assertEqual(totals["discount"], 62.7)
        self.assertEqual(totals["promo_code"], "BREW10")

    def test_invalid_promo_raises(self):
        with self.assertRaises(checkout.CheckoutError):
            checkout.compute_totals(self.cart_dicts, "NOTREAL")

    def test_free_delivery_above_threshold(self):
        cart.add_to_cart(self.cart_dicts, self.mocha, 2)  # total qty 5 -> subtotal 1045
        totals = checkout.compute_totals(self.cart_dicts)
        self.assertEqual(totals["delivery_fee"], 0)

    def test_place_order_empty_cart_raises(self):
        with self.assertRaises(checkout.CheckoutError):
            checkout.place_order(_FakeUser(), [], None)


class _FakeUser:
    """Minimal stand-in for a User, just for the empty-cart test."""
    username = "ghost"
    orders = []
    brew_points = 0


if __name__ == "__main__":
    unittest.main()
