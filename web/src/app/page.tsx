'use client'

import { useState } from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { 
  useGetProductsQuery, 
  useGetProductCategoriesQuery,
  useCreateProductMutation, 
  useUpdateProductMutation, 
  useDeleteProductMutation,
  useCreateProductCategoryMutation,
  useDeleteProductCategoryMutation 
} from "@/store/api/enhanced/products";
import { productSchema, categorySchema, type ProductFormData, type CategoryFormData } from "@/lib/validations";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Badge } from "@/components/ui/badge";
import { Trash2, Plus, Edit, Package, Tag } from "lucide-react";
import { Dialog, DialogContent, DialogDescription, DialogFooter, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog";
import {
  Form,
  FormControl,
  FormDescription,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form";

export default function InventoryDashboard() {
    const { data: products, isLoading: productsLoading } = useGetProductsQuery({});
    const { data: categories, isLoading: categoriesLoading } = useGetProductCategoriesQuery();
    const [createProduct] = useCreateProductMutation();
    const [updateProduct] = useUpdateProductMutation();
    const [deleteProduct] = useDeleteProductMutation();
    const [createCategory] = useCreateProductCategoryMutation();
    const [deleteCategory] = useDeleteProductCategoryMutation();
    
    const [selectedCategory, setSelectedCategory] = useState<number | null>(null);
    const [editingProduct, setEditingProduct] = useState<any>(null);
    const [productDialogOpen, setProductDialogOpen] = useState(false);
    const [categoryDialogOpen, setCategoryDialogOpen] = useState(false);
    
    const productForm = useForm<ProductFormData>({
        resolver: zodResolver(productSchema),
        defaultValues: {
            sku: "",
            name: "",
            description: "",
            category_id: undefined,
            stock: 0,
            price: 0
        }
    });

    const categoryForm = useForm<CategoryFormData>({
        resolver: zodResolver(categorySchema),
        defaultValues: {
            name: "",
            description: ""
        }
    });

    const filteredProducts = products?.filter(p => 
        selectedCategory === null || p.category_id === selectedCategory
    );

    const handleCreateProduct = async (data: ProductFormData) => {
        try {
            await createProduct({ 
                createProductCommand: {
                    ...data,
                    description: data.description || null,
                    category_id: data.category_id || null,
                } 
            }).unwrap();
            productForm.reset();
            setProductDialogOpen(false);
        } catch (error) {
            console.error("Failed to create product:", error);
        }
    };

    const handleUpdateProduct = async (data: ProductFormData) => {
        if (editingProduct) {
            try {
                await updateProduct({ 
                    id: editingProduct.id,
                    updateProductCommand: {
                        ...data,
                        description: data.description || null,
                        category_id: data.category_id || null,
                    }
                }).unwrap();
                setEditingProduct(null);
                productForm.reset();
                setProductDialogOpen(false);
            } catch (error) {
                console.error("Failed to update product:", error);
            }
        }
    };

    const handleCreateCategory = async (data: CategoryFormData) => {
        try {
            await createCategory({ 
                createProductCategoryCommand: {
                    ...data,
                    description: data.description || null
                } 
            }).unwrap();
            categoryForm.reset();
            setCategoryDialogOpen(false);
        } catch (error) {
            console.error("Failed to create category:", error);
        }
    };

    const openProductDialog = (product?: any) => {
        if (product) {
            setEditingProduct(product);
            productForm.reset({
                sku: product.sku,
                name: product.name,
                description: product.description || "",
                category_id: product.category_id || undefined,
                stock: product.stock || 0,
                price: parseFloat(product.price)
            });
        } else {
            setEditingProduct(null);
            productForm.reset();
        }
        setProductDialogOpen(true);
    };

    const openCategoryDialog = () => {
        categoryForm.reset();
        setCategoryDialogOpen(true);
    };

    if (productsLoading || categoriesLoading) {
        return <div className="flex items-center justify-center min-h-screen">Loading inventory...</div>;
    }

    const totalStock = products?.reduce((sum, p) => sum + (p.stock || 0), 0) || 0;
    const totalValue = products?.reduce((sum, p) => sum + ((p.stock || 0) * parseFloat(p.price)), 0) || 0;
    const lowStockItems = products?.filter(p => (p.stock || 0) < 10).length || 0;

    return (
        <div className="container mx-auto p-6">
            <div className="mb-8">
                <h1 className="text-3xl font-bold mb-2">Product Inventory Management</h1>
                <p className="text-muted-foreground">Manage your products, categories, and stock levels</p>
            </div>

            <div className="grid gap-4 md:grid-cols-4 mb-6">
                <Card>
                    <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                        <CardTitle className="text-sm font-medium">Total Products</CardTitle>
                        <Package className="h-4 w-4 text-muted-foreground" />
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold">{products?.length || 0}</div>
                    </CardContent>
                </Card>
                <Card>
                    <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                        <CardTitle className="text-sm font-medium">Total Stock</CardTitle>
                        <Package className="h-4 w-4 text-muted-foreground" />
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold">{totalStock}</div>
                    </CardContent>
                </Card>
                <Card>
                    <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                        <CardTitle className="text-sm font-medium">Total Value</CardTitle>
                        <Package className="h-4 w-4 text-muted-foreground" />
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold">${totalValue.toFixed(2)}</div>
                    </CardContent>
                </Card>
                <Card>
                    <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                        <CardTitle className="text-sm font-medium">Low Stock Alert</CardTitle>
                        <Package className="h-4 w-4 text-muted-foreground" />
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold text-red-600">{lowStockItems}</div>
                        <p className="text-xs text-muted-foreground">Items below 10 units</p>
                    </CardContent>
                </Card>
            </div>

            <Tabs defaultValue="products" className="space-y-4">
                <TabsList>
                    <TabsTrigger value="products">Products</TabsTrigger>
                    <TabsTrigger value="categories">Categories</TabsTrigger>
                </TabsList>

                <TabsContent value="products" className="space-y-4">
                    <div className="flex justify-between items-center">
                        <div className="flex gap-2">
                            <Select value={selectedCategory?.toString() || "all"} onValueChange={(value) => setSelectedCategory(value === "all" ? null : parseInt(value))}>
                                <SelectTrigger className="w-[200px]">
                                    <SelectValue placeholder="Filter by category" />
                                </SelectTrigger>
                                <SelectContent>
                                    <SelectItem value="all">All Categories</SelectItem>
                                    {categories?.map((cat) => (
                                        <SelectItem key={cat.id} value={cat.id.toString()}>{cat.name}</SelectItem>
                                    ))}
                                </SelectContent>
                            </Select>
                        </div>
                        <Dialog open={productDialogOpen} onOpenChange={(open) => {
                            setProductDialogOpen(open);
                            if (!open) {
                                productForm.reset();
                                setEditingProduct(null);
                            }
                        }}>
                            <DialogTrigger asChild>
                                <Button onClick={() => openProductDialog()}>
                                    <Plus className="mr-2 h-4 w-4" /> Add Product
                                </Button>
                            </DialogTrigger>
                            <DialogContent className="sm:max-w-[525px]">
                                <DialogHeader>
                                    <DialogTitle>{editingProduct ? 'Edit Product' : 'Add New Product'}</DialogTitle>
                                    <DialogDescription>
                                        {editingProduct ? 'Update product details' : 'Add a new product to your inventory'}
                                    </DialogDescription>
                                </DialogHeader>
                                <Form {...productForm}>
                                    <form onSubmit={productForm.handleSubmit(editingProduct ? handleUpdateProduct : handleCreateProduct)} className="space-y-4">
                                        <FormField
                                            control={productForm.control}
                                            name="sku"
                                            render={({ field }) => (
                                                <FormItem>
                                                    <FormLabel>SKU</FormLabel>
                                                    <FormControl>
                                                        <Input placeholder="PROD-001" {...field} />
                                                    </FormControl>
                                                    <FormDescription>
                                                        Unique stock keeping unit identifier
                                                    </FormDescription>
                                                    <FormMessage />
                                                </FormItem>
                                            )}
                                        />
                                        <FormField
                                            control={productForm.control}
                                            name="name"
                                            render={({ field }) => (
                                                <FormItem>
                                                    <FormLabel>Product Name</FormLabel>
                                                    <FormControl>
                                                        <Input placeholder="Enter product name" {...field} />
                                                    </FormControl>
                                                    <FormMessage />
                                                </FormItem>
                                            )}
                                        />
                                        <FormField
                                            control={productForm.control}
                                            name="description"
                                            render={({ field }) => (
                                                <FormItem>
                                                    <FormLabel>Description</FormLabel>
                                                    <FormControl>
                                                        <Input placeholder="Product description (optional)" {...field} value={field.value || ""} />
                                                    </FormControl>
                                                    <FormMessage />
                                                </FormItem>
                                            )}
                                        />
                                        <FormField
                                            control={productForm.control}
                                            name="category_id"
                                            render={({ field }) => (
                                                <FormItem>
                                                    <FormLabel>Category</FormLabel>
                                                    <Select 
                                                        onValueChange={(value) => field.onChange(value ? parseInt(value) : undefined)}
                                                        value={field.value?.toString() || ""}
                                                    >
                                                        <FormControl>
                                                            <SelectTrigger>
                                                                <SelectValue placeholder="Select a category" />
                                                            </SelectTrigger>
                                                        </FormControl>
                                                        <SelectContent>
                                                            {categories?.map((cat) => (
                                                                <SelectItem key={cat.id} value={cat.id.toString()}>
                                                                    {cat.name}
                                                                </SelectItem>
                                                            ))}
                                                        </SelectContent>
                                                    </Select>
                                                    <FormMessage />
                                                </FormItem>
                                            )}
                                        />
                                        <div className="grid grid-cols-2 gap-4">
                                            <FormField
                                                control={productForm.control}
                                                name="stock"
                                                render={({ field }) => (
                                                    <FormItem>
                                                        <FormLabel>Stock Quantity</FormLabel>
                                                        <FormControl>
                                                            <Input 
                                                                type="number" 
                                                                placeholder="0" 
                                                                {...field} 
                                                                onChange={(e) => field.onChange(parseInt(e.target.value) || 0)}
                                                            />
                                                        </FormControl>
                                                        <FormMessage />
                                                    </FormItem>
                                                )}
                                            />
                                            <FormField
                                                control={productForm.control}
                                                name="price"
                                                render={({ field }) => (
                                                    <FormItem>
                                                        <FormLabel>Price</FormLabel>
                                                        <FormControl>
                                                            <Input 
                                                                type="number" 
                                                                step="0.01"
                                                                placeholder="0.00" 
                                                                {...field}
                                                                onChange={(e) => field.onChange(e.target.value)}
                                                            />
                                                        </FormControl>
                                                        <FormMessage />
                                                    </FormItem>
                                                )}
                                            />
                                        </div>
                                        <DialogFooter>
                                            <Button type="submit">
                                                {editingProduct ? 'Update' : 'Create'} Product
                                            </Button>
                                        </DialogFooter>
                                    </form>
                                </Form>
                            </DialogContent>
                        </Dialog>
                    </div>

                    <Card>
                        <CardContent className="p-0">
                            <Table>
                                <TableHeader>
                                    <TableRow>
                                        <TableHead>SKU</TableHead>
                                        <TableHead>Product Name</TableHead>
                                        <TableHead>Category</TableHead>
                                        <TableHead>Stock</TableHead>
                                        <TableHead>Price</TableHead>
                                        <TableHead>Total Value</TableHead>
                                        <TableHead className="text-right">Actions</TableHead>
                                    </TableRow>
                                </TableHeader>
                                <TableBody>
                                    {filteredProducts?.map((product) => (
                                        <TableRow key={product.id}>
                                            <TableCell className="font-medium">{product.sku}</TableCell>
                                            <TableCell>
                                                <div>
                                                    <div className="font-medium">{product.name}</div>
                                                    {product.description && (
                                                        <div className="text-sm text-muted-foreground">{product.description}</div>
                                                    )}
                                                </div>
                                            </TableCell>
                                            <TableCell>
                                                {product.category ? (
                                                    <Badge variant="secondary">
                                                        <Tag className="mr-1 h-3 w-3" />
                                                        {product.category.name}
                                                    </Badge>
                                                ) : "-"}
                                            </TableCell>
                                            <TableCell>
                                                <Badge variant={(product.stock || 0) < 10 ? "destructive" : "default"}>
                                                    {product.stock || 0}
                                                </Badge>
                                            </TableCell>
                                            <TableCell>${parseFloat(product.price).toFixed(2)}</TableCell>
                                            <TableCell>${((product.stock || 0) * parseFloat(product.price)).toFixed(2)}</TableCell>
                                            <TableCell className="text-right">
                                                <div className="flex gap-2 justify-end">
                                                    <Button 
                                                        variant="ghost" 
                                                        size="sm"
                                                        onClick={() => openProductDialog(product)}>
                                                        <Edit className="h-4 w-4" />
                                                    </Button>
                                                    <Button 
                                                        variant="ghost" 
                                                        size="sm"
                                                        onClick={() => deleteProduct({ id: product.id })}>
                                                        <Trash2 className="h-4 w-4 text-destructive" />
                                                    </Button>
                                                </div>
                                            </TableCell>
                                        </TableRow>
                                    ))}
                                </TableBody>
                            </Table>
                        </CardContent>
                    </Card>
                </TabsContent>

                <TabsContent value="categories" className="space-y-4">
                    <div className="flex justify-end">
                        <Dialog open={categoryDialogOpen} onOpenChange={(open) => {
                            setCategoryDialogOpen(open);
                            if (!open) {
                                categoryForm.reset();
                            }
                        }}>
                            <DialogTrigger asChild>
                                <Button onClick={openCategoryDialog}>
                                    <Plus className="mr-2 h-4 w-4" /> Add Category
                                </Button>
                            </DialogTrigger>
                            <DialogContent>
                                <DialogHeader>
                                    <DialogTitle>Add New Category</DialogTitle>
                                    <DialogDescription>
                                        Create a new product category
                                    </DialogDescription>
                                </DialogHeader>
                                <Form {...categoryForm}>
                                    <form onSubmit={categoryForm.handleSubmit(handleCreateCategory)} className="space-y-4">
                                        <FormField
                                            control={categoryForm.control}
                                            name="name"
                                            render={({ field }) => (
                                                <FormItem>
                                                    <FormLabel>Category Name</FormLabel>
                                                    <FormControl>
                                                        <Input placeholder="Electronics, Clothing, etc." {...field} />
                                                    </FormControl>
                                                    <FormMessage />
                                                </FormItem>
                                            )}
                                        />
                                        <FormField
                                            control={categoryForm.control}
                                            name="description"
                                            render={({ field }) => (
                                                <FormItem>
                                                    <FormLabel>Description</FormLabel>
                                                    <FormControl>
                                                        <Input 
                                                            placeholder="Brief description (optional)" 
                                                            {...field} 
                                                            value={field.value || ""}
                                                        />
                                                    </FormControl>
                                                    <FormMessage />
                                                </FormItem>
                                            )}
                                        />
                                        <DialogFooter>
                                            <Button type="submit">Create Category</Button>
                                        </DialogFooter>
                                    </form>
                                </Form>
                            </DialogContent>
                        </Dialog>
                    </div>

                    <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
                        {categories?.map((category) => {
                            const categoryProducts = products?.filter(p => p.category_id === category.id) || [];
                            return (
                                <Card key={category.id}>
                                    <CardHeader>
                                        <div className="flex justify-between items-start">
                                            <div>
                                                <CardTitle>{category.name}</CardTitle>
                                                {category.description && (
                                                    <CardDescription>{category.description}</CardDescription>
                                                )}
                                            </div>
                                            <Button 
                                                variant="ghost" 
                                                size="sm"
                                                onClick={() => deleteCategory({ id: category.id })}>
                                                <Trash2 className="h-4 w-4 text-destructive" />
                                            </Button>
                                        </div>
                                    </CardHeader>
                                    <CardContent>
                                        <div className="text-sm text-muted-foreground">
                                            {categoryProducts.length} products
                                        </div>
                                    </CardContent>
                                </Card>
                            );
                        })}
                    </div>
                </TabsContent>
            </Tabs>
        </div>
    );
}