from fastapi import APIRouter
from backend.database import get_db

router = APIRouter(prefix="/api/admin", tags=["Admin Database Records"])

@router.get("/records")
def get_all_database_records():
    with get_db() as conn:
        cursor = conn.cursor()

        # 1. Customers
        cursor.execute("SELECT * FROM customers ORDER BY id DESC")
        customers = [dict(r) for r in cursor.fetchall()]

        # 2. Orders with items count
        cursor.execute("""
            SELECT o.*, 
                   (SELECT COUNT(*) FROM order_items WHERE order_id = o.id) as items_count
            FROM orders o 
            ORDER BY o.id DESC
        """)
        orders = [dict(r) for r in cursor.fetchall()]

        # 3. Newsletter Subscribers
        cursor.execute("SELECT * FROM newsletter_subscribers ORDER BY id DESC")
        newsletter = [dict(r) for r in cursor.fetchall()]

        # 4. Concierge Inquiries
        cursor.execute("SELECT * FROM concierge_inquiries ORDER BY id DESC")
        inquiries = [dict(r) for r in cursor.fetchall()]

        # 5. Reviews
        cursor.execute("""
            SELECT r.*, p.name as product_name, p.slug as product_slug
            FROM reviews r
            LEFT JOIN products p ON r.product_id = p.id
            ORDER BY r.id DESC
        """)
        reviews = [dict(r) for r in cursor.fetchall()]

        # 6. Email Notifications Sent to shaanventures1@gmail.com
        cursor.execute("SELECT * FROM email_notifications ORDER BY id DESC LIMIT 50")
        emails = [dict(r) for r in cursor.fetchall()]

        # Stats
        total_revenue = sum(float(o["total"]) for o in orders)

        return {
            "stats": {
                "total_customers": len(customers),
                "total_orders": len(orders),
                "total_revenue": round(total_revenue, 2),
                "total_newsletter": len(newsletter),
                "total_inquiries": len(inquiries),
                "total_reviews": len(reviews),
                "total_emails_logged": len(emails)
            },
            "customers": customers,
            "orders": orders,
            "newsletter": newsletter,
            "inquiries": inquiries,
            "reviews": reviews,
            "emails": emails
        }
