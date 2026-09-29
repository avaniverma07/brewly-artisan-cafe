# Problem Statement - Brewly Artisan Café

## Problem Statement

Ordering coffee at a busy campus cafe often involves long queues, verbal
miscommunication about order customizations, and no easy way to track past
orders or loyalty rewards. There is a need for a lightweight, dependency-free
ordering system that lets a customer browse a menu, build a cart, apply
discounts, and check out — usable even in constrained/offline
environments (e.g. a lab machine with no GUI framework installed) — while
still teaching and demonstrating fundamental programming concepts such as
control flow, functions, and data structures.

## Scope of the Project

BREWLY is a **command-line coffee ordering application** written in Python.
It covers the full customer ordering journey:

- Account creation and sign-in
- Menu browsing, filtering, searching, and sorting
- Cart management (add / update / remove)
- Promo code application and total calculation
- Order placement, confirmation, and history
- Favourites and a basic loyalty points system

It is a **single-user-at-a-time, local, file-based system** — it does not
include a networked multi-user backend, payment gateway integration, or a
graphical interface. Those are explicitly out of scope, in line with the
"fully executable via the command line" requirement of this course project.

## Target Users

- **Coffee shop customers** who want a fast, no-frills way to browse a menu
  and place an order without a GUI or an app installation.
- **Evaluators/instructors** assessing the application of CSE1021 syllabus
  concepts (data types, control flow, functions, lists/tuples/dictionaries,
  fundamental algorithms) in a realistic, end-to-end program.

## High-Level Features

1. **User Management Module** — registration, login, input validation,
   password hashing
2. **Menu Browsing Module** — category filters, keyword search, and a
   hand-written selection-sort for price sorting
3. **Cart & Checkout Module** — add/update/remove cart items, promo-code
   discounts, delivery-fee logic, order placement, and order history
4. Supplementary features: favourites list and a simple loyalty
   ("Brew Points") system

## Relationship to the Original Design

This project was first prototyped as a mobile UI/UX design in Figma
("BREWLY - Find your favourite coffee"), covering onboarding, sign-up/sign-in,
home, product detail, cart, checkout, order-success, favourites, and profile
screens. The CLI application in this repository is a functional,
from-scratch reimplementation of that same user flow and information
architecture, adapted to a terminal-based interface as required by this
course's submission guidelines.
