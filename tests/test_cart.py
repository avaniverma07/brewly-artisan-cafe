import unittest
from brewly.models import MenuItem
from brewly import cart


class TestCart(unittest.TestCase):

    def setUp(self):
        self.mocha = MenuItem("MOC01", "Mocha", "Mocha", 209, 4.8, "Choco espresso")
        self.latte = MenuItem("LAT01", "Latte", "Latte", 189, 4.7, "Smooth milk coffee")
        self.cart_dicts = []

    def test_add_new_item(self):
        cart.add_to_cart(self.cart_dicts, self.mocha, 2)
        self.assertEqual(len(self.cart_dicts), 1)
        self.assertEqual(self.cart_dicts[0]["quantity"], 2)

    def test_add_existing_item_increments_quantity(self):
        cart.add_to_cart(self.cart_dicts, self.mocha, 1)
        cart.add_to_cart(self.cart_dicts, self.mocha, 2)
        self.assertEqual(len(self.cart_dicts), 1)
        self.assertEqual(self.cart_dicts[0]["quantity"], 3)

    def test_update_quantity(self):
        cart.add_to_cart(self.cart_dicts, self.mocha, 1)
        cart.update_quantity(self.cart_dicts, "MOC01", 5)
        self.assertEqual(self.cart_dicts[0]["quantity"], 5)

    def test_update_quantity_to_zero_removes_item(self):
        cart.add_to_cart(self.cart_dicts, self.mocha, 1)
        cart.update_quantity(self.cart_dicts, "MOC01", 0)
        self.assertEqual(len(self.cart_dicts), 0)

    def test_remove_item(self):
        cart.add_to_cart(self.cart_dicts, self.mocha, 1)
        removed = cart.remove_from_cart(self.cart_dicts, "MOC01")
        self.assertTrue(removed)
        self.assertEqual(len(self.cart_dicts), 0)

    def test_remove_nonexistent_item(self):
        self.assertFalse(cart.remove_from_cart(self.cart_dicts, "XXX"))

    def test_cart_subtotal(self):
        cart.add_to_cart(self.cart_dicts, self.mocha, 2)   # 418
        cart.add_to_cart(self.cart_dicts, self.latte, 1)   # 189
        self.assertEqual(cart.cart_subtotal(self.cart_dicts), 607)

    def test_cart_item_count(self):
        cart.add_to_cart(self.cart_dicts, self.mocha, 2)
        cart.add_to_cart(self.cart_dicts, self.latte, 3)
        self.assertEqual(cart.cart_item_count(self.cart_dicts), 5)


if __name__ == "__main__":
    unittest.main()
