"""
menu.py
-------
FUNCTIONAL MODULE 2: Menu Browsing
Handles listing, filtering, searching and sorting coffee items.
Mirrors the Figma "Home" screen (categories + popular coffee grid).
"""

from brewly import data_manager as dm
from brewly.models import MenuItem
from brewly.utils import linear_search, selection_sort, find_maximum


def get_all_items():
    """Returns the full menu as a list of MenuItem objects."""
    data = dm.load_menu()
    return [MenuItem.from_dict(d) for d in data["items"]]


def get_categories():
    """Returns the unique list of categories, in first-seen order."""
    items = get_all_items()
    categories = []
    for item in items:
        if item.category not in categories:
            categories.append(item.category)
    return categories


def filter_by_category(category):
    items = get_all_items()
    return [i for i in items if i.category.lower() == category.lower()]


def find_item_by_id(item_id):
    """Uses the linear_search utility (Unit 5 array technique)."""
    items = get_all_items()
    return linear_search(items, item_id.upper(), key_fn=lambda i: i.item_id)


def search_by_name(keyword):
    keyword = keyword.lower().strip()
    return [i for i in get_all_items() if keyword in i.name.lower()]


def sort_by_price(items=None, descending=False):
    """Uses the hand-written selection_sort utility."""
    items = items if items is not None else get_all_items()
    return selection_sort(items, key_fn=lambda i: i.price, reverse=descending)


def most_expensive_item(items=None):
    items = items if items is not None else get_all_items()
    return find_maximum(items, key_fn=lambda i: i.price)
