import re
from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import List, Optional, Dict, Any

def sanitize_text(v: str) -> str:
    """Removes script tags, HTML tags, and null bytes to prevent injection."""
    if not isinstance(v, str):
        return v
    # Remove HTML tags
    cleaned = re.sub(r'<[^>]*?>', '', v)
    # Remove control characters and null bytes
    cleaned = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]', '', cleaned)
    return cleaned.strip()

class ReviewCreate(BaseModel):
    author: str = Field(..., min_length=2, max_length=80)
    location: Optional[str] = "India"
    rating: int = Field(..., ge=1, le=5)
    title: Optional[str] = ""
    comment: str = Field(..., min_length=5, max_length=1000)

    @field_validator('author', 'location', 'title', 'comment', mode='before')
    @classmethod
    def sanitize_strings(cls, v):
        return sanitize_text(str(v)) if v is not None else ""

class ReviewOut(BaseModel):
    id: int
    product_id: int
    author: str
    location: Optional[str] = None
    rating: int
    title: Optional[str] = None
    comment: str
    verified: int
    created_at: str

class ProductOut(BaseModel):
    id: int
    slug: str
    name: str
    category: str
    category_slug: str
    price: float
    original_price: float
    discount_percent: int
    badge: Optional[str] = None
    rating: float
    reviews_count: int
    edition_tag: Optional[str] = None
    short_description: Optional[str] = None
    description: Optional[str] = None
    material: Optional[str] = None
    lining: Optional[str] = None
    hardware: Optional[str] = None
    dimensions: Optional[str] = None
    provenance: Optional[str] = None
    stock_quantity: int
    is_featured: int
    is_bestseller: int
    is_new: int
    colors: List[Dict[str, Any]]
    images: List[str]
    specifications: Dict[str, Any]
    reviews: Optional[List[ReviewOut]] = []

class CartItemAdd(BaseModel):
    product_id: int
    color: Optional[str] = None
    quantity: int = Field(1, ge=1)
    session_id: Optional[str] = "guest_default"

class CartItemUpdate(BaseModel):
    quantity: int = Field(..., ge=0)

class CartItemOut(BaseModel):
    id: int
    product_id: int
    name: str
    slug: str
    price: float
    original_price: float
    color: Optional[str] = None
    quantity: int
    image: str
    item_total: float

class CartOut(BaseModel):
    items: List[CartItemOut]
    items_count: int
    subtotal: float
    free_shipping_threshold: float = 1499.0
    free_shipping_unlocked: bool
    free_shipping_remaining: float
    shipping_fee: float
    estimated_total: float

class WishlistToggle(BaseModel):
    product_id: int
    session_id: Optional[str] = "guest_default"

class CouponApply(BaseModel):
    code: str
    cart_total: float

class CouponOut(BaseModel):
    valid: bool
    code: str
    discount_amount: float
    discount_percent: float
    message: str

class CheckoutRequest(BaseModel):
    session_id: Optional[str] = "guest_default"
    customer_name: str = Field(..., min_length=2, max_length=120)
    customer_email: str = Field(..., min_length=5, max_length=150)
    customer_phone: str = Field(..., min_length=6, max_length=30)
    address_line1: str = Field(..., min_length=3, max_length=255)
    address_line2: Optional[str] = ""
    landmark: Optional[str] = ""
    city: str = Field(..., min_length=2, max_length=100)
    state: str = Field(..., min_length=2, max_length=100)
    postal_code: str = Field(..., min_length=3, max_length=20)
    delivery_option: Optional[str] = "express"
    payment_method: str = "UPI"
    coupon_code: Optional[str] = ""
    notes: Optional[str] = ""

    @field_validator(
        'customer_name', 'customer_email', 'customer_phone',
        'address_line1', 'address_line2', 'landmark', 'city', 'state',
        'postal_code', 'delivery_option', 'payment_method', 'coupon_code', 'notes',
        mode='before'
    )
    @classmethod
    def sanitize_checkout_fields(cls, v):
        return sanitize_text(str(v)) if v is not None else ""

    @field_validator('customer_email')
    @classmethod
    def validate_email_format(cls, v):
        if "@" not in v or "." not in v:
            raise ValueError("Invalid email format")
        return v.lower()

class OrderItemOut(BaseModel):
    id: int
    product_id: int
    product_name: str
    product_image: str
    color: Optional[str]
    price: float
    quantity: int
    total: float

class OrderOut(BaseModel):
    id: int
    order_number: str
    customer_name: str
    customer_email: str
    customer_phone: str
    address_line1: str
    address_line2: Optional[str]
    landmark: Optional[str]
    city: str
    state: str
    postal_code: str
    delivery_option: str
    payment_method: str
    payment_status: str
    subtotal: float
    coupon_code: Optional[str]
    discount: float
    shipping_fee: float
    total: float
    order_status: str
    tracking_number: str
    estimated_delivery: str
    notes: Optional[str]
    created_at: str
    items: List[OrderItemOut]

class ConciergeRequest(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    phone: str = Field(..., min_length=6, max_length=30)
    email: Optional[str] = ""
    occasion: Optional[str] = "Bridal Trousseau"
    notes: Optional[str] = ""

    @field_validator('name', 'phone', 'email', 'occasion', 'notes', mode='before')
    @classmethod
    def sanitize_concierge_fields(cls, v):
        return sanitize_text(str(v)) if v is not None else ""

class NewsletterSubscribe(BaseModel):
    email: str
    source: Optional[str] = "vip_club_form"
