import { z } from "zod";

export const ProductSchema = z.object({
  id:          z.number(),
  name:        z.string(),
  slug:        z.string(),
  description: z.string(),
  price:       z.number(),
  salePrice:   z.number().nullable(),
  stock:       z.number().int().nonnegative(),
  images:      z.array(z.string()),
  category:    z.object({ id: z.number(), name: z.string(), slug: z.string() }),
  rating:      z.number().min(0).max(5),
  reviewCount: z.number().int(),
  isActive:    z.boolean(),
  createdAt:   z.string().datetime(),
  updatedAt:   z.string().datetime(),
});

export const ProductListSchema = z.object({
  results:  z.array(ProductSchema),
  count:    z.number(),
  next:     z.string().nullable(),
  previous: z.string().nullable(),
});

export type Product     = z.infer<typeof ProductSchema>;
export type ProductList = z.infer<typeof ProductListSchema>;

export interface ProductFilters {
  search?:   string;
  category?: string;
  minPrice?: number;
  maxPrice?: number;
  ordering?: "price" | "-price" | "-created_at" | "rating";
  page?:     number;
  pageSize?: number;
}
