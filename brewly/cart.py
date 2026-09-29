"""
cart.py
-------
FUNCTIONAL MODULE 3: Cart Management
CRUD operations on a user's cart. Mirrors the Figma "Your Cart" and
"Added to your Cart" screens.
"""

from brewly.models import CartItem
from brewly.utils import summation


def _find_cart_line(cart_dicts, item_id):
    for idx, line in enumerate(cart_dicts):
        if line["item"]["id"] == item_id:
            return idx
    return -1


def add_to_cart(cart_dicts, menu_item, quantity=1):
    """
    Adds a MenuItem to the cart (list of dicts, as stored on the User).
    If it already exists, increments the quantity instead of duplicating
    the line (a small "remove duplicates" style guard).
    """
    idx = _find_cart_line(cart_dicts, menu_item.item_id)
    if idx != -1:
        cart_dicts[idx]["quantity"] += quantity
    else:
        cart_dicts.append(CartItem(menu_item, quantity).to_dict())
    return cart_dicts


def update_quantity(cart_dicts, item_id, new_quantity):
    idx = _find_cart_line(cart_dicts, item_id)
    if idx == -1:
        return False
    if new_quantity <= 0:
        cart_dicts.pop(idx)
    else:
        cart_dicts[idx]["quantity"] = new_quantity
    return True


def remove_from_cart(cart_dicts, item_id):
    idx = _find_cart_line(cart_dicts, item_id)
    if idx == -1:
        return False
    cart_dicts.pop(idx)
    return True


def cart_subtotal(cart_dicts):
    """Uses the summation() utility over each line's subtotal."""
    line_totals = [d["item"]["price"] * d["quantity"] for d in cart_dicts]
    return summation(line_totals)


def cart_item_count(cart_dicts):
    return summation([d["quantity"] for d in cart_dicts])


def clear_cart(cart_dicts):
    cart_dicts.clear()
    return cart_dicts
