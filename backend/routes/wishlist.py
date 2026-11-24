from fastapi import APIRouter, HTTPException, Query
from typing import List
from backend.database import get_db
from backend.schemas import WishlistToggle, ProductOut
from backend.routes.products import format_product_row

router = APIRouter(prefix="/api/wishlist", tags=["Wishlist"])

@router.get("", response_model=List[ProductOut])
def get_wishlist(session_id: str = Query("guest_default")):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT p.* FROM wishlist_items w
            JOIN products p ON w.product_id = p.id
            WHERE w.session_id = ?
            ORDER BY w.created_at DESC
        """, (session_id,))
        rows = cursor.fetchall()
        return [format_product_row(r) for r in rows]

@router.get("/ids")
def get_wishlist_ids(session_id: str = Query("guest_default")):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT product_id FROM wishlist_items WHERE session_id = ?", (session_id,))
        return [r["product_id"] for r in cursor.fetchall()]

@router.post("/toggle")
def toggle_wishlist(data: WishlistToggle):
    session_id = data.session_id or "guest_default"
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM products WHERE id = ?", (data.product_id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Product not found")

        cursor.execute(
            "SELECT id FROM wishlist_items WHERE session_id = ? AND product_id = ?",
            (session_id, data.product_id)
        )
        row = cursor.fetchone()
        if row:
            cursor.execute("DELETE FROM wishlist_items WHERE id = ?", (row["id"],))
            is_wishlisted = False
        else:
            cursor.execute(
                "INSERT INTO wishlist_items (session_id, product_id) VALUES (?, ?)",
                (session_id, data.product_id)
            )
            is_wishlisted = True

        cursor.execute("SELECT COUNT(*) FROM wishlist_items WHERE session_id = ?", (session_id,))
        total_count = cursor.fetchone()[0]

        return {
            "product_id": data.product_id,
            "is_wishlisted": is_wishlisted,
            "total_count": total_count,
            "message": "Added to wishlist" if is_wishlisted else "Removed from wishlist"
        }
