from fastapi import APIRouter, HTTPException
from backend.database import get_db
from backend.schemas import ConciergeRequest, NewsletterSubscribe

router = APIRouter(prefix="/api/concierge", tags=["Concierge & Inquiries"])

@router.post("/inquiry")
def submit_concierge_inquiry(req: ConciergeRequest):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO concierge_inquiries (name, phone, email, occasion, notes)
            VALUES (?, ?, ?, ?, ?)
        """, (req.name.strip(), req.phone.strip(), req.email.strip() if req.email else "", req.occasion, req.notes))
        
        inquiry_id = cursor.lastrowid

        # Also upsert into Customers database registry if email provided
        if req.email and req.email.strip():
            cursor.execute("""
                INSERT INTO customers (name, email, phone)
                VALUES (?, ?, ?)
                ON CONFLICT(email) DO UPDATE SET
                    name = excluded.name,
                    phone = excluded.phone,
                    updated_at = CURRENT_TIMESTAMP
            """, (req.name.strip(), req.email.strip().lower(), req.phone.strip()))

    # Trigger email notification to shaanventures1@gmail.com (outside DB transaction)
    try:
        from backend.services.email_service import notify_concierge_inquiry
        notify_concierge_inquiry({
            "id": inquiry_id,
            "name": req.name.strip(),
            "phone": req.phone.strip(),
            "email": req.email.strip() if req.email else "",
            "occasion": req.occasion,
            "notes": req.notes
        })
    except Exception as err:
        print(f"[Concierge Email Alert Error]: {err}")

    return {
        "success": True,
        "inquiry_id": inquiry_id,
        "message": f"Thank you, {req.name}. Your details have been securely recorded in our Atelier database. An Ejitas Stylist will contact you via WhatsApp shortly."
    }

@router.post("/newsletter")
def subscribe_newsletter(req: NewsletterSubscribe):
    email_clean = req.email.strip().lower()
    if not email_clean or "@" not in email_clean:
        raise HTTPException(status_code=400, detail="Please enter a valid email address.")

    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO newsletter_subscribers (email, source)
            VALUES (?, ?)
            ON CONFLICT(email) DO UPDATE SET
                source = excluded.source
        """, (email_clean, req.source or "vip_club_form"))

    # Trigger email alert (outside DB transaction)
    try:
        from backend.services.email_service import notify_newsletter_signup
        notify_newsletter_signup(email_clean, req.source or "vip_club_form")
    except Exception as err:
        print(f"[Newsletter Email Alert Error]: {err}")

    return {
        "success": True,
        "email": email_clean,
        "message": "Welcome to the Ejitas Privilege Club! Your details have been stored. Enjoy 10% off with coupon code EJITAS10."
    }
