"""
models.py
---------
Defines the core data structures used across the BREWLY application.

Course concept mapping:
    - Demonstrates use of classes as compound data types (an alternative
      to plain dictionaries), constructors, instance methods, and
      converting between objects <-> dictionaries for JSON storage.
"""

from datetime import datetime


class MenuItem:
    """Represents a single coffee item on the menu."""

    def __init__(self, item_id, name, category, price, rating=0.0, description=""):
        self.item_id = item_id
        self.name = name
        self.category = category
        self.price = price
        self.rating = rating
        self.description = description

    def to_dict(self):
        return {
            "id": self.item_id,
            "name": self.name,
            "category": self.category,
            "price": self.price,
            "rating": self.rating,
            "description": self.description,
        }

    @staticmethod
    def from_dict(d):
        return MenuItem(
            item_id=d["id"],
            name=d["name"],
            category=d["category"],
            price=d["price"],
            rating=d.get("rating", 0.0),
            description=d.get("description", ""),
        )

    def __str__(self):
        return f"[{self.item_id}] {self.name} ({self.category}) - Rs.{self.price} | {self.rating}*"


class CartItem:
    """Represents one line item inside a user's cart (item + quantity)."""

    def __init__(self, menu_item: MenuItem, quantity: int = 1):
        self.menu_item = menu_item
        self.quantity = quantity

    @property
    def subtotal(self):
        return round(self.menu_item.price * self.quantity, 2)

    def to_dict(self):
        return {"item": self.menu_item.to_dict(), "quantity": self.quantity}

    @staticmethod
    def from_dict(d):
        return CartItem(menu_item=MenuItem.from_dict(d["item"]), quantity=d["quantity"])

    def __str__(self):
        return f"{self.menu_item.name} x{self.quantity} = Rs.{self.subtotal}"


class User:
    """Represents a registered BREWLY customer."""

    def __init__(self, username, email, password_hash, phone="",
                 favorites=None, brew_points=0, cart=None, orders=None):
        self.username = username
        self.email = email
        self.password_hash = password_hash
        self.phone = phone
        self.favorites = favorites if favorites is not None else []   # list of item_ids
        self.brew_points = brew_points
        self.cart = cart if cart is not None else []                  # list of CartItem dicts
        self.orders = orders if orders is not None else []             # list of order ids

    def to_dict(self):
        return {
            "username": self.username,
            "email": self.email,
            "password_hash": self.password_hash,
            "phone": self.phone,
            "favorites": self.favorites,
            "brew_points": self.brew_points,
            "cart": self.cart,
            "orders": self.orders,
        }

    @staticmethod
    def from_dict(d):
        return User(
            username=d["username"],
            email=d["email"],
            password_hash=d["password_hash"],
            phone=d.get("phone", ""),
            favorites=d.get("favorites", []),
            brew_points=d.get("brew_points", 0),
            cart=d.get("cart", []),
            orders=d.get("orders", []),
        )


class Order:
    """Represents a placed order."""

    def __init__(self, order_id, username, items, subtotal, discount,
                 delivery_fee, total, promo_code=None, timestamp=None):
        self.order_id = order_id
        self.username = username
        self.items = items                # list of CartItem dicts
        self.subtotal = subtotal
        self.discount = discount
        self.delivery_fee = delivery_fee
        self.total = total
        self.promo_code = promo_code
        self.timestamp = timestamp or datetime.now().isoformat(timespec="seconds")

    def to_dict(self):
        return {
            "order_id": self.order_id,
            "username": self.username,
            "items": self.items,
            "subtotal": self.subtotal,
            "discount": self.discount,
            "delivery_fee": self.delivery_fee,
            "total": self.total,
            "promo_code": self.promo_code,
            "timestamp": self.timestamp,
        }

    @staticmethod
    def from_dict(d):
        return Order(**d)
