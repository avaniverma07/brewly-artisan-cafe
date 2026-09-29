"""
data_manager.py
---------------
A tiny persistence layer that reads and writes JSON files.
This keeps file I/O (a syllabus topic: input/output structure) in one
place, separate from business logic.
"""

import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")

MENU_FILE = os.path.join(DATA_DIR, "menu.json")
USERS_FILE = os.path.join(DATA_DIR, "users.json")
ORDERS_FILE = os.path.join(DATA_DIR, "orders.json")


def _ensure_file(path, default):
    """Create the file with a default value if it does not already exist."""
    if not os.path.exists(path):
        with open(path, "w", encoding="utf-8") as f:
            json.dump(default, f, indent=2)


def load_json(path, default):
    """Load JSON data from `path`, creating it with `default` if missing."""
    _ensure_file(path, default)
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        # Defensive fallback: corrupted/missing file should not crash the app
        return default


def save_json(path, data):
    """Persist `data` as JSON to `path`."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


# --- Convenience wrappers used by the rest of the app -----------------

def load_menu():
    return load_json(MENU_FILE, {"items": [], "promo_codes": {}, "delivery_fee": 40,
                                  "free_delivery_above": 500})


def load_users():
    return load_json(USERS_FILE, {"users": {}})


def save_users(data):
    save_json(USERS_FILE, data)


def load_orders():
    return load_json(ORDERS_FILE, {"orders": {}})


def save_orders(data):
    save_json(ORDERS_FILE, data)
