import os
from pathlib import Path
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware

from backend.database import init_db, get_db
from backend.seed_data import seed_database
from backend.routes.products import router as products_router, format_product_row
from backend.routes.cart import router as cart_router
from backend.routes.wishlist import router as wishlist_router
from backend.routes.orders import router as orders_router
from backend.routes.coupons import router as coupons_router
from backend.routes.concierge import router as concierge_router
from backend.routes.admin import router as admin_router

BASE_DIR = Path(__file__).resolve().parent.parent

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize DB and seed on startup
    init_db()
    seed_database()
    yield

app = FastAPI(
    title="Ejitas Luxury Fashion E-Commerce API",
    description="REST API and web application for Ejitas handcrafted vanity cases, bags, and organizers.",
    version="1.0.0",
    lifespan=lifespan
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Comprehensive Security & Rate Limiting Middleware
import time
from collections import defaultdict
from fastapi.responses import JSONResponse

RATE_LIMIT_STORAGE = defaultdict(list)
RATE_LIMIT_WINDOW = 60  # seconds
RATE_LIMIT_MAX_CHECKOUT = 15  # requests per minute
RATE_LIMIT_MAX_API = 120  # requests per minute

@app.middleware("http")
async def security_and_rate_limit_middleware(request: Request, call_next):
    # 1. Protection against oversized payloads (DoS mitigation)
    content_length = request.headers.get("content-length")
    if content_length and int(content_length) > 5 * 1024 * 1024:  # 5MB limit
        return JSONResponse(status_code=413, content={"detail": "Payload too large. Maximum size is 5MB."})

    # 2. Rate Limiting on sensitive endpoints
    client_ip = request.client.host if request.client else "unknown"
    path = request.url.path
    now = time.time()

    if path.startswith("/api/orders/checkout") or path.startswith("/api/concierge"):
        # Purge timestamps older than window
        timestamps = [t for t in RATE_LIMIT_STORAGE[client_ip] if now - t < RATE_LIMIT_WINDOW]
        RATE_LIMIT_STORAGE[client_ip] = timestamps
        
        limit = RATE_LIMIT_MAX_CHECKOUT if path.startswith("/api/orders/checkout") else RATE_LIMIT_MAX_API
        if len(timestamps) >= limit:
            return JSONResponse(
                status_code=429,
                content={"detail": "Too many requests. For security reasons, please wait a moment before trying again."}
            )
        RATE_LIMIT_STORAGE[client_ip].append(now)

    # 3. Process Request
    response = await call_next(request)

    # 4. Strict Security Headers with permissive media & style policies for Tailwind & Fonts
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "SAMEORIGIN"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Permissions-Policy"] = "camera=(), microphone=(), geolocation=()"
    response.headers["Content-Security-Policy"] = (
        "default-src * 'unsafe-inline' 'unsafe-eval' data: blob:; "
        "script-src * 'unsafe-inline' 'unsafe-eval' data: blob:; "
        "style-src * 'unsafe-inline' https: http:; "
        "font-src * data: https: http:; "
        "img-src * data: blob: https: http:; "
        "connect-src *;"
    )

    return response

# Mount Static and Templates
STATIC_DIR = BASE_DIR / "static"
TEMPLATES_DIR = BASE_DIR / "templates"

STATIC_DIR.mkdir(parents=True, exist_ok=True)
TEMPLATES_DIR.mkdir(parents=True, exist_ok=True)

app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

# Include API Routers
app.include_router(products_router)
app.include_router(cart_router)
app.include_router(wishlist_router)
app.include_router(orders_router)
app.include_router(coupons_router)
app.include_router(concierge_router)
app.include_router(admin_router)

# Frontend Web Page Routes
@app.get("/", response_class=HTMLResponse)
def page_home(request: Request):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM products ORDER BY is_featured DESC, rating DESC LIMIT 8")
        products = [format_product_row(r) for r in cursor.fetchall()]
        
    return templates.TemplateResponse(
        request=request,
        name="home.html",
        context={
            "products": products,
            "active_page": "home"
        }
    )

@app.get("/shop", response_class=HTMLResponse)
def page_shop(request: Request, category: str = "all", sort: str = "featured"):
    with get_db() as conn:
        cursor = conn.cursor()
        query = "SELECT * FROM products WHERE 1=1"
        params = []

        if category and category.lower() != "all":
            query += " AND (category_slug = ? OR LOWER(category) LIKE ?)"
            params.extend([category.lower(), f"%{category.lower()}%"])

        if sort == "price-asc":
            query += " ORDER BY price ASC"
        elif sort == "price-desc":
            query += " ORDER BY price DESC"
        elif sort == "bestseller":
            query += " ORDER BY is_bestseller DESC, rating DESC"
        elif sort == "newest":
            query += " ORDER BY is_new DESC, id DESC"
        else:
            query += " ORDER BY is_featured DESC, rating DESC, id ASC"

        cursor.execute(query, params)
        products = [format_product_row(r) for r in cursor.fetchall()]

    return templates.TemplateResponse(
        request=request,
        name="shop.html",
        context={
            "products": products,
            "current_category": category,
            "current_sort": sort,
            "active_page": "shop"
        }
    )

@app.get("/product/{id_or_slug}", response_class=HTMLResponse)
def page_product(request: Request, id_or_slug: str):
    with get_db() as conn:
        cursor = conn.cursor()
        if id_or_slug.isdigit():
            cursor.execute("SELECT * FROM products WHERE id = ?", (int(id_or_slug),))
        else:
            cursor.execute("SELECT * FROM products WHERE slug = ?", (id_or_slug,))
        row = cursor.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Product not found")
        product = format_product_row(row, include_reviews=True)

    return templates.TemplateResponse(
        request=request,
        name="product.html",
        context={
            "product": product,
            "active_page": "shop"
        }
    )

@app.get("/cart", response_class=HTMLResponse)
def page_cart(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="cart.html",
        context={
            "active_page": "cart"
        }
    )

@app.get("/checkout", response_class=HTMLResponse)
def page_checkout(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="checkout.html",
        context={
            "active_page": "checkout"
        }
    )

@app.get("/order-success/{order_number}", response_class=HTMLResponse)
def page_order_success(request: Request, order_number: str):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM orders WHERE order_number = ?", (order_number,))
        order_row = cursor.fetchone()
        if not order_row:
            raise HTTPException(status_code=404, detail="Order not found")
        
        order = dict(order_row)
        cursor.execute("SELECT * FROM order_items WHERE order_id = ?", (order["id"],))
        order["items"] = [dict(i) for i in cursor.fetchall()]

    return templates.TemplateResponse(
        request=request,
        name="order_success.html",
        context={
            "order": order,
            "active_page": "checkout"
        }
    )

@app.get("/wishlist", response_class=HTMLResponse)
def page_wishlist(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="wishlist.html",
        context={
            "active_page": "wishlist"
        }
    )

@app.get("/admin", response_class=HTMLResponse)
def page_admin(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="admin.html",
        context={
            "active_page": "admin"
        }
    )

# Service Worker must be served from root path for maximum scope
@app.get("/sw.js")
def service_worker():
    return FileResponse(str(STATIC_DIR / "sw.js"), media_type="application/javascript")

# Digital Asset Links for Android App / Play Store TWA
@app.get("/.well-known/assetlinks.json")
def assetlinks():
    assetlinks_file = STATIC_DIR / "assetlinks.json"
    if assetlinks_file.exists():
        return FileResponse(str(assetlinks_file), media_type="application/json")
    return JSONResponse(status_code=200, content=[])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="127.0.0.1", port=8000, reload=True)
