import pytest
from fastapi.testclient import TestClient
from backend.main import app
from backend.database import init_db
from backend.seed_data import seed_database

client = TestClient(app)

def setup_module():
    init_db()
    seed_database()

def test_list_products():
    response = client.get("/api/products")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 16
    assert any(p["slug"] == "the-jackie-crescent-hobo" for p in data)
    assert any(p["slug"] == "the-horsebit-1955-flap-bag" for p in data)
    assert any(p["slug"] == "the-bamboo-1947-top-handle" for p in data)
    assert "name" in data[0]
    assert "price" in data[0]

def test_get_og_gucci_inspired_bag():
    response = client.get("/api/products/the-jackie-crescent-hobo")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "The Jackie Crescent Hobo"
    assert data["badge"] == "Iconic Silhouette"
    assert data["price"] == 4499.0
    assert len(data["reviews"]) > 0

def test_filter_products_by_category():
    response = client.get("/api/products?category=vanity")
    assert response.status_code == 200
    data = response.json()
    assert all("vanity" in p["category_slug"] or "Vanity" in p["category"] for p in data)

def test_get_single_product():
    response = client.get("/api/products/royale-vanity-trunk")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "The Royale Vanity Trunk"
    assert "reviews" in data
    assert len(data["reviews"]) > 0

def test_cart_operations():
    session_id = "test_cart_user_123"
    
    # 1. Add item to cart
    add_res = client.post("/api/cart/items", json={
        "product_id": 1,
        "color": "Rose Gold & Cream",
        "quantity": 1,
        "session_id": session_id
    })
    assert add_res.status_code == 200
    cart_data = add_res.json()
    assert cart_data["items_count"] == 1
    assert cart_data["subtotal"] == 3499.0
    assert cart_data["free_shipping_unlocked"] is True

    # 2. Add second item
    add_res_2 = client.post("/api/cart/items", json={
        "product_id": 2,
        "color": "Blush Pink",
        "quantity": 2,
        "session_id": session_id
    })
    assert add_res_2.status_code == 200
    cart_data_2 = add_res_2.json()
    assert cart_data_2["items_count"] == 3

    # 3. Update quantity
    item_id = cart_data_2["items"][0]["id"]
    upd_res = client.put(f"/api/cart/items/{item_id}?session_id={session_id}", json={
        "quantity": 3
    })
    assert upd_res.status_code == 200

    # 4. Remove item
    del_res = client.delete(f"/api/cart/items/{item_id}?session_id={session_id}")
    assert del_res.status_code == 200

    # 5. Clear cart
    clear_res = client.delete(f"/api/cart?session_id={session_id}")
    assert clear_res.status_code == 200
    assert clear_res.json()["items_count"] == 0

def test_coupon_validation():
    # Valid coupon
    res = client.post("/api/coupons/apply", json={
        "code": "EJITAS10",
        "cart_total": 3500.0
    })
    assert res.status_code == 200
    data = res.json()
    assert data["valid"] is True
    assert data["discount_amount"] == 350.0

    # Below min order
    res_low = client.post("/api/coupons/apply", json={
        "code": "WELCOME20",
        "cart_total": 1000.0
    })
    assert res_low.status_code == 200
    assert res_low.json()["valid"] is False

def test_wishlist_toggle():
    session_id = "test_wishlist_user"
    res = client.post("/api/wishlist/toggle", json={
        "product_id": 1,
        "session_id": session_id
    })
    assert res.status_code == 200
    assert res.json()["is_wishlisted"] is True

    # Toggle off
    res_off = client.post("/api/wishlist/toggle", json={
        "product_id": 1,
        "session_id": session_id
    })
    assert res_off.status_code == 200
    assert res_off.json()["is_wishlisted"] is False

def test_full_checkout_flow():
    session_id = "test_checkout_user_789"
    # Add item
    client.post("/api/cart/items", json={
        "product_id": 1,
        "color": "Rose Gold & Cream",
        "quantity": 1,
        "session_id": session_id
    })

    # Checkout
    chk_res = client.post("/api/orders/checkout", json={
        "session_id": session_id,
        "customer_name": "Priyanka Roy",
        "customer_email": "priyanka@example.com",
        "customer_phone": "9876543210",
        "address_line1": "Flat 402, Royal Palms",
        "address_line2": "Koregaon Park",
        "city": "Pune",
        "state": "Maharashtra",
        "postal_code": "411001",
        "payment_method": "UPI",
        "coupon_code": "EJITAS10",
        "notes": "Please gift wrap with gold ribbon"
    })
    assert chk_res.status_code == 200
    order = chk_res.json()
    assert order["order_number"].startswith("EJT-2026-")
    assert order["discount"] == 349.9
    assert order["order_status"] == "Confirmed"
    assert len(order["items"]) == 1
    assert order["items"][0]["product_name"] == "The Royale Vanity Trunk"

    # Verify cart is empty after order
    cart_res = client.get(f"/api/cart?session_id={session_id}")
    assert cart_res.json()["items_count"] == 0

    # Retrieve order by order_number
    get_res = client.get(f"/api/orders/{order['order_number']}")
    assert get_res.status_code == 200
    assert get_res.json()["customer_name"] == "Priyanka Roy"

def test_details_stored_in_database_registry():
    # 1. Test newsletter subscription stores email
    sub_res = client.post("/api/concierge/newsletter", json={
        "email": "aanya.oberoi@example.com",
        "source": "home_vip_banner"
    })
    assert sub_res.status_code == 200
    assert sub_res.json()["success"] is True

    # 2. Test concierge styling inquiry stores contact details
    cnrg_res = client.post("/api/concierge/inquiry", json={
        "name": "Simran Khanna",
        "phone": "9812345678",
        "email": "simran.khanna@example.com",
        "occasion": "Bridal Trousseau Styling",
        "notes": "Need vanity case monogrammed for destination wedding in Jaipur"
    })
    assert cnrg_res.status_code == 200
    assert cnrg_res.json()["success"] is True

    # 3. Verify Admin records reflect all stored details in SQLite database
    admin_res = client.get("/api/admin/records")
    assert admin_res.status_code == 200
    records = admin_res.json()
    assert records["stats"]["total_orders"] >= 1
    assert any(c["email"] == "priyanka@example.com" for c in records["customers"])
    assert any(c["email"] == "simran.khanna@example.com" for c in records["customers"])
    assert any(n["email"] == "aanya.oberoi@example.com" for n in records["newsletter"])
    assert any(i["name"] == "Simran Khanna" for i in records["inquiries"])

def test_pages_render():
    assert client.get("/").status_code == 200
    assert client.get("/shop").status_code == 200
    assert client.get("/product/royale-vanity-trunk").status_code == 200
    assert client.get("/cart").status_code == 200
    assert client.get("/checkout").status_code == 200
    assert client.get("/wishlist").status_code == 200
    assert client.get("/admin").status_code == 200
