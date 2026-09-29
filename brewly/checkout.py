"""
checkout.py
-----------
FUNCTIONAL MODULE 3 (continued): Checkout & Orders
Applies promo codes, computes delivery fee/total, and places the order.
Mirrors the Figma "Checkout" and "Order Successful" screens.
"""

from brewly import data_manager as dm
from brewly.models import Order
from brewly.cart import cart_subtotal
from brewly.utils import generate_order_id


class CheckoutError(Exception):
    pass


def apply_promo_code(subtotal, code):
    """
    Looks up the promo code in the menu data (dictionary lookup) and
    returns the discount amount. Raises CheckoutError if invalid.
    """
    menu_data = dm.load_menu()
    codes = menu_data.get("promo_codes", {})
    code = (code or "").strip().upper()

    if not code:
        return 0.0, None
    if code not in codes:
        raise CheckoutError(f"Promo code '{code}' is not valid.")

    promo = codes[code]
    if promo["type"] == "percent":
        discount = round(subtotal * promo["value"] / 100, 2)
    else:  # flat
        discount = min(promo["value"], subtotal)
    return discount, code


def calculate_delivery_fee(subtotal):
    menu_data = dm.load_menu()
    fee = menu_data.get("delivery_fee", 40)
    free_above = menu_data.get("free_delivery_above", 500)
    return 0 if subtotal >= free_above else fee


def compute_totals(cart_dicts, promo_code=None):
    """Returns a dict with subtotal, discount, delivery_fee, and total."""
    subtotal = cart_subtotal(cart_dicts)
    discount, applied_code = apply_promo_code(subtotal, promo_code) if promo_code else (0.0, None)
    delivery_fee = calculate_delivery_fee(subtotal - discount)
    total = round(subtotal - discount + delivery_fee, 2)
    return {
        "subtotal": subtotal,
        "discount": discount,
        "promo_code": applied_code,
        "delivery_fee": delivery_fee,
        "total": total,
    }


def place_order(user, cart_dicts, promo_code=None):
    """
    Finalizes an order: computes totals, saves the order record, awards
    loyalty ("Brew Points"), and clears the cart. Returns the Order object.
    """
    if not cart_dicts:
        raise CheckoutError("Your cart is empty.")

    totals = compute_totals(cart_dicts, promo_code)
    order = Order(
        order_id=generate_order_id(),
        username=user.username,
        items=cart_dicts.copy(),
        subtotal=totals["subtotal"],
        discount=totals["discount"],
        delivery_fee=totals["delivery_fee"],
        total=totals["total"],
        promo_code=totals["promo_code"],
    )

    orders_data = dm.load_orders()
    orders_data["orders"][order.order_id] = order.to_dict()
    dm.save_orders(orders_data)

    # Loyalty: 1 Brew Point per Rs.20 spent (simple integer division)
    user.brew_points += int(totals["total"] // 20)
    user.orders.append(order.order_id)
    cart_dicts.clear()

    return order


def get_order_history(user):
    orders_data = dm.load_orders()
    return [
        Order.from_dict(o) for o in orders_data["orders"].values()
        if o["username"] == user.username
    ]
