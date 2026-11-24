# Ejitas - Handcrafted Luxury Bags & Vanity E-Commerce

A full-stack, quiet-luxury e-commerce web platform and REST API built for modern Indian women. Features heirloom Indian leathercraft, brushed 24K champagne brass aesthetics, responsive editorial design, and an integrated FastAPI backend with SQLite persistence.

---

## 🌟 Key Highlights

- **Virtual Environment**: Pre-configured Python 3.14 virtual environment in `venv/` with FastAPI, Uvicorn, Pydantic, and Jinja2.
- **Full REST API**: Clean endpoints for products, category filtering, search, cart management, coupons, wishlist, checkout, orders, and styling concierge.
- **Interactive Web Pages**:
  - **`/` (Home)**: Lookbook hero, signature categories, bestselling vanity cases, and newsletter privilege code.
  - **`/shop` (Collection)**: Real-time category pills, sorting (price, bestsellers, newest), filter drawer, and quick add-to-bag.
  - **`/product/{slug}` (Product Detail)**: Gallery thumbnail switcher, color swatch picker, quantity stepper, add-to-bag, buy-now instant checkout, accordions, and customer review submission.
  - **`/cart` (Shopping Bag)**: Interactive line items, live free shipping progress tracker (₹1,499 threshold), privilege code applicator (`EJITAS10`, `WELCOME20`, `ATELIER500`), and order summary.
  - **`/checkout` (Secure Checkout)**: Indian address form with PIN code validation, payment selection (UPI, Credit/Debit Card, Netbanking, Cash on Delivery), and order confirmation.
  - **`/order-success/{order_number}`**: Order celebration screen with unique order ID (`EJT-2026-XXXXX`), courier tracking number, itemized receipt, and printable invoice.
  - **`/wishlist`**: Saved favorites with 1-click move to bag.
  - **Interactive Global Drawers**: Slide-over cart drawer, mobile navigation drawer, and live instant search modal across all pages.
- **Interactive Swagger Docs**: Fully documented interactive API testing at [`http://127.0.0.1:8000/docs`](http://127.0.0.1:8000/docs).

---

## 🚀 Quick Start Guide

### 1. One-Click Launch (Windows)

Double-click `run.bat` or run in PowerShell:

```powershell
.\run.ps1
```

### 2. Manual Startup with Virtual Environment

Activate the virtual environment and run the server:

```powershell
# In PowerShell:
.\venv\Scripts\Activate.ps1
python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000 --reload
```

```cmd
# In Command Prompt (cmd.exe):
.\venv\Scripts\activate.bat
python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000 --reload
```

Visit the application in your browser:
- **Storefront**: [http://127.0.0.1:8000](http://127.0.0.1:8000)
- **Collection**: [http://127.0.0.1:8000/shop](http://127.0.0.1:8000/shop)
- **Swagger API Docs**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc API Docs**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## 🧪 Running Automated Tests

Run the full automated test suite verifying endpoints, cart operations, coupons, checkout, and page rendering:

```powershell
.\venv\Scripts\python.exe -m pytest tests/test_api.py -v
```

---

## 📡 REST API Reference

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/products` | List all products with category, search, and sort filters |
| `GET` | `/api/products/{id_or_slug}` | Detailed product with colors, gallery images, specifications, and reviews |
| `GET` | `/api/products/categories` | Categories list with product count and cover images |
| `POST` | `/api/products/{id}/reviews` | Submit verified customer review and update aggregate rating |
| `GET` | `/api/cart?session_id=...` | Retrieve cart, subtotal, and free shipping progress |
| `POST` | `/api/cart/items` | Add item with selected color and quantity |
| `PUT` | `/api/cart/items/{id}` | Update item quantity |
| `DELETE` | `/api/cart/items/{id}` | Remove line item |
| `DELETE` | `/api/cart` | Empty shopping bag |
| `GET` | `/api/wishlist?session_id=...` | Retrieve saved products |
| `POST` | `/api/wishlist/toggle` | Toggle item in user's wishlist |
| `POST` | `/api/coupons/apply` | Validate coupon code (`EJITAS10`, `WELCOME20`, `ATELIER500`) |
| `POST` | `/api/orders/checkout` | Process order, validate inventory, calculate shipping, create order record |
| `GET` | `/api/orders/{order_number}` | Retrieve order details by order number |
| `POST` | `/api/concierge/inquiry` | Submit styling & bridal trousseau WhatsApp inquiry |

---

## 🎁 Active Privilege Codes

- **`EJITAS10`**: 10% off entire order (Orders above ₹1,499)
- **`WELCOME20`**: 20% off for first-time connoisseurs (Orders above ₹2,499)
- **`ATELIER500`**: Flat ₹500 off on bridal vanity orders above ₹3,000

---

## 📂 Project Architecture

```
├── backend/
│   ├── routes/
│   │   ├── products.py       # Product catalog & review routes
│   │   ├── cart.py           # Shopping bag calculations & CRUD
│   │   ├── wishlist.py       # Saved items toggle & retrieval
│   │   ├── orders.py         # Order placement & receipt retrieval
│   │   ├── coupons.py        # Privilege code validation & discount math
│   │   └── concierge.py      # WhatsApp bridal stylist concierge inquiries
│   ├── database.py           # SQLite connection, schema definition
│   ├── seed_data.py          # Curated Indian luxury bag data & reviews
│   ├── schemas.py            # Pydantic validation schemas
│   └── main.py               # FastAPI application & page routing
├── static/
│   └── js/
│       └── app.js            # Reactive client engine (cart sync, drawer, toast, search)
├── templates/
│   ├── base.html             # Master layout with Tailwind & Google Fonts
│   ├── components/           # Modular headers, drawers, search, and footers
│   ├── home.html             # Lookbook & showcase home page
│   ├── shop.html             # Merchandised collection with live filters
│   ├── product.html          # Product detail with interactive gallery & reviews
│   ├── cart.html             # Full bag view with live free-shipping bar
│   ├── checkout.html         # Bespoke checkout with Indian payment methods
│   ├── order_success.html    # Order confirmation with live tracking & receipt
│   └── wishlist.html         # Saved favorites page
├── tests/
│   └── test_api.py           # Pytest test suite (100% pass)
├── venv/                     # Python virtual environment
├── ejitas.db                 # SQLite database
├── requirements.txt          # Python dependencies
├── run.bat                   # 1-click Windows runner
└── run.ps1                   # PowerShell runner
```
