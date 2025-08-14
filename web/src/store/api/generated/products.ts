/* eslint-disable -- Auto Generated File */
import { emptySplitApi as api } from "../empty-api";
const injectedRtkApi = api.injectEndpoints({
  endpoints: (build) => ({
    redirectToSwaggerGet: build.query<
      RedirectToSwaggerGetApiResponse,
      RedirectToSwaggerGetApiArg
    >({
      query: () => ({ url: `/` }),
    }),
    getProductCategories: build.query<
      GetProductCategoriesApiResponse,
      GetProductCategoriesApiArg
    >({
      query: () => ({ url: `/api/ProductCategories` }),
    }),
    createProductCategory: build.mutation<
      CreateProductCategoryApiResponse,
      CreateProductCategoryApiArg
    >({
      query: (queryArg) => ({
        url: `/api/ProductCategories`,
        method: "POST",
        body: queryArg.createProductCategoryCommand,
      }),
    }),
    getProductCategory: build.query<
      GetProductCategoryApiResponse,
      GetProductCategoryApiArg
    >({
      query: (queryArg) => ({ url: `/api/ProductCategories/${queryArg.id}` }),
    }),
    updateProductCategory: build.mutation<
      UpdateProductCategoryApiResponse,
      UpdateProductCategoryApiArg
    >({
      query: (queryArg) => ({
        url: `/api/ProductCategories/${queryArg.id}`,
        method: "PUT",
        body: queryArg.updateProductCategoryCommand,
      }),
    }),
    deleteProductCategory: build.mutation<
      DeleteProductCategoryApiResponse,
      DeleteProductCategoryApiArg
    >({
      query: (queryArg) => ({
        url: `/api/ProductCategories/${queryArg.id}`,
        method: "DELETE",
      }),
    }),
    getProducts: build.query<GetProductsApiResponse, GetProductsApiArg>({
      query: (queryArg) => ({
        url: `/api/Products`,
        params: {
          category_id: queryArg.categoryId,
        },
      }),
    }),
    createProduct: build.mutation<
      CreateProductApiResponse,
      CreateProductApiArg
    >({
      query: (queryArg) => ({
        url: `/api/Products`,
        method: "POST",
        body: queryArg.createProductCommand,
      }),
    }),
    getProduct: build.query<GetProductApiResponse, GetProductApiArg>({
      query: (queryArg) => ({ url: `/api/Products/${queryArg.id}` }),
    }),
    updateProduct: build.mutation<
      UpdateProductApiResponse,
      UpdateProductApiArg
    >({
      query: (queryArg) => ({
        url: `/api/Products/${queryArg.id}`,
        method: "PUT",
        body: queryArg.updateProductCommand,
      }),
    }),
    deleteProduct: build.mutation<
      DeleteProductApiResponse,
      DeleteProductApiArg
    >({
      query: (queryArg) => ({
        url: `/api/Products/${queryArg.id}`,
        method: "DELETE",
      }),
    }),
  }),
  overrideExisting: false,
});
export { injectedRtkApi as productsApi };
export type RedirectToSwaggerGetApiResponse =
  /** status 200 Successful Response */ any;
export type RedirectToSwaggerGetApiArg = void;
export type GetProductCategoriesApiResponse =
  /** status 200 Successful Response */ ProductCategory[];
export type GetProductCategoriesApiArg = void;
export type CreateProductCategoryApiResponse =
  /** status 200 Successful Response */ number;
export type CreateProductCategoryApiArg = {
  createProductCategoryCommand: CreateProductCategoryCommand;
};
export type GetProductCategoryApiResponse =
  /** status 200 Successful Response */ ProductCategory;
export type GetProductCategoryApiArg = {
  id: number;
};
export type UpdateProductCategoryApiResponse =
  /** status 200 Successful Response */ any;
export type UpdateProductCategoryApiArg = {
  id: number;
  updateProductCategoryCommand: UpdateProductCategoryCommand;
};
export type DeleteProductCategoryApiResponse =
  /** status 200 Successful Response */ any;
export type DeleteProductCategoryApiArg = {
  id: number;
};
export type GetProductsApiResponse =
  /** status 200 Successful Response */ Product[];
export type GetProductsApiArg = {
  categoryId?: number | null;
};
export type CreateProductApiResponse =
  /** status 200 Successful Response */ number;
export type CreateProductApiArg = {
  createProductCommand: CreateProductCommand;
};
export type GetProductApiResponse =
  /** status 200 Successful Response */ Product;
export type GetProductApiArg = {
  id: number;
};
export type UpdateProductApiResponse =
  /** status 200 Successful Response */ any;
export type UpdateProductApiArg = {
  id: number;
  updateProductCommand: UpdateProductCommand;
};
export type DeleteProductApiResponse =
  /** status 200 Successful Response */ any;
export type DeleteProductApiArg = {
  id: number;
};
export type ProductCategory = {
  id: number;
  name: string;
  description?: string | null;
};
export type ValidationError = {
  loc: (string | number)[];
  msg: string;
  type: string;
};
export type HttpValidationError = {
  detail?: ValidationError[];
};
export type CreateProductCategoryCommand = {
  name: string;
  description?: string | null;
};
export type UpdateProductCategoryCommand = {
  name: string;
  description?: string | null;
};
export type Product = {
  id: number;
  sku: string;
  name: string;
  description?: string | null;
  category_id?: number | null;
  category?: ProductCategory | null;
  stock?: number;
  price: string;
};
export type CreateProductCommand = {
  sku: string;
  name: string;
  description?: string | null;
  category_id?: number | null;
  stock?: number;
  price: number | string;
};
export type UpdateProductCommand = {
  sku: string;
  name: string;
  description?: string | null;
  category_id?: number | null;
  stock: number;
  price: number | string;
};
export const {
  useRedirectToSwaggerGetQuery,
  useGetProductCategoriesQuery,
  useCreateProductCategoryMutation,
  useGetProductCategoryQuery,
  useUpdateProductCategoryMutation,
  useDeleteProductCategoryMutation,
  useGetProductsQuery,
  useCreateProductMutation,
  useGetProductQuery,
  useUpdateProductMutation,
  useDeleteProductMutation,
} = injectedRtkApi;
