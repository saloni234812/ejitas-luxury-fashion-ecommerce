import json
import random
import string
from datetime import datetime, timedelta
from fastapi import APIRouter, HTTPException, Query
from backend.database import get_db
from backend.schemas import CheckoutRequest, OrderOut, OrderItemOut

router = APIRouter(prefix="/api/orders", tags=["Orders"])

def generate_order_number():
    random_digits = ''.join(random.choices(string.digits, k=5))
    return f"EJT-2026-{random_digits}"

def generate_tracking_number():
    return f"EJT-EXP-IN{''.join(random.choices(string.digits, k=8))}"

@router.post("/checkout", response_model=OrderOut)
def process_checkout(req: CheckoutRequest):
    session_id = req.session_id or "guest_default"
    
    with get_db() as conn:
        cursor = conn.cursor()
        
        # 1. Fetch current cart items
        cursor.execute("""
            SELECT c.id, c.product_id, c.color, c.quantity,
                   p.name, p.price, p.images
            FROM cart_items c
            JOIN products p ON c.product_id = p.id
            WHERE c.session_id = ?
        """, (session_id,))
        cart_rows = cursor.fetchall()
        
        if not cart_rows:
            raise HTTPException(status_code=400, detail="Your shopping bag is empty. Please add items to checkout.")

        # 2. Calculate Subtotal
        subtotal = 0.0
        line_items_data = []
        for r in cart_rows:
            img_list = json.loads(r["images"]) if r["images"] else []
            img_url = img_list[0] if img_list else ""
            item_total = float(r["price"]) * int(r["quantity"])
            subtotal += item_total
            line_items_data.append({
                "product_id": r["product_id"],
                "product_name": r["name"],
                "product_image": img_url,
                "color": r["color"] or "Classic Atelier",
                "price": float(r["price"]),
                "quantity": int(r["quantity"]),
                "total": round(item_total, 2)
            })

        # 3. Calculate Shipping (Free above ₹1,499)
        shipping_fee = 0.0 if subtotal >= 1499.0 else 150.0

        # 4. Calculate Discount if coupon provided
        discount = 0.0
        applied_coupon = None
        if req.coupon_code:
            code_clean = req.coupon_code.strip().upper()
            cursor.execute("SELECT * FROM coupons WHERE code = ? AND is_active = 1", (code_clean,))
            c_row = cursor.fetchone()
            if c_row and subtotal >= c_row["min_order"]:
                applied_coupon = code_clean
                if c_row["discount_percent"]:
                    discount = round((subtotal * c_row["discount_percent"]) / 100.0, 2)
                elif c_row["discount_amount"]:
                    discount = min(subtotal, c_row["discount_amount"])

        final_total = max(0.0, round(subtotal - discount + shipping_fee, 2))

        # 5. Metadata
        order_num = generate_order_number()
        tracking_num = generate_tracking_number()
        est_delivery = (datetime.now() + timedelta(days=3)).strftime("%d %B, %Y")
        created_at_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # 6. Insert Order
        cursor.execute("""
            INSERT INTO orders (
                order_number, session_id, customer_name, customer_email, customer_phone,
                address_line1, address_line2, landmark, city, state, postal_code,
                delivery_option, payment_method, payment_status, subtotal, coupon_code,
                discount, shipping_fee, total, order_status, tracking_number,
                estimated_delivery, notes, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            order_num, session_id, req.customer_name, req.customer_email, req.customer_phone,
            req.address_line1, req.address_line2, req.landmark, req.city, req.state, req.postal_code,
            req.delivery_option or "express", req.payment_method, "Paid", subtotal, applied_coupon,
            discount, shipping_fee, final_total, "Confirmed", tracking_num,
            est_delivery, req.notes, created_at_str
        ))
        order_id = cursor.lastrowid

        # 6b. Upsert into Customers table to permanently maintain customer details in database
        cursor.execute("""
            INSERT INTO customers (
                name, email, phone, address_line1, address_line2, landmark,
                city, state, postal_code, total_orders, total_spent, last_order_date
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 1, ?, CURRENT_TIMESTAMP)
            ON CONFLICT(email) DO UPDATE SET
                name = excluded.name,
                phone = excluded.phone,
                address_line1 = excluded.address_line1,
                address_line2 = excluded.address_line2,
                landmark = excluded.landmark,
                city = excluded.city,
                state = excluded.state,
                postal_code = excluded.postal_code,
                total_orders = customers.total_orders + 1,
                total_spent = customers.total_spent + excluded.total_spent,
                last_order_date = CURRENT_TIMESTAMP,
                updated_at = CURRENT_TIMESTAMP
        """, (
            req.customer_name, req.customer_email, req.customer_phone,
            req.address_line1, req.address_line2, req.landmark,
            req.city, req.state, req.postal_code, final_total
        ))

        # 7. Insert Order Items
        order_items_out = []
        for li in line_items_data:
            cursor.execute("""
                INSERT INTO order_items (
                    order_id, product_id, product_name, product_image, color, price, quantity, total
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                order_id, li["product_id"], li["product_name"], li["product_image"],
                li["color"], li["price"], li["quantity"], li["total"]
            ))
            li_id = cursor.lastrowid
            order_items_out.append(OrderItemOut(
                id=li_id,
                product_id=li["product_id"],
                product_name=li["product_name"],
                product_image=li["product_image"],
                color=li["color"],
                price=li["price"],
                quantity=li["quantity"],
                total=li["total"]
            ))

        # 8. Clear user's cart
        cursor.execute("DELETE FROM cart_items WHERE session_id = ?", (session_id,))

    # 9. Dispatch email notification to shaanventures1@gmail.com & record in database (outside DB transaction)
    order_dict_for_email = {
        "order_number": order_num,
        "customer_name": req.customer_name,
        "customer_email": req.customer_email,
        "customer_phone": req.customer_phone,
        "address_line1": req.address_line1,
        "address_line2": req.address_line2,
        "landmark": req.landmark,
        "city": req.city,
        "state": req.state,
        "postal_code": req.postal_code,
        "delivery_option": req.delivery_option or "express",
        "payment_method": req.payment_method,
        "subtotal": subtotal,
        "coupon_code": applied_coupon,
        "discount": discount,
        "shipping_fee": shipping_fee,
        "total": final_total,
        "tracking_number": tracking_num,
        "notes": req.notes
    }
    try:
        from backend.services.email_service import notify_new_order
        notify_new_order(order_dict_for_email, line_items_data)
    except Exception as email_err:
        print(f"[Email Notification Error]: {email_err}")

    return OrderOut(
        id=order_id,
        order_number=order_num,
        customer_name=req.customer_name,
        customer_email=req.customer_email,
        customer_phone=req.customer_phone,
        address_line1=req.address_line1,
        address_line2=req.address_line2,
        landmark=req.landmark,
        city=req.city,
        state=req.state,
        postal_code=req.postal_code,
        delivery_option=req.delivery_option or "express",
        payment_method=req.payment_method,
        payment_status="Paid",
        subtotal=subtotal,
        coupon_code=applied_coupon,
        discount=discount,
        shipping_fee=shipping_fee,
        total=final_total,
        order_status="Confirmed",
        tracking_number=tracking_num,
        estimated_delivery=est_delivery,
        notes=req.notes,
        created_at=created_at_str,
        items=order_items_out
    )

@router.get("/{order_number_or_id}", response_model=OrderOut)
def get_order(order_number_or_id: str):
    with get_db() as conn:
        cursor = conn.cursor()
        if order_number_or_id.isdigit():
            cursor.execute("SELECT * FROM orders WHERE id = ?", (int(order_number_or_id),))
        else:
            cursor.execute("SELECT * FROM orders WHERE order_number = ?", (order_number_or_id,))
            
        row = cursor.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Order not found")

        order_id = row["id"]
        cursor.execute("SELECT * FROM order_items WHERE order_id = ?", (order_id,))
        item_rows = cursor.fetchall()
        
        items = [OrderItemOut(
            id=i["id"],
            product_id=i["product_id"],
            product_name=i["product_name"],
            product_image=i["product_image"],
            color=i["color"],
            price=i["price"],
            quantity=i["quantity"],
            total=i["total"]
        ) for i in item_rows]

        return OrderOut(
            id=row["id"],
            order_number=row["order_number"],
            customer_name=row["customer_name"],
            customer_email=row["customer_email"],
            customer_phone=row["customer_phone"],
            address_line1=row["address_line1"],
            address_line2=row["address_line2"],
            landmark=row["landmark"],
            city=row["city"],
            state=row["state"],
            postal_code=row["postal_code"],
            delivery_option=row["delivery_option"],
            payment_method=row["payment_method"],
            payment_status=row["payment_status"],
            subtotal=row["subtotal"],
            coupon_code=row["coupon_code"],
            discount=row["discount"],
            shipping_fee=row["shipping_fee"],
            total=row["total"],
            order_status=row["order_status"],
            tracking_number=row["tracking_number"],
            estimated_delivery=row["estimated_delivery"],
            notes=row["notes"],
            created_at=row["created_at"],
            items=items
        )
