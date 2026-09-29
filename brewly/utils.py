"""
utils.py
--------
Small, self-contained algorithms used across the app. These are written
by hand (rather than relying only on built-ins) to demonstrate the
fundamental algorithm / array-technique concepts from the course syllabus
(Units 3-5): summation, counting, linear search, selection-style sorting,
finding the Kth smallest element, and duplicate removal.
"""

import hashlib
import re
import uuid


# --- Unit 2: Data & Expressions ---------------------------------------

def hash_password(password: str) -> str:
    """One-way hash so raw passwords are never stored on disk."""
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def is_valid_email(email: str) -> bool:
    pattern = r"^[\w.\-]+@[\w\-]+\.[a-zA-Z]{2,}$"
    return re.match(pattern, email) is not None


def generate_order_id() -> str:
    return "BWL" + uuid.uuid4().hex[:6].upper()


# --- Unit 3: Fundamental Algorithms (Summation / Counting) -------------

def summation(values):
    """Manual summation loop (rather than sum()) to show the algorithm."""
    total = 0
    for v in values:
        total += v
    return total


def count_occurrences(items, predicate):
    """Counts how many elements in `items` satisfy `predicate`."""
    count = 0
    for item in items:
        if predicate(item):
            count += 1
    return count


# --- Unit 5: Array Techniques -------------------------------------------

def linear_search(items, key, key_fn=lambda x: x):
    """Returns the first item whose key_fn(item) == key, else None."""
    for item in items:
        if key_fn(item) == key:
            return item
    return None


def selection_sort(items, key_fn=lambda x: x, reverse=False):
    """
    Classic selection sort implemented manually (course syllabus:
    'Array Techniques'). Returns a NEW sorted list; does not mutate input.
    """
    result = list(items)
    n = len(result)
    for i in range(n):
        target_idx = i
        for j in range(i + 1, n):
            if reverse:
                if key_fn(result[j]) > key_fn(result[target_idx]):
                    target_idx = j
            else:
                if key_fn(result[j]) < key_fn(result[target_idx]):
                    target_idx = j
        result[i], result[target_idx] = result[target_idx], result[i]
    return result


def find_kth_smallest(items, k, key_fn=lambda x: x):
    """
    Finds the Kth smallest element (1-indexed) using the 'Finding the
    Kth smallest element' technique from Unit 5, built on selection sort.
    """
    if k < 1 or k > len(items):
        raise IndexError("k is out of range for the given list")
    sorted_items = selection_sort(items, key_fn=key_fn)
    return sorted_items[k - 1]


def remove_duplicates(items, key_fn=lambda x: x):
    """
    Removes duplicates from a list while preserving order, based on
    Unit 5's 'Removal of Duplicates from an ordered array'.
    """
    seen = set()
    result = []
    for item in items:
        k = key_fn(item)
        if k not in seen:
            seen.add(k)
            result.append(item)
    return result


def find_maximum(items, key_fn=lambda x: x):
    """Finds the maximum element in a non-empty list (Unit 5 technique)."""
    if not items:
        return None
    max_item = items[0]
    for item in items[1:]:
        if key_fn(item) > key_fn(max_item):
            max_item = item
    return max_item
