import os
import smtplib
import json
import logging
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path
from datetime import datetime
from backend.database import get_db

logger = logging.getLogger("ejitas.email")
logger.setLevel(logging.INFO)

# File logger for email events
LOGS_DIR = Path(__file__).resolve().parent.parent.parent / "logs"
LOGS_DIR.mkdir(parents=True, exist_ok=True)
file_handler = logging.FileHandler(LOGS_DIR / "email_notifications.log", encoding="utf-8")
file_handler.setFormatter(logging.Formatter("[%(asctime)s] %(levelname)s: %(message)s"))
logger.addHandler(file_handler)

ADMIN_EMAIL = os.getenv("ADMIN_EMAIL", "shaanventures1@gmail.com")
SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER", "")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", os.getenv("SMTP_APP_PASSWORD", ""))
SMTP_FROM = os.getenv("SMTP_FROM", f"Ejitas Atelier <{SMTP_USER or 'atelier@ejitas.com'}>")

def record_email_in_db(recipient: str, subject: str, event_type: str, reference_id: str, payload: dict, status: str):
    """Permanently store email notification records in the SQLite database."""
    try:
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO email_notifications (recipient, subject, event_type, reference_id, payload_json, status)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (recipient, subject, event_type, str(reference_id), json.dumps(payload, ensure_ascii=False), status))
    except Exception as e:
        logger.error(f"Failed to record email in database: {e}")

def _dispatch_smtp(to_email: str, subject: str, html_content: str, text_content: str) -> bool:
    """Attempts live SMTP dispatch. If credentials not configured, safely logs and stores."""
    if not SMTP_USER or not SMTP_PASSWORD:
        logger.info(f"[OFFLINE/MOCK EMAIL DISPATCH] To: {to_email} | Subject: {subject}")
        return False

    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = SMTP_FROM
        msg["To"] = to_email

        msg.attach(MIMEText(text_content, "plain", "utf-8"))
        msg.attach(MIMEText(html_content, "html", "utf-8"))

        with smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=10) as server:
            server.ehlo()
            server.starttls()
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.sendmail(SMTP_FROM, [to_email], msg.as_string())

        logger.info(f"[SMTP SENT] Successfully sent email to {to_email}: {subject}")
        return True
    except Exception as e:
        logger.error(f"[SMTP ERROR] Failed to send email via {SMTP_HOST}:{SMTP_PORT} to {to_email}: {e}")
        return False

def notify_new_order(order_data: dict, line_items: list):
    """
    Sends detailed order notification to shaanventures1@gmail.com
    and records all details permanently in the database and audit log.
    """
    order_num = order_data.get("order_number", "N/A")
    cust_name = order_data.get("customer_name", "Valued Customer")
    cust_email = order_data.get("customer_email", "N/A")
    cust_phone = order_data.get("customer_phone", "N/A")
    total_amount = float(order_data.get("total", 0.0))
    payment_method = order_data.get("payment_method", "Prepaid")

    subject = f"👑 [EJITAS NEW ORDER] {order_num} • ₹{total_amount:,.2f} from {cust_name}"

    # Build items HTML table
    items_rows_html = ""
    items_rows_text = ""
    for item in line_items:
        p_name = item.get("product_name", "Luxury Bag")
        p_color = item.get("color", "Classic")
        p_qty = item.get("quantity", 1)
        p_price = float(item.get("price", 0.0))
        p_total = float(item.get("total", p_price * p_qty))
        
        items_rows_html += f"""
        <tr style="border-bottom: 1px solid #eae8e5;">
            <td style="padding: 10px; font-weight: 500;">{p_name}</td>
            <td style="padding: 10px; color: #6e353d;">{p_color}</td>
            <td style="padding: 10px; text-align: center;">{p_qty}</td>
            <td style="padding: 10px; text-align: right;">₹{p_price:,.2f}</td>
            <td style="padding: 10px; text-align: right; font-weight: bold;">₹{p_total:,.2f}</td>
        </tr>
        """
        items_rows_text += f"- {p_name} ({p_color}) x {p_qty}: ₹{p_total:,.2f}\n"

    address_full = f"{order_data.get('address_line1', '')}, {order_data.get('address_line2', '') or ''}".strip(", ")
    landmark = order_data.get("landmark", "")
    city_state_pin = f"{order_data.get('city', '')}, {order_data.get('state', '')} - {order_data.get('postal_code', '')}"

    shipping_val = float(order_data.get('shipping_fee', 0.0))
    shipping_str = "FREE Express" if shipping_val == 0 else f"₹{shipping_val:,.2f}"
    discount_val = float(order_data.get('discount', 0.0))
    coupon_code = order_data.get('coupon_code', '')
    discount_row_html = f"<div style='color: #ba1a1a;'>Coupon ({coupon_code}): -₹{discount_val:,.2f}</div>" if discount_val > 0 else ""

    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head><meta charset="utf-8"/></head>
    <body style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; background-color: #fbf9f6; color: #1b1c1a; padding: 20px; margin: 0;">
        <div style="max-width: 650px; margin: 0 auto; background-color: #ffffff; border-radius: 12px; border: 1px solid #e4e2df; overflow: hidden; box-shadow: 0 4px 20px rgba(0,0,0,0.06);">
            
            <!-- Header Banner -->
            <div style="background-color: #1c1b1b; color: #ffffff; padding: 24px; text-align: center; border-bottom: 3px solid #8a4c54;">
                <h1 style="margin: 0; font-family: 'Playfair Display', Georgia, serif; font-size: 24px; letter-spacing: 2px;">EJITAS</h1>
                <p style="margin: 4px 0 0 0; font-size: 11px; text-transform: uppercase; letter-spacing: 3px; color: #ffd9dc;">Fragrance of Royalty • Shaan Ventures Pvt Ltd</p>
                <div style="display: inline-block; background-color: #8a4c54; color: #ffffff; font-size: 12px; padding: 4px 12px; border-radius: 20px; margin-top: 12px; font-weight: bold;">
                    NEW CUSTOMER ORDER RECEIVED
                </div>
            </div>

            <!-- Order Snapshot -->
            <div style="padding: 24px; background-color: #f5f3f0; border-bottom: 1px solid #e4e2df;">
                <table style="width: 100%; border-collapse: collapse;">
                    <tr>
                        <td style="font-size: 13px; color: #747878;">Order Number:</td>
                        <td style="font-size: 15px; font-weight: bold; text-align: right; color: #8a4c54;">{order_num}</td>
                    </tr>
                    <tr>
                        <td style="font-size: 13px; color: #747878;">Total Paid:</td>
                        <td style="font-size: 18px; font-weight: bold; text-align: right; color: #1b1c1a;">₹{total_amount:,.2f}</td>
                    </tr>
                    <tr>
                        <td style="font-size: 13px; color: #747878;">Payment Method:</td>
                        <td style="font-size: 13px; text-align: right; font-weight: 500;">{payment_method}</td>
                    </tr>
                    <tr>
                        <td style="font-size: 13px; color: #747878;">Tracking Number:</td>
                        <td style="font-size: 13px; text-align: right; font-family: monospace;">{order_data.get('tracking_number', 'Assigned')}</td>
                    </tr>
                </table>
            </div>

            <!-- Customer & Shipping Details -->
            <div style="padding: 24px; border-bottom: 1px solid #e4e2df;">
                <h3 style="margin-top: 0; font-size: 15px; color: #8a4c54; text-transform: uppercase; letter-spacing: 1px; border-bottom: 1px solid #eee; padding-bottom: 8px;">Customer & Shipping Address</h3>
                <table style="width: 100%; font-size: 14px; line-height: 1.6;">
                    <tr>
                        <td style="width: 35%; color: #747878;">Full Name:</td>
                        <td style="font-weight: 600;">{cust_name}</td>
                    </tr>
                    <tr>
                        <td style="color: #747878;">Email Address:</td>
                        <td><a href="mailto:{cust_email}" style="color: #8a4c54; text-decoration: none;">{cust_email}</a></td>
                    </tr>
                    <tr>
                        <td style="color: #747878;">Phone / WhatsApp:</td>
                        <td style="font-weight: 600;"><a href="tel:{cust_phone}" style="color: #1b1c1a; text-decoration: none;">{cust_phone}</a></td>
                    </tr>
                    <tr>
                        <td style="color: #747878; vertical-align: top;">Delivery Address:</td>
                        <td>
                            {address_full}<br/>
                            {f"Landmark: {landmark}<br/>" if landmark else ""}
                            {city_state_pin}
                        </td>
                    </tr>
                    <tr>
                        <td style="color: #747878;">Special Notes:</td>
                        <td style="font-style: italic;">{order_data.get('notes') or 'None specified'}</td>
                    </tr>
                </table>
            </div>

            <!-- Items Ordered -->
            <div style="padding: 24px;">
                <h3 style="margin-top: 0; font-size: 15px; color: #8a4c54; text-transform: uppercase; letter-spacing: 1px; border-bottom: 1px solid #eee; padding-bottom: 8px;">Ordered Bag Items</h3>
                <table style="width: 100%; border-collapse: collapse; font-size: 13px;">
                    <thead>
                        <tr style="background-color: #f5f3f0; text-align: left; font-size: 11px; text-transform: uppercase; color: #747878;">
                            <th style="padding: 8px 10px;">Item</th>
                            <th style="padding: 8px 10px;">Finish/Color</th>
                            <th style="padding: 8px 10px; text-align: center;">Qty</th>
                            <th style="padding: 8px 10px; text-align: right;">Unit Price</th>
                            <th style="padding: 8px 10px; text-align: right;">Subtotal</th>
                        </tr>
                    </thead>
                    <tbody>
                        {items_rows_html}
                    </tbody>
                </table>

                <div style="margin-top: 16px; text-align: right; font-size: 14px;">
                    <div>Subtotal: <strong>₹{float(order_data.get('subtotal', 0)):,.2f}</strong></div>
                    {discount_row_html}
                    <div>Shipping: <strong>{shipping_str}</strong></div>
                    <div style="font-size: 18px; color: #8a4c54; font-weight: bold; margin-top: 6px; border-top: 1px solid #ddd; padding-top: 6px;">
                        Final Total: ₹{total_amount:,.2f}
                    </div>
                </div>
            </div>

            <!-- Footer -->
            <div style="background-color: #efeeeb; padding: 16px 24px; text-align: center; font-size: 12px; color: #747878; border-top: 1px solid #e4e2df;">
                This automated notification was generated by Ejitas Luxury E-Commerce Engine for Shaan Ventures Pvt Ltd.<br/>
                All records are archived securely in the central atelier database.
            </div>
        </div>
    </body>
    </html>
    """

    text_content = f"""
EJITAS LUXURY E-COMMERCE - NEW ORDER RECEIVED
=====================================================
Order Number: {order_num}
Total: ₹{total_amount:,.2f}
Payment Method: {payment_method}
Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

CUSTOMER & SHIPPING DETAILS:
----------------------------
Name: {cust_name}
Email: {cust_email}
Phone: {cust_phone}
Address: {address_full}
City/State/PIN: {city_state_pin}
Landmark: {landmark}
Notes: {order_data.get('notes', 'None')}

ORDERED ITEMS:
--------------
{items_rows_text}

Subtotal: ₹{float(order_data.get('subtotal', 0)):,.2f}
Discount: ₹{float(order_data.get('discount', 0)):,.2f}
Total Paid: ₹{total_amount:,.2f}
=====================================================
    """

    sent = _dispatch_smtp(ADMIN_EMAIL, subject, html_content, text_content)
    status = "sent" if sent else "logged_and_stored"
    
    payload = {
        "order": order_data,
        "items": line_items,
        "timestamp": datetime.now().isoformat()
    }
    record_email_in_db(ADMIN_EMAIL, subject, "order_placed", order_num, payload, status)
    logger.info(f"Order notification processed for {order_num} (Status: {status})")
    return status

def notify_concierge_inquiry(inquiry_data: dict):
    """Sends notification when a user books Concierge styling / bridal assistance."""
    name = inquiry_data.get("name", "Guest")
    phone = inquiry_data.get("phone", "N/A")
    email = inquiry_data.get("email", "N/A")
    occasion = inquiry_data.get("occasion", "General Styling Inquiry")
    notes = inquiry_data.get("notes", "No notes provided")

    subject = f"✨ [EJITAS CONCIERGE INQUIRY] New request from {name} ({phone})"

    html_content = f"""
    <!DOCTYPE html>
    <html>
    <body style="font-family: -apple-system, BlinkMacSystemFont, sans-serif; background-color: #fbf9f6; color: #1b1c1a; padding: 20px;">
        <div style="max-width: 600px; margin: 0 auto; background-color: #ffffff; border-radius: 12px; border: 1px solid #e4e2df; overflow: hidden;">
            <div style="background-color: #1c1b1b; color: #ffffff; padding: 20px; text-align: center;">
                <h2 style="margin: 0; font-family: Georgia, serif; letter-spacing: 2px;">EJITAS CONCIERGE</h2>
                <p style="margin: 4px 0 0; font-size: 11px; text-transform: uppercase; color: #ffd9dc;">New Styling & Bridal Trousseau Lead</p>
            </div>
            <div style="padding: 24px; font-size: 14px; line-height: 1.6;">
                <p><strong>Customer Name:</strong> {name}</p>
                <p><strong>Phone / WhatsApp:</strong> <a href="tel:{phone}">{phone}</a> | <a href="https://wa.me/{phone.replace(' ', '').replace('+', '')}">Message on WhatsApp</a></p>
                <p><strong>Email Address:</strong> <a href="mailto:{email}">{email}</a></p>
                <p><strong>Occasion / Need:</strong> {occasion}</p>
                <p><strong>Customer Notes:</strong> {notes}</p>
            </div>
            <div style="background-color: #efeeeb; padding: 12px; text-align: center; font-size: 11px; color: #747878;">
                Shaan Ventures Pvt Ltd • Stored in Ejitas Database
            </div>
        </div>
    </body>
    </html>
    """
    text_content = f"New Concierge Inquiry:\nName: {name}\nPhone: {phone}\nEmail: {email}\nOccasion: {occasion}\nNotes: {notes}"

    sent = _dispatch_smtp(ADMIN_EMAIL, subject, html_content, text_content)
    status = "sent" if sent else "logged_and_stored"
    record_email_in_db(ADMIN_EMAIL, subject, "concierge_inquiry", str(inquiry_data.get("id", "inq")), inquiry_data, status)
    return status

def notify_newsletter_signup(email: str, source: str = "website_footer"):
    """Sends notification when a user subscribes to the VIP Privilege Club."""
    subject = f"💌 [EJITAS VIP CLUB] New Subscriber: {email}"
    html_content = f"<p>A new customer joined the VIP club:</p><h3>{email}</h3><p>Source: {source}</p>"
    text_content = f"New VIP Club Subscriber: {email} (Source: {source})"

    sent = _dispatch_smtp(ADMIN_EMAIL, subject, html_content, text_content)
    status = "sent" if sent else "logged_and_stored"
    record_email_in_db(ADMIN_EMAIL, subject, "newsletter_signup", email, {"email": email, "source": source}, status)
    return status
