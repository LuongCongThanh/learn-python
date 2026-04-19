import { create } from "zustand";
import { subscribeWithSelector, persist } from "zustand/middleware";

export interface CartItem {
  variantId: string;
  productId: string;
  name:      string;
  image:     string;
  price:     number;
  quantity:  number;
}

interface CartState {
  items:     CartItem[];
  total:     number;
  itemCount: number;
}

interface CartActions {
  addToCart:      (item: CartItem) => void;
  removeCartItem: (variantId: string) => void;
  updateQuantity: (variantId: string, quantity: number) => void;
  clearCart:      () => void;
}

function calcTotal(items: CartItem[])     { return items.reduce((s, i) => s + i.price * i.quantity, 0); }
function calcItemCount(items: CartItem[]) { return items.reduce((s, i) => s + i.quantity, 0); }

export const useCartStore = create<CartState & CartActions>()(
  subscribeWithSelector(
    persist(
      (set, get) => ({
        items:     [],
        total:     0,
        itemCount: 0,

        addToCart: (item) => {
          const items    = get().items;
          const existing = items.find((i) => i.variantId === item.variantId);
          const updated  = existing
            ? items.map((i) =>
                i.variantId === item.variantId
                  ? { ...i, quantity: i.quantity + item.quantity }
                  : i,
              )
            : [...items, item];
          set({ items: updated, total: calcTotal(updated), itemCount: calcItemCount(updated) });
        },

        removeCartItem: (variantId) => {
          const updated = get().items.filter((i) => i.variantId !== variantId);
          set({ items: updated, total: calcTotal(updated), itemCount: calcItemCount(updated) });
        },

        updateQuantity: (variantId, quantity) => {
          const updated = get().items.map((i) =>
            i.variantId === variantId ? { ...i, quantity } : i,
          );
          set({ items: updated, total: calcTotal(updated), itemCount: calcItemCount(updated) });
        },

        clearCart: () => set({ items: [], total: 0, itemCount: 0 }),
      }),
      { name: "cart-storage" },
    ),
  ),
);
