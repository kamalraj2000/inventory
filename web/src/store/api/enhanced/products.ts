import { productsApi } from "../generated/products";

export const enhancedProductsApi = productsApi.enhanceEndpoints({
    addTagTypes: [
        'Product',
        'ProductCategory', 
    ],
    endpoints: {
        // Product Category endpoints
        getProductCategories: {
            providesTags: ['ProductCategory'],
        },
        getProductCategory: {
            providesTags: ['ProductCategory'],
        },
        createProductCategory: {
            invalidatesTags: ['ProductCategory'],
        },
        updateProductCategory: {
            invalidatesTags: ['ProductCategory'],
        },
        deleteProductCategory: {
            invalidatesTags: ['ProductCategory', 'Product'], // Also invalidate products since they depend on categories
        },
        // Product endpoints
        getProducts: {
            providesTags: ['Product'],
        },
        getProduct: {
            providesTags: ['Product'],
        },
        createProduct: {
            invalidatesTags: ['Product'],
        },
        updateProduct: {
            invalidatesTags: ['Product'],
        },
        deleteProduct: {
            invalidatesTags: ['Product'],
        },
    }
});

export const {
  // Product Category hooks
  useGetProductCategoriesQuery,
  useGetProductCategoryQuery,
  useCreateProductCategoryMutation,
  useUpdateProductCategoryMutation,
  useDeleteProductCategoryMutation,
  // Product hooks
  useGetProductsQuery,
  useGetProductQuery,
  useCreateProductMutation,
  useUpdateProductMutation,
  useDeleteProductMutation,
} = enhancedProductsApi;