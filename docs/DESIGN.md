# Brewly Artisan Café - Design Documentation

This document contains the architectural and behavioural diagrams for the
BREWLY CLI project. All diagrams are written in **Mermaid** syntax, which
GitHub renders automatically when viewing this file in the browser.

---

## 1. System Architecture Diagram

Shows how the CLI (presentation layer) talks to the functional modules
(business logic layer), which in turn talk to the JSON persistence layer
(data layer).

```mermaid
graph TD
    subgraph Presentation Layer
        A[main.py - CLI Interface]
    end

    subgraph Business Logic Layer
        B[auth.py<br/>User Management]
        C[menu.py<br/>Menu Browsing]
        D[cart.py<br/>Cart Operations]
        E[checkout.py<br/>Checkout and Orders]
        F[utils.py<br/>Shared Algorithms]
    end

    subgraph Data Layer
        G[data_manager.py<br/>JSON Read/Write]
        H[(users.json)]
        I[(menu.json)]
        J[(orders.json)]
    end

    A --> B
    A --> C
    A --> D
    A --> E
    B --> F
    C --> F
    D --> F
    E --> F
    B --> G
    C --> G
    D --> G
    E --> G
    G --> H
    G --> I
    G --> J
```

---

## 2. Process Flow / Workflow Diagram

Mirrors the original Figma user flow: Welcome -> Auth -> Home -> Product
Detail -> Cart -> Checkout -> Order Success.

```mermaid
flowchart TD
    Start([Start]) --> Welcome[Welcome Screen]
    Welcome -->|Sign in| SignIn[Sign In]
    Welcome -->|Create Account| SignUp[Create Account]
    Welcome -->|Guest| Guest[Browse as Guest]

    SignIn --> Home[Home: Browse Menu]
    SignUp --> Home
    Guest --> GuestView[View-only Menu]
    GuestView --> End1([Exit])

    Home --> Detail[View Item Detail]
    Detail -->|Add to Cart| Cart[Your Cart]
    Detail -->|Add to Favourites| Home

    Cart -->|Update/Remove| Cart
    Cart -->|Proceed| Checkout[Checkout]

    Checkout -->|Apply Promo Code| Checkout
    Checkout -->|Confirm| Success[Order Successful]
    Success --> Points[Brew Points Awarded]
    Points --> Home

    Home -->|Log out| End2([Exit])
```

---

## 3. Use Case Diagram

```mermaid
graph LR
    Guest((Guest))
    Customer((Registered<br/>Customer))

    Guest --> UC1[Browse Menu]

    Customer --> UC1
    Customer --> UC2[Create Account / Sign In]
    Customer --> UC3[Add Item to Cart]
    Customer --> UC4[Update / Remove Cart Item]
    Customer --> UC5[Apply Promo Code]
    Customer --> UC6[Place Order]
    Customer --> UC7[Manage Favourites]
    Customer --> UC8[View Order History]
    Customer --> UC9[View Profile]
```

---

## 4. Class / Component Diagram

```mermaid
classDiagram
    class MenuItem {
        +str item_id
        +str name
        +str category
        +float price
        +float rating
        +str description
        +to_dict()
        +from_dict(d)
    }

    class CartItem {
        +MenuItem menu_item
        +int quantity
        +subtotal()
        +to_dict()
        +from_dict(d)
    }

    class User {
        +str username
        +str email
        +str password_hash
        +str phone
        +list favorites
        +int brew_points
        +list cart
        +list orders
        +to_dict()
        +from_dict(d)
    }

    class Order {
        +str order_id
        +str username
        +list items
        +float subtotal
        +float discount
        +float delivery_fee
        +float total
        +str promo_code
        +str timestamp
        +to_dict()
        +from_dict(d)
    }

    class AuthModule {
        +create_account(username, email, phone, password)
        +sign_in(email, password)
        +save_user(user)
    }

    class MenuModule {
        +get_all_items()
        +filter_by_category(category)
        +search_by_name(keyword)
        +sort_by_price(items, descending)
    }

    class CartModule {
        +add_to_cart(cart, item, qty)
        +update_quantity(cart, id, qty)
        +remove_from_cart(cart, id)
        +cart_subtotal(cart)
    }

    class CheckoutModule {
        +apply_promo_code(subtotal, code)
        +compute_totals(cart, promo_code)
        +place_order(user, cart, promo_code)
        +get_order_history(user)
    }

    User "1" --> "*" CartItem : holds in cart
    CartItem "1" --> "1" MenuItem : references
    Order "1" --> "*" CartItem : snapshot of
    AuthModule ..> User : creates/authenticates
    MenuModule ..> MenuItem : queries
    CartModule ..> CartItem : manipulates
    CheckoutModule ..> Order : creates
```

---

## 5. Sequence Diagram - "Place an Order"

```mermaid
sequenceDiagram
    actor U as User
    participant CLI as main.py
    participant Cart as cart.py
    participant Chk as checkout.py
    participant DM as data_manager.py

    U->>CLI: Select "Checkout"
    CLI->>Cart: cart_subtotal(user.cart)
    Cart-->>CLI: subtotal
    CLI->>U: Prompt for promo code
    U->>CLI: Enter promo code (optional)
    CLI->>Chk: compute_totals(cart, promo_code)
    Chk->>DM: load_menu() [promo codes]
    DM-->>Chk: menu data
    Chk-->>CLI: {subtotal, discount, delivery_fee, total}
    CLI->>U: Display order summary
    U->>CLI: Confirm (y)
    CLI->>Chk: place_order(user, cart, promo_code)
    Chk->>DM: save_orders(order)
    Chk-->>CLI: Order object
    CLI->>DM: save_user(user) [points, order id]
    CLI->>U: "Order Successful!" + Brew Points
```

---

## 6. Data / Storage Design

BREWLY uses flat-file **JSON storage** (no external database server needed,
keeping the project runnable anywhere with plain Python). The structure
below is the logical equivalent of an ER diagram for this storage model.

```mermaid
erDiagram
    USER ||--o{ CART_ITEM : contains
    USER ||--o{ ORDER : places
    ORDER ||--o{ CART_ITEM : snapshots
    CART_ITEM }o--|| MENU_ITEM : references

    USER {
        string username
        string email PK
        string password_hash
        string phone
        list favorites
        int brew_points
    }

    MENU_ITEM {
        string item_id PK
        string name
        string category
        float price
        float rating
        string description
    }

    CART_ITEM {
        string item_id FK
        int quantity
    }

    ORDER {
        string order_id PK
        string username FK
        float subtotal
        float discount
        float delivery_fee
        float total
        string promo_code
        string timestamp
    }
```

**Schema files:**
- `brewly/data/menu.json` — menu items + promo codes (seed data, version-controlled)
- `brewly/data/users.json` — created at runtime (gitignored, holds registered users)
- `brewly/data/orders.json` — created at runtime (gitignored, holds placed orders)
