"""
Brewly Artisan Café (BREWLY) - Coffee Ordering CLI Application
=========================================
A command-line coffee ordering system built for CSE1021
(Introduction to Problem Solving and Programming).

Package contents:
    models.py        -> Core data structures (User, MenuItem, CartItem, Order)
    data_manager.py   -> JSON-based persistence layer (load/save)
    auth.py           -> User registration, login, session handling
    menu.py           -> Menu browsing, searching, sorting algorithms
    cart.py           -> Cart operations (add/remove/update)
    checkout.py       -> Promo codes, totals, order placement
    utils.py          -> Small reusable algorithms (search, sort, dedup, etc.)
"""

__version__ = "1.0.0"
__author__ = "BREWLY Project - CSE1021"
