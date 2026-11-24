import json
from fastapi import APIRouter, HTTPException, Query
from typing import Optional, List
from backend.database import get_db
from backend.schemas import ProductOut, ReviewCreate, ReviewOut

router = APIRouter(prefix="/api/products", tags=["Products"])

def format_product_row(row, include_reviews=False):
    p = dict(row)
    p["colors"] = json.loads(p["colors"]) if p.get("colors") else []
    p["images"] = json.loads(p["images"]) if p.get("images") else []
    p["specifications"] = json.loads(p["specifications"]) if p.get("specifications") else {}
    
    if include_reviews:
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM reviews WHERE product_id = ? ORDER BY created_at DESC",
                (p["id"],)
            )
            reviews = [dict(r) for r in cursor.fetchall()]
            p["reviews"] = reviews
    else:
        p["reviews"] = []
        
    return p

@router.get("", response_model=List[ProductOut])
def list_products(
    category: Optional[str] = Query(None, description="Category slug e.g. vanity, sling, totes, organisers"),
    search: Optional[str] = Query(None, description="Search query in name or description"),
    sort: Optional[str] = Query("featured", description="Sorting: featured, bestseller, price-asc, price-desc, newest"),
    limit: int = 50,
    offset: int = 0
):
    with get_db() as conn:
        cursor = conn.cursor()
        query = "SELECT * FROM products WHERE 1=1"
        params = []

        if category and category.lower() != "all":
            query += " AND (category_slug = ? OR LOWER(category) LIKE ?)"
            params.extend([category.lower(), f"%{category.lower()}%"])

        if search:
            query += " AND (name LIKE ? OR description LIKE ? OR material LIKE ?)"
            s = f"%{search}%"
            params.extend([s, s, s])

        # Sorting logic
        if sort == "price-asc":
            query += " ORDER BY price ASC"
        elif sort == "price-desc":
            query += " ORDER BY price DESC"
        elif sort == "bestseller":
            query += " ORDER BY is_bestseller DESC, rating DESC, reviews_count DESC"
        elif sort == "newest":
            query += " ORDER BY is_new DESC, id DESC"
        else:
            query += " ORDER BY is_featured DESC, rating DESC, id ASC"

        query += " LIMIT ? OFFSET ?"
        params.extend([limit, offset])

        cursor.execute(query, params)
        rows = cursor.fetchall()
        return [format_product_row(r) for r in rows]

@router.get("/categories")
def get_categories():
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT category, category_slug, COUNT(*) as count, MIN(price) as min_price,
                   (SELECT json_extract(images, '$[0]') FROM products p2 WHERE p2.category_slug = p1.category_slug LIMIT 1) as cover_image
            FROM products p1
            GROUP BY category, category_slug
            ORDER BY count DESC
        """)
        return [dict(r) for r in cursor.fetchall()]

@router.get("/{id_or_slug}", response_model=ProductOut)
def get_product(id_or_slug: str):
    with get_db() as conn:
        cursor = conn.cursor()
        if id_or_slug.isdigit():
            cursor.execute("SELECT * FROM products WHERE id = ?", (int(id_or_slug),))
        else:
            cursor.execute("SELECT * FROM products WHERE slug = ?", (id_or_slug,))
            
        row = cursor.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Product not found")
            
        return format_product_row(row, include_reviews=True)

@router.post("/{product_id}/reviews", response_model=ReviewOut)
def add_product_review(product_id: int, review: ReviewCreate):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM products WHERE id = ?", (product_id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Product not found")

        cursor.execute("""
            INSERT INTO reviews (product_id, author, location, rating, title, comment, verified)
            VALUES (?, ?, ?, ?, ?, ?, 1)
        """, (product_id, review.author, review.location or "Verified Buyer", review.rating, review.title, review.comment))
        
        review_id = cursor.lastrowid
        
        # Update product aggregate rating & reviews_count
        cursor.execute("""
            SELECT AVG(rating), COUNT(*) FROM reviews WHERE product_id = ?
        """, (product_id,))
        avg_rating, count = cursor.fetchone()
        
        cursor.execute("""
            UPDATE products SET rating = ROUND(?, 1), reviews_count = ? WHERE id = ?
        """, (avg_rating, count, product_id))
        
        cursor.execute("SELECT * FROM reviews WHERE id = ?", (review_id,))
        return dict(cursor.fetchone())
