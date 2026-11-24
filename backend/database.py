import sqlite3
import os
import json
from pathlib import Path
from contextlib import contextmanager

DB_PATH = Path(__file__).resolve().parent.parent / "ejitas.db"

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@contextmanager
def get_db():
    conn = get_db_connection()
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()

def init_db():
    with get_db() as conn:
        cursor = conn.cursor()
        
        # Products table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            slug TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            category_slug TEXT NOT NULL,
            price REAL NOT NULL,
            original_price REAL NOT NULL,
            discount_percent INTEGER DEFAULT 0,
            badge TEXT,
            rating REAL DEFAULT 4.8,
            reviews_count INTEGER DEFAULT 1,
            edition_tag TEXT DEFAULT 'Atelier Signature • Edition No. 04',
            short_description TEXT,
            description TEXT,
            material TEXT,
            lining TEXT,
            hardware TEXT,
            dimensions TEXT,
            provenance TEXT DEFAULT 'Handcrafted in Jaipur, India',
            stock_quantity INTEGER DEFAULT 50,
            colors TEXT, -- JSON array of {name, hex, image}
            images TEXT, -- JSON array of image URLs
            specifications TEXT, -- JSON dict of specs
            is_featured INTEGER DEFAULT 0,
            is_bestseller INTEGER DEFAULT 0,
            is_new INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """)

        # Reviews table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS reviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER NOT NULL,
            author TEXT NOT NULL,
            location TEXT,
            rating INTEGER NOT NULL,
            title TEXT,
            comment TEXT NOT NULL,
            verified INTEGER DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE
        );
        """)

        # Cart items table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS cart_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT NOT NULL,
            product_id INTEGER NOT NULL,
            color TEXT,
            quantity INTEGER NOT NULL DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE,
            UNIQUE(session_id, product_id, color)
        );
        """)

        # Wishlist table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS wishlist_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT NOT NULL,
            product_id INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE,
            UNIQUE(session_id, product_id)
        );
        """)

        # Coupons table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS coupons (
            code TEXT PRIMARY KEY,
            discount_percent REAL DEFAULT 0,
            discount_amount REAL DEFAULT 0,
            min_order REAL DEFAULT 0,
            description TEXT,
            is_active INTEGER DEFAULT 1
        );
        """)

        # Orders table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_number TEXT UNIQUE NOT NULL,
            session_id TEXT NOT NULL,
            customer_name TEXT NOT NULL,
            customer_email TEXT NOT NULL,
            customer_phone TEXT NOT NULL,
            address_line1 TEXT NOT NULL,
            address_line2 TEXT,
            landmark TEXT,
            city TEXT NOT NULL,
            state TEXT NOT NULL,
            postal_code TEXT NOT NULL,
            delivery_option TEXT DEFAULT 'express',
            payment_method TEXT NOT NULL,
            payment_status TEXT DEFAULT 'Paid',
            subtotal REAL NOT NULL,
            coupon_code TEXT,
            discount REAL DEFAULT 0.0,
            shipping_fee REAL DEFAULT 0.0,
            total REAL NOT NULL,
            order_status TEXT DEFAULT 'Confirmed',
            tracking_number TEXT,
            estimated_delivery TEXT,
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """)

        # Order Items table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS order_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            product_name TEXT NOT NULL,
            product_image TEXT NOT NULL,
            color TEXT,
            price REAL NOT NULL,
            quantity INTEGER NOT NULL,
            total REAL NOT NULL,
            FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE
        );
        """)

        # Concierge inquiries table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS concierge_inquiries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT NOT NULL,
            email TEXT,
            occasion TEXT,
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """)

        # Customers table (stores all registered/checkout customer profiles)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            phone TEXT,
            address_line1 TEXT,
            address_line2 TEXT,
            landmark TEXT,
            city TEXT,
            state TEXT,
            postal_code TEXT,
            total_orders INTEGER DEFAULT 0,
            total_spent REAL DEFAULT 0.0,
            last_order_date TIMESTAMP,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """)

        # Newsletter / Privilege Club Subscribers table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS newsletter_subscribers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            source TEXT DEFAULT 'vip_club_form',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """)

        # Email Notifications Log table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS email_notifications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            recipient TEXT NOT NULL,
            subject TEXT NOT NULL,
            event_type TEXT NOT NULL,
            reference_id TEXT,
            payload_json TEXT,
            status TEXT DEFAULT 'sent',
            sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """)

if __name__ == "__main__":
    init_db()
    print("Database initialized successfully at", DB_PATH)
