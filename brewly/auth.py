"""
auth.py
-------
FUNCTIONAL MODULE 1: User Management
Handles account creation, sign-in, and session state.
Mirrors the Figma screens: "Create an Account", "Welcome Back / Sign in",
and "Continue as Guest".
"""

from brewly import data_manager as dm
from brewly.models import User
from brewly.utils import hash_password, is_valid_email


class AuthError(Exception):
    """Raised for invalid credentials or bad signup data."""
    pass


def create_account(username, email, phone, password):
    """
    Registers a new user. Mirrors the 'Create an account' Figma screen
    fields: Full Name, Email Address, Phone Number, Password.
    """
    username = username.strip()
    email = email.strip().lower()

    if not username:
        raise AuthError("Full name cannot be empty.")
    if not is_valid_email(email):
        raise AuthError("Please enter a valid email address.")
    if len(password) < 4:
        raise AuthError("Password must be at least 4 characters long.")

    data = dm.load_users()
    if email in data["users"]:
        raise AuthError("An account with this email already exists.")

    user = User(
        username=username,
        email=email,
        password_hash=hash_password(password),
        phone=phone.strip(),
    )
    data["users"][email] = user.to_dict()
    dm.save_users(data)
    return user


def sign_in(email, password):
    """
    Authenticates a returning user. Mirrors the 'Welcome Back / Sign in'
    Figma screen.
    """
    email = email.strip().lower()
    data = dm.load_users()
    record = data["users"].get(email)

    if record is None:
        raise AuthError("No account found with that email.")
    if record["password_hash"] != hash_password(password):
        raise AuthError("Incorrect password.")

    return User.from_dict(record)


def save_user(user: User):
    """Persists changes made to a User object (cart, favorites, points)."""
    data = dm.load_users()
    data["users"][user.email] = user.to_dict()
    dm.save_users(data)
