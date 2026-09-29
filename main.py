#!/usr/bin/env python3
"""
BREWLY - Coffee Ordering CLI Application (Brewly Artisan Café)
=========================================
Entry point. Run with:  python main.py

A command-line coffee ordering system built for CSE1021
(Introduction to Problem Solving and Programming).

Design note: this CLI is a functional re-implementation of a Figma UI
prototype ("BREWLY - Find your favourite coffee") originally designed
for this project. Screens map to menus as follows:

    Welcome / Sign in / Create Account  -> main_menu()
    Home (categories + popular coffee)   -> browse_menu()
    Product detail + Add to Cart         -> view_item()
    Your Cart                            -> view_cart()
    Checkout / Order Successful          -> checkout_flow()
    Favourites                           -> view_favorites()
    My Profile                           -> view_profile()
"""

import sys

from brewly import auth, menu, cart, checkout
from brewly.auth import AuthError
from brewly.checkout import CheckoutError


def pause():
    input("\nPress Enter to continue...")


def print_header(title):
    print("\n" + "=" * 44)
    print(f"  BREWLY | {title}")
    print("=" * 44)


# ---------------------------------------------------------------------
# Entry / Authentication screens
# ---------------------------------------------------------------------

def welcome_screen():
    print_header("Find your favourite coffee")
    print("1. Sign in")
    print("2. Create an Account")
    print("3. Continue as Guest")
    print("0. Exit")
    return input("Choose an option: ").strip()


def create_account_flow():
    print_header("Create an account")
    username = input("Full Name: ")
    email = input("Email Address: ")
    phone = input("Phone Number: ")
    password = input("Create Password: ")
    try:
        user = auth.create_account(username, email, phone, password)
        print(f"\nAccount created successfully. Welcome, {user.username}!")
        return user
    except AuthError as e:
        print(f"\n[Error] {e}")
        return None


def sign_in_flow():
    print_header("Welcome Back - Sign in")
    email = input("Email Address: ")
    password = input("Password: ")
    try:
        user = auth.sign_in(email, password)
        print(f"\nGlad to see you, {user.username}!")
        return user
    except AuthError as e:
        print(f"\n[Error] {e}")
        return None


# ---------------------------------------------------------------------
# Home / Menu browsing
# ---------------------------------------------------------------------

def browse_menu(user):
    while True:
        print_header("Home - Popular Coffee")
        categories = menu.get_categories()
        print("Categories:", ", ".join(categories))
        print("-" * 44)

        items = menu.get_all_items()
        for i in items:
            print(f"  {i}")

        print("-" * 44)
        print("1. View item detail (Add to Cart)")
        print("2. Filter by category")
        print("3. Search by name")
        print("4. Sort by price")
        print("5. View Cart")
        print("6. Checkout")
        print("7. Favourites")
        print("8. My Profile")
        print("9. Order History")
        print("0. Log out")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            view_item(user)
        elif choice == "2":
            cat = input("Enter category name: ")
            for i in menu.filter_by_category(cat):
                print(f"  {i}")
            pause()
        elif choice == "3":
            keyword = input("Search keyword: ")
            for i in menu.search_by_name(keyword):
                print(f"  {i}")
            pause()
        elif choice == "4":
            order = input("Sort (asc/desc): ").strip().lower()
            sorted_items = menu.sort_by_price(descending=(order == "desc"))
            for i in sorted_items:
                print(f"  {i}")
            pause()
        elif choice == "5":
            view_cart(user)
        elif choice == "6":
            checkout_flow(user)
        elif choice == "7":
            view_favorites(user)
        elif choice == "8":
            view_profile(user)
        elif choice == "9":
            view_order_history(user)
        elif choice == "0":
            auth.save_user(user)
            print("Logged out. See you soon!")
            break
        else:
            print("Invalid option.")


def view_item(user):
    item_id = input("Enter item ID (e.g. MOC01): ").strip()
    item = menu.find_item_by_id(item_id)
    if not item:
        print("Item not found.")
        return

    print_header(item.name)
    print(item.description)
    print(f"Price: Rs.{item.price}   Rating: {item.rating}*")

    print("\n1. Add to Cart")
    print("2. Add to Favourites")
    print("0. Back")
    choice = input("Choose an option: ").strip()

    if choice == "1":
        try:
            qty = int(input("Quantity: ") or "1")
        except ValueError:
            qty = 1
        cart.add_to_cart(user.cart, item, qty)
        auth.save_user(user)
        print(f"\nAdded to your Cart! {item.name} x{qty} added.")
    elif choice == "2":
        if item.item_id not in user.favorites:
            user.favorites.append(item.item_id)
            auth.save_user(user)
            print("Added to Favourites.")
        else:
            print("Already in Favourites.")
    pause()


# ---------------------------------------------------------------------
# Cart & Checkout
# ---------------------------------------------------------------------

def view_cart(user):
    print_header("Your Cart")
    if not user.cart:
        print("Your cart is empty.")
        pause()
        return

    for line in user.cart:
        print(f"  {line['item']['name']} x{line['quantity']} = Rs.{line['item']['price'] * line['quantity']}")
    print(f"\nSubtotal: Rs.{cart.cart_subtotal(user.cart)}")

    print("\n1. Update quantity")
    print("2. Remove item")
    print("3. Proceed to Checkout")
    print("0. Back")
    choice = input("Choose an option: ").strip()

    if choice == "1":
        item_id = input("Item ID to update: ").strip().upper()
        try:
            qty = int(input("New quantity: "))
        except ValueError:
            print("Invalid quantity.")
            pause()
            return
        cart.update_quantity(user.cart, item_id, qty)
        auth.save_user(user)
        print("Cart updated.")
    elif choice == "2":
        item_id = input("Item ID to remove: ").strip().upper()
        cart.remove_from_cart(user.cart, item_id)
        auth.save_user(user)
        print("Item removed.")
    elif choice == "3":
        checkout_flow(user)
        return
    pause()


def checkout_flow(user):
    print_header("Checkout")
    if not user.cart:
        print("Your cart is empty. Add something tasty first!")
        pause()
        return

    for line in user.cart:
        print(f"  {line['item']['name']} x{line['quantity']} = Rs.{line['item']['price'] * line['quantity']}")

    promo = input("\nHave a coupon code? (or press Enter to skip): ").strip()

    try:
        totals = checkout.compute_totals(user.cart, promo or None)
    except CheckoutError as e:
        print(f"\n[Error] {e}")
        pause()
        return

    print("\n--- Order Summary ---")
    print(f"Subtotal:      Rs.{totals['subtotal']}")
    if totals["discount"]:
        print(f"Discount ({totals['promo_code']}): -Rs.{totals['discount']}")
    print(f"Delivery Fee:  Rs.{totals['delivery_fee']}")
    print(f"Total:         Rs.{totals['total']}")

    confirm = input("\nPlace order? (y/n): ").strip().lower()
    if confirm == "y":
        order = checkout.place_order(user, user.cart, promo or None)
        auth.save_user(user)
        print_header("Order Successful!")
        print(f"Order #{order.order_id} placed.")
        print(f"Total charged: Rs.{order.total}")
        print(f"You now have {user.brew_points} Brew Points.")
    else:
        print("Order cancelled.")
    pause()


# ---------------------------------------------------------------------
# Favourites / Profile / History
# ---------------------------------------------------------------------

def view_favorites(user):
    print_header("Favourites")
    if not user.favorites:
        print("You haven't favourited anything yet.")
    else:
        for item_id in user.favorites:
            item = menu.find_item_by_id(item_id)
            if item:
                print(f"  {item}")
    pause()


def view_profile(user):
    print_header("My Profile")
    print(f"Name:        {user.username}")
    print(f"Email:       {user.email}")
    print(f"Phone:       {user.phone}")
    print(f"Brew Points: {user.brew_points}")
    print(f"Favourites:  {len(user.favorites)}")
    print(f"Orders:      {len(user.orders)}")
    pause()


def view_order_history(user):
    print_header("Order History")
    orders = checkout.get_order_history(user)
    if not orders:
        print("No past orders yet.")
    else:
        for o in sorted(orders, key=lambda x: x.timestamp, reverse=True):
            print(f"  Order #{o.order_id} | {o.timestamp} | Rs.{o.total}")
    pause()


# ---------------------------------------------------------------------
# Guest mode (browse only, no cart persistence)
# ---------------------------------------------------------------------

def guest_browse():
    print_header("Guest Mode - Browsing Only")
    print("(Sign in or create an account to add items to your cart.)")
    for i in menu.get_all_items():
        print(f"  {i}")
    pause()


# ---------------------------------------------------------------------
# Main loop
# ---------------------------------------------------------------------

def main():
    print("Welcome to BREWLY - your favourite coffee, one command away.")
    while True:
        choice = welcome_screen()
        if choice == "1":
            user = sign_in_flow()
            if user:
                browse_menu(user)
        elif choice == "2":
            user = create_account_flow()
            if user:
                browse_menu(user)
        elif choice == "3":
            guest_browse()
        elif choice == "0":
            print("Thanks for visiting BREWLY. Goodbye!")
            sys.exit(0)
        else:
            print("Invalid option, please try again.")


if __name__ == "__main__":
    main()
