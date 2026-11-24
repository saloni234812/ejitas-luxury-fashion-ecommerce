// Ejitas Luxury Fashion E-Commerce Client Engine

const Ejitas = {
  // Session handling
  getSessionId() {
    let sid = localStorage.getItem('ejitas_session_id');
    if (!sid) {
      sid = 'ejt_' + Math.random().toString(36).substring(2, 12) + '_' + Date.now();
      localStorage.setItem('ejitas_session_id', sid);
    }
    return sid;
  },

  // Toast Notification
  toast(message, type = 'info') {
    let container = document.getElementById('ejitas-toast-container');
    if (!container) {
      container = document.createElement('div');
      container.id = 'ejitas-toast-container';
      container.className = 'fixed bottom-20 left-1/2 -translate-x-1/2 z-[9999] flex flex-col gap-2 pointer-events-none w-11/12 max-w-sm';
      document.body.appendChild(container);
    }

    const toast = document.createElement('div');
    toast.className = 'pointer-events-auto bg-inverse-surface text-inverse-on-surface px-4 py-3 rounded-full shadow-xl flex items-center justify-between text-body-sm animate-fade-in transition-all duration-300';
    toast.innerHTML = `
      <div class="flex items-center gap-2 truncate">
        <span class="material-symbols-outlined text-[18px] text-tertiary-fixed">
          ${type === 'success' ? 'check_circle' : type === 'wishlist' ? 'favorite' : 'info'}
        </span>
        <span class="font-medium truncate">${message}</span>
      </div>
      <button onclick="this.parentElement.remove()" class="text-inverse-on-surface/70 hover:text-inverse-on-surface ml-2">
        <span class="material-symbols-outlined text-[16px]">close</span>
      </button>
    `;

    container.appendChild(toast);
    setTimeout(() => {
      toast.style.opacity = '0';
      toast.style.transform = 'translateY(10px)';
      setTimeout(() => toast.remove(), 300);
    }, 3500);
  },

  // Refresh cart state across entire site
  async syncCart() {
    try {
      const res = await fetch(`/api/cart?session_id=${this.getSessionId()}`);
      if (!res.ok) return;
      const data = await res.json();
      
      // Update badge counts
      document.querySelectorAll('.ejitas-cart-badge').forEach(badge => {
        badge.innerText = data.items_count;
        if (data.items_count > 0) {
          badge.classList.remove('hidden');
          badge.style.display = 'flex';
        } else {
          badge.classList.add('hidden');
          badge.style.display = 'none';
        }
      });

      // Update cart drawer if it exists
      this.renderCartDrawer(data);
    } catch (e) {
      console.warn('Cart sync failed:', e);
    }
  },

  // Add item to bag
  async addToBag(productId, color = null, quantity = 1, openDrawer = true) {
    try {
      const res = await fetch('/api/cart/items', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          product_id: parseInt(productId),
          color: color,
          quantity: parseInt(quantity),
          session_id: this.getSessionId()
        })
      });
      const data = await res.json();
      this.syncCart();
      this.toast('Added to your Shopping Bag', 'success');
      if (openDrawer) {
        this.openCartDrawer();
      }
    } catch (e) {
      console.error(e);
      this.toast('Could not add to bag', 'info');
    }
  },

  // Update item quantity
  async updateQuantity(itemId, qty) {
    try {
      await fetch(`/api/cart/items/${itemId}?session_id=${this.getSessionId()}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ quantity: qty })
      });
      this.syncCart();
      // If on cart page, trigger full page reload/refresh
      if (window.refreshCartPage) {
        window.refreshCartPage();
      }
    } catch (e) {
      console.error(e);
    }
  },

  // Remove item
  async removeItem(itemId) {
    try {
      await fetch(`/api/cart/items/${itemId}?session_id=${this.getSessionId()}`, {
        method: 'DELETE'
      });
      this.syncCart();
      this.toast('Item removed from Bag', 'info');
      if (window.refreshCartPage) {
        window.refreshCartPage();
      }
    } catch (e) {
      console.error(e);
    }
  },

  // Toggle wishlist
  async toggleWishlist(productId, btnElement = null) {
    try {
      const res = await fetch('/api/wishlist/toggle', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          product_id: parseInt(productId),
          session_id: this.getSessionId()
        })
      });
      const data = await res.json();
      
      if (btnElement) {
        const icon = btnElement.querySelector('.material-symbols-outlined') || btnElement;
        if (data.is_wishlisted) {
          icon.style.fontVariationSettings = "'FILL' 1";
          icon.classList.add('text-secondary');
        } else {
          icon.style.fontVariationSettings = "'FILL' 0";
          icon.classList.remove('text-secondary');
        }
      }

      this.toast(data.is_wishlisted ? 'Saved to Wishlist' : 'Removed from Wishlist', 'wishlist');
    } catch (e) {
      console.error(e);
    }
  },

  // Drawer Controls
  openCartDrawer() {
    const drawer = document.getElementById('cart-drawer');
    if (drawer) {
      drawer.classList.remove('translate-x-full', 'pointer-events-none');
    }
  },

  closeCartDrawer() {
    const drawer = document.getElementById('cart-drawer');
    if (drawer) {
      drawer.classList.add('translate-x-full', 'pointer-events-none');
    }
  },

  openMobileMenu() {
    const menu = document.getElementById('mobile-drawer');
    if (menu) {
      menu.classList.remove('-translate-x-full', 'pointer-events-none');
    }
  },

  closeMobileMenu() {
    const menu = document.getElementById('mobile-drawer');
    if (menu) {
      menu.classList.add('-translate-x-full', 'pointer-events-none');
    }
  },

  // Render Cart Drawer dynamically
  renderCartDrawer(cartData) {
    const listContainer = document.getElementById('drawer-cart-items');
    const emptyContainer = document.getElementById('drawer-cart-empty');
    const totalEl = document.getElementById('drawer-cart-total');
    const countEl = document.getElementById('drawer-cart-count');
    const footerEl = document.getElementById('drawer-cart-footer');

    if (!listContainer) return;

    if (countEl) countEl.innerText = `${cartData.items_count} Item${cartData.items_count === 1 ? '' : 's'}`;
    if (totalEl) totalEl.innerText = `₹${cartData.subtotal.toLocaleString('en-IN')}`;

    if (!cartData.items || cartData.items.length === 0) {
      if (listContainer) listContainer.classList.add('hidden');
      if (emptyContainer) emptyContainer.classList.remove('hidden');
      if (footerEl) footerEl.classList.add('hidden');
    } else {
      if (listContainer) listContainer.classList.remove('hidden');
      if (emptyContainer) emptyContainer.classList.add('hidden');
      if (footerEl) footerEl.classList.remove('hidden');

      listContainer.innerHTML = cartData.items.map(item => `
        <div class="flex gap-3 py-3 border-b border-surface-variant/40 items-center">
          <img src="${item.image}" alt="${item.name}" class="w-14 h-16 object-cover rounded-lg bg-surface-container flex-shrink-0" />
          <div class="flex-1 min-w-0">
            <h4 class="font-title-md text-[13px] text-on-surface truncate font-semibold">${item.name}</h4>
            <p class="font-body-sm text-[11px] text-on-surface-variant truncate">${item.color || 'Standard Atelier'}</p>
            <div class="flex items-center justify-between mt-1">
              <span class="font-currency-price text-[13px] text-primary font-bold">₹${item.price.toLocaleString('en-IN')}</span>
              <div class="flex items-center gap-1.5 bg-surface-container rounded-full px-1.5 py-0.5">
                <button onclick="Ejitas.updateQuantity(${item.id}, ${item.quantity - 1})" class="w-5 h-5 flex items-center justify-center text-on-surface-variant hover:text-on-surface">
                  <span class="material-symbols-outlined text-[14px]">remove</span>
                </button>
                <span class="font-title-md text-[11px] text-on-surface font-semibold px-1">${item.quantity}</span>
                <button onclick="Ejitas.updateQuantity(${item.id}, ${item.quantity + 1})" class="w-5 h-5 flex items-center justify-center text-on-surface-variant hover:text-on-surface">
                  <span class="material-symbols-outlined text-[14px]">add</span>
                </button>
              </div>
            </div>
          </div>
          <button onclick="Ejitas.removeItem(${item.id})" class="text-on-surface-variant hover:text-error p-1">
            <span class="material-symbols-outlined text-[16px]">delete_outline</span>
          </button>
        </div>
      `).join('');
    }
  }
};

// Global initialization on DOMContentLoaded
document.addEventListener('DOMContentLoaded', () => {
  Ejitas.syncCart();

  // Register Service Worker with auto-update
  if ('serviceWorker' in navigator) {
    navigator.serviceWorker.register('/sw.js?v=4', { scope: '/' })
      .then((reg) => {
        reg.update();
      })
      .catch((err) => console.warn('SW registration failed:', err));
  }
});
