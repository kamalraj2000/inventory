import { z } from "zod";

export const productSchema = z.object({
  sku: z.string()
    .min(1, "SKU is required")
    .max(50, "SKU must be less than 50 characters")
    .regex(/^[A-Z0-9-]+$/i, "SKU must contain only letters, numbers, and hyphens"),
  name: z.string()
    .min(1, "Product name is required")
    .max(100, "Product name must be less than 100 characters"),
  description: z.string()
    .max(500, "Description must be less than 500 characters")
    .optional()
    .nullable(),
  category_id: z.number()
    .positive("Please select a category")
    .optional()
    .nullable(),
  stock: z.number()
    .int("Stock must be a whole number")
    .min(0, "Stock cannot be negative"),
  price: z.union([
    z.string().regex(/^\d+(\.\d{1,2})?$/, "Price must be a valid number with up to 2 decimal places"),
    z.number().positive("Price must be greater than 0")
  ]).transform((val) => {
    if (typeof val === 'string') {
      return parseFloat(val);
    }
    return val;
  })
});

export const categorySchema = z.object({
  name: z.string()
    .min(1, "Category name is required")
    .max(50, "Category name must be less than 50 characters"),
  description: z.string()
    .max(200, "Description must be less than 200 characters")
    .optional()
    .nullable()
});

export type ProductFormData = z.infer<typeof productSchema>;
export type CategoryFormData = z.infer<typeof categorySchema>;