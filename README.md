# Brewly Artisan Café - Coffee Ordering CLI Application

> A command-line coffee ordering system, built for **CSE1021 - Introduction
> to Problem Solving and Programming**.
>
> Brewly Artisan Café (brand: BREWLY) began as a UI/UX design in Figma ("BREWLY - Find your favourite
> coffee") and has been re-implemented here as a fully working, terminal-based
> Python application so that it demonstrates the programming concepts taught
> in this course: data types, control flow, functions, lists/tuples/
> dictionaries, and fundamental algorithms.

---

## 1. Overview

BREWLY lets a user create an account, browse a coffee menu by category,
search and sort items, add items to a cart, apply promo codes, check out,
and track order history and loyalty ("Brew Points") — all from the
terminal, with data persisted locally in JSON files.

## 2. Features

- **User Management** — create account, sign in, guest browsing (no
  duplicate accounts, validated email, hashed passwords)
- **Menu Browsing** — list all items, filter by category, keyword search,
  sort by price (ascending/descending) using a hand-written selection sort
- **Cart Management** — add / update quantity / remove items, live subtotal
- **Checkout** — promo code validation (percentage or flat discount),
  automatic free-delivery threshold, order confirmation
- **Favourites** — save items for quick access later
- **Order History & Profile** — view past orders and loyalty "Brew Points"
- **Persistent storage** — all data is saved to JSON files so progress
  survives between runs

## 3. Technologies / Tools Used

| Tool | Purpose |
|---|---|
| Python 3.8+ | Core language (standard library only — no external packages) |
| `json` | Data persistence (menu, users, orders) |
| `hashlib` | Password hashing |
| `uuid` | Unique order ID generation |
| `unittest` | Automated testing |
| Figma | Original UI/UX design reference (see `docs/`) |

No third-party packages are required — see `requirements.txt`.

## 4. Project Structure

```
brewly-artisan-cafe/
├── main.py                # CLI entry point
├── brewly/
│   ├── __init__.py
│   ├── models.py           # MenuItem, CartItem, User, Order classes
│   ├── data_manager.py      # JSON load/save helpers
│   ├── auth.py              # Module 1: user management
│   ├── menu.py               # Module 2: menu browsing/search/sort
│   ├── cart.py                 # Module 3a: cart operations
│   ├── checkout.py             # Module 3b: promo codes, totals, orders
│   ├── utils.py                 # Shared algorithms (search, sort, kth-smallest, etc.)
│   └── data/
│       └── menu.json              # Seed data: menu items + promo codes
├── tests/
│   ├── test_utils.py
│   ├── test_cart.py
│   └── test_checkout.py
├── docs/
│   └── DESIGN.md            # Architecture, workflow, UML & ER diagrams
├── statement.md
├── requirements.txt
└── README.md
```

## 5. Steps to Install & Run

### Prerequisites
- Python 3.8 or higher installed
- No internet connection or extra packages required

### Setup

```bash
# 1. Clone the repository
git clone https://github.com/<your-username>/brewly-artisan-cafe.git
cd brewly-artisan-cafe

# 2. (Optional) create a virtual environment
python3 -m venv venv
source venv/bin/activate      # On Windows: venv\Scripts\activate

# 3. No dependencies to install — BREWLY only uses the Python standard library
```

### Run the application

```bash
python3 main.py
```

You will see a text menu. Example first run:

```
Welcome to BREWLY - your favourite coffee, one command away.

============================================
  BREWLY | Find your favourite coffee
============================================
1. Sign in
2. Create an Account
3. Continue as Guest
0. Exit
Choose an option:
```

Follow the on-screen prompts — everything is menu-driven (type a number and
press Enter).

## 6. Instructions for Testing

The project includes a `unittest` suite covering the algorithm utilities,
cart operations, and checkout/promo-code logic (25 test cases).

```bash
# From the project root
python3 -m unittest discover -s tests -v
```

Expected output ends with:
```
Ran 25 tests in 0.00Xs

OK
```

### Manual test walkthrough
1. Run `python3 main.py`
2. Choose `2` to create an account and follow the prompts
3. From Home, choose `1` and enter an item ID (e.g. `MOC01`) to view a
   product and add it to your cart
4. Choose `5` to view your cart, then `6` to checkout
5. Try promo code `BREW10` (10% off) or `FLAT50` (flat Rs.50 off)
6. Confirm the order and check `9` (Order History) and `8` (Profile) to see
   your Brew Points

## 7. Sample Data

`brewly/data/menu.json` ships with 10 coffee items across 5 categories
(Espresso, Latte, Cappuccino, Mocha, Cold Brew) and 3 sample promo codes
(`BREW10`, `FLAT50`, `FIRSTCUP`). `users.json` and `orders.json` are created
automatically on first run and are gitignored.

## 8. Original Design Reference

The original Figma UI/UX design that this CLI's flow and screens are based
on is referenced in the project report (screens: Welcome, Sign Up/In, Home,
Product Detail, Cart, Checkout, Order Success, Favourites, Profile).

## 9. Author

Built as an Evaluated Course Project for CSE1021 - Introduction to Problem
Solving and Programming.
