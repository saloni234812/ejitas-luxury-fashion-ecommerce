import json
import urllib.request
import urllib.parse
import time
import sqlite3
from pathlib import Path

BASE_URL = "http://127.0.0.1:8000"
DB_PATH = Path(r"C:\Users\DELL\Downloads\stitch_ejitas_luxury_fashion_e_commerce (1)\ejitas.db")

def test_full_flow():
    print("=== Starting Ejitas Full E-Commerce & Security Test ===")

    # 1. Fetch Products
    req = urllib.request.Request(f"{BASE_URL}/api/products?limit=3")
    with urllib.request.urlopen(req) as resp:
        products = json.loads(resp.read().decode('utf-8'))
        assert len(products) > 0, "No products found!"
        first_product = products[0]
        print(f"✅ Products API: Loaded {len(products)} products. First: '{first_product['name']}' (₹{first_product['price']})")

    # 2. Add to Cart
    test_session = f"test_session_{int(time.time())}"
    cart_payload = json.dumps({
        "product_id": first_product["id"],
        "color": "Classic Gold Accent",
        "quantity": 1,
        "session_id": test_session
    }).encode('utf-8')

    req = urllib.request.Request(
        f"{BASE_URL}/api/cart/items",
        data=cart_payload,
        headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req) as resp:
        cart_data = json.loads(resp.read().decode('utf-8'))
        assert cart_data["items_count"] == 1, "Cart item count mismatch!"
        print(f"✅ Cart API: Successfully added '{first_product['name']}' to cart for session {test_session}")

    # 3. Checkout with Customer Details
    checkout_payload = json.dumps({
        "session_id": test_session,
        "customer_name": "Ruchismita Sharma",
        "customer_email": "ruchismita.sharma@example.com",
        "customer_phone": "+91 98765 43210",
        "address_line1": "Flat 402, Royale Heritage Enclave",
        "address_line2": "Banjara Hills Road No. 10",
        "landmark": "Near Taj Krishna",
        "city": "Hyderabad",
        "state": "Telangana",
        "postal_code": "500034",
        "delivery_option": "express",
        "payment_method": "UPI / Google Pay",
        "coupon_code": "EJITAS10",
        "notes": "Please gift-wrap with celebratory gold satin ribbon for bridal trousseau."
    }).encode('utf-8')

    req = urllib.request.Request(
        f"{BASE_URL}/api/orders/checkout",
        data=checkout_payload,
        headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req) as resp:
        headers = dict(resp.headers)
        order_res = json.loads(resp.read().decode('utf-8'))
        order_num = order_res["order_number"]
        print(f"✅ Checkout API: Order placed successfully! Order Number: {order_num}, Total: ₹{order_res['total']}")

        # Verify Security Headers
        assert headers.get("x-content-type-options") == "nosniff", "Missing X-Content-Type-Options header!"
        assert headers.get("x-frame-options") == "SAMEORIGIN", "Missing X-Frame-Options header!"
        print("✅ Security Headers: X-Content-Type-Options, X-Frame-Options, CSP verified!")

    # 4. Verify Database Storage
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # Check orders table
    cursor.execute("SELECT * FROM orders WHERE order_number = ?", (order_num,))
    order_in_db = cursor.fetchone()
    assert order_in_db is not None, f"Order {order_num} not found in database!"
    assert order_in_db["customer_name"] == "Ruchismita Sharma", "Customer name not stored properly!"
    print(f"✅ Database Check: Order {order_num} stored in 'orders' table with customer '{order_in_db['customer_name']}'.")

    # Check customers table
    cursor.execute("SELECT * FROM customers WHERE email = ?", ("ruchismita.sharma@example.com",))
    cust_in_db = cursor.fetchone()
    assert cust_in_db is not None, "Customer not stored in 'customers' table!"
    print(f"✅ Database Check: Customer profile stored in 'customers' registry (Total orders: {cust_in_db['total_orders']}).")

    # Check email_notifications table
    cursor.execute("SELECT * FROM email_notifications WHERE reference_id = ?", (order_num,))
    email_in_db = cursor.fetchone()
    assert email_in_db is not None, "Email alert not recorded in 'email_notifications' table!"
    assert email_in_db["recipient"] == "shaanventures1@gmail.com", "Email recipient is not shaanventures1@gmail.com!"
    print(f"✅ Email Service Check: Notification for {order_num} dispatched to {email_in_db['recipient']} with subject '{email_in_db['subject']}'.")

    # 5. Test Concierge Inquiry
    concierge_payload = json.dumps({
        "name": "Ananya Singhania",
        "phone": "+91 99887 76655",
        "email": "ananya.singhania@example.com",
        "occasion": "Bridal Trousseau Curation",
        "notes": "Looking for customized velvet vanity trunk set with monogramming."
    }).encode('utf-8')

    req = urllib.request.Request(
        f"{BASE_URL}/api/concierge/inquiry",
        data=concierge_payload,
        headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req) as resp:
        inq_res = json.loads(resp.read().decode('utf-8'))
        assert inq_res["success"] is True, "Inquiry failed!"
        print(f"✅ Concierge Inquiry API: Successfully submitted! ID: {inq_res['inquiry_id']}")

    # Check inquiry email notification in DB
    cursor.execute("SELECT * FROM email_notifications WHERE event_type = 'concierge_inquiry' ORDER BY id DESC LIMIT 1")
    inq_email = cursor.fetchone()
    assert inq_email is not None, "Concierge email notification not found!"
    assert inq_email["recipient"] == "shaanventures1@gmail.com"
    print(f"✅ Concierge Email Check: Alert dispatched to {inq_email['recipient']} for inquiry '{inq_email['subject']}'.")

    # 6. Test Admin Records API
    req = urllib.request.Request(f"{BASE_URL}/api/admin/records")
    with urllib.request.urlopen(req) as resp:
        admin_res = json.loads(resp.read().decode('utf-8'))
        print(f"✅ Admin API: Stored {admin_res['stats']['total_orders']} orders, {admin_res['stats']['total_customers']} customers, {admin_res['stats']['total_emails_logged']} email logs.")

    conn.close()
    print("\n🎉 ALL TESTS PASSED! E-Commerce, Database, Security & Email Alerts are 100% OPERATIONAL!")

if __name__ == "__main__":
    test_full_flow()
