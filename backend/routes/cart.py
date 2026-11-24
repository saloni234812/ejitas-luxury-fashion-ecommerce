import json
from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from backend.database import get_db
from backend.schemas import CartItemAdd, CartItemUpdate, CartOut, CartItemOut

router = APIRouter(prefix="/api/cart", tags=["Cart"])

def calculate_cart(session_id: str) -> CartOut:
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT c.id, c.product_id, c.color, c.quantity,
                   p.name, p.slug, p.price, p.original_price, p.images
            FROM cart_items c
            JOIN products p ON c.product_id = p.id
            WHERE c.session_id = ?
            ORDER BY c.created_at DESC
        """, (session_id,))
        
        rows = cursor.fetchall()
        items = []
        subtotal = 0.0
        total_items_count = 0

        for r in rows:
            img_list = json.loads(r["images"]) if r["images"] else []
            img_url = img_list[0] if img_list else ""
            item_tot = float(r["price"]) * int(r["quantity"])
            subtotal += item_tot
            total_items_count += int(r["quantity"])
            
            items.append(CartItemOut(
                id=r["id"],
                product_id=r["product_id"],
                name=r["name"],
                slug=r["slug"],
                price=r["price"],
                original_price=r["original_price"],
                color=r["color"],
                quantity=r["quantity"],
                image=img_url,
                item_total=round(item_tot, 2)
            ))

        free_thresh = 1499.0
        free_unlocked = subtotal >= free_thresh or subtotal == 0
        remaining = max(0.0, round(free_thresh - subtotal, 2)) if subtotal > 0 else free_thresh
        shipping_fee = 0.0 if (free_unlocked or subtotal == 0) else 150.0
        estimated_total = round(subtotal + shipping_fee, 2)

        return CartOut(
            items=items,
            items_count=total_items_count,
            subtotal=round(subtotal, 2),
            free_shipping_threshold=free_thresh,
            free_shipping_unlocked=free_unlocked,
            free_shipping_remaining=remaining,
            shipping_fee=shipping_fee,
            estimated_total=estimated_total
        )

@router.get("", response_model=CartOut)
def get_cart(session_id: str = Query("guest_default", description="Client session ID")):
    return calculate_cart(session_id)

@router.post("/items", response_model=CartOut)
def add_to_cart(item: CartItemAdd):
    session_id = item.session_id or "guest_default"
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, name FROM products WHERE id = ?", (item.product_id,))
        p = cursor.fetchone()
        if not p:
            raise HTTPException(status_code=404, detail="Product not found")

        # Check if item with same session_id, product_id, and color already exists
        cursor.execute("""
            SELECT id, quantity FROM cart_items
            WHERE session_id = ? AND product_id = ? AND (color = ? OR (color IS NULL AND ? IS NULL))
        """, (session_id, item.product_id, item.color, item.color))
        existing = cursor.fetchone()

        if existing:
            new_qty = existing["quantity"] + item.quantity
            cursor.execute("UPDATE cart_items SET quantity = ? WHERE id = ?", (new_qty, existing["id"]))
        else:
            cursor.execute("""
                INSERT INTO cart_items (session_id, product_id, color, quantity)
                VALUES (?, ?, ?, ?)
            """, (session_id, item.product_id, item.color, item.quantity))

    return calculate_cart(session_id)

@router.put("/items/{item_id}", response_model=CartOut)
def update_cart_item(item_id: int, update: CartItemUpdate, session_id: str = Query("guest_default")):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM cart_items WHERE id = ? AND session_id = ?", (item_id, session_id))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Cart item not found")

        if update.quantity <= 0:
            cursor.execute("DELETE FROM cart_items WHERE id = ?", (item_id,))
        else:
            cursor.execute("UPDATE cart_items SET quantity = ? WHERE id = ?", (update.quantity, item_id))

    return calculate_cart(session_id)

@router.delete("/items/{item_id}", response_model=CartOut)
def remove_from_cart(item_id: int, session_id: str = Query("guest_default")):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM cart_items WHERE id = ? AND session_id = ?", (item_id, session_id))
    return calculate_cart(session_id)

@router.delete("", response_model=CartOut)
def clear_cart(session_id: str = Query("guest_default")):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM cart_items WHERE session_id = ?", (session_id,))
    return calculate_cart(session_id)
