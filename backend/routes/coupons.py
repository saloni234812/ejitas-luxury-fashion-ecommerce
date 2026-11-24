from fastapi import APIRouter
from backend.database import get_db
from backend.schemas import CouponApply, CouponOut

router = APIRouter(prefix="/api/coupons", tags=["Coupons"])

@router.post("/apply", response_model=CouponOut)
def apply_coupon(data: CouponApply):
    code_clean = data.code.strip().upper()
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM coupons WHERE code = ? AND is_active = 1", (code_clean,))
        row = cursor.fetchone()

        if not row:
            return CouponOut(
                valid=False,
                code=code_clean,
                discount_amount=0.0,
                discount_percent=0.0,
                message=f"Coupon code '{code_clean}' is invalid or expired."
            )

        min_order = row["min_order"]
        if data.cart_total < min_order:
            return CouponOut(
                valid=False,
                code=code_clean,
                discount_amount=0.0,
                discount_percent=0.0,
                message=f"Code '{code_clean}' requires minimum order of ₹{min_order:,.0f}."
            )

        discount_amount = 0.0
        percent = row["discount_percent"] or 0.0
        fixed = row["discount_amount"] or 0.0

        if percent > 0:
            discount_amount = round((data.cart_total * percent) / 100.0, 2)
        elif fixed > 0:
            discount_amount = min(data.cart_total, fixed)

        return CouponOut(
            valid=True,
            code=code_clean,
            discount_amount=discount_amount,
            discount_percent=percent,
            message=f"Luxury privilege applied! Saved ₹{discount_amount:,.2f}"
        )

@router.get("")
def list_coupons():
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT code, discount_percent, discount_amount, min_order, description FROM coupons WHERE is_active = 1")
        return [dict(r) for r in cursor.fetchall()]
