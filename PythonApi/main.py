from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response, RedirectResponse
from typing import List, Optional
from models import (
    Product, CreateProductCommand, UpdateProductCommand,
    ProductCategory, CreateProductCategoryCommand, UpdateProductCategoryCommand
)
from database import db

app = FastAPI(title="Product Inventory API", version="v1", docs_url="/swagger", redoc_url="/redoc")
app.title = "Product Inventory API"
app.version = "v1"
app.description = "API for managing product inventory with categories"

# Configure CORS to allow all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Send interactive user to swagger page by default
@app.get("/")
async def redirect_to_swagger():
    return RedirectResponse(url="/swagger")


# Product Category Endpoints
@app.get("/api/ProductCategories", response_model=List[ProductCategory], tags=["Product Categories"], operation_id="GetProductCategories")
async def get_product_categories():
    return db.get_all_categories()


@app.get("/api/ProductCategories/{id}", response_model=ProductCategory, tags=["Product Categories"], operation_id="GetProductCategory")
async def get_product_category(id: int):
    category = db.get_category_by_id(id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category


@app.post("/api/ProductCategories", response_model=int, tags=["Product Categories"], operation_id="CreateProductCategory")
async def create_product_category(command: CreateProductCategoryCommand):
    category_id = db.create_category(command.name, command.description)
    return category_id


@app.put("/api/ProductCategories/{id}", tags=["Product Categories"], operation_id="UpdateProductCategory")
async def update_product_category(id: int, command: UpdateProductCategoryCommand):
    success = db.update_category(id, command.name, command.description)
    if not success:
        raise HTTPException(status_code=404, detail="Category not found")
    return Response(status_code=200)


@app.delete("/api/ProductCategories/{id}", tags=["Product Categories"], operation_id="DeleteProductCategory")
async def delete_product_category(id: int):
    success = db.delete_category(id)
    if not success:
        raise HTTPException(status_code=400, detail="Cannot delete category - either it doesn't exist or has products assigned")
    return Response(status_code=200)


# Product Endpoints
@app.get("/api/Products", response_model=List[Product], tags=["Products"], operation_id="GetProducts")
async def get_products(category_id: Optional[int] = None):
    if category_id:
        return db.get_products_by_category(category_id)
    return db.get_all_products()


@app.get("/api/Products/{id}", response_model=Product, tags=["Products"], operation_id="GetProduct")
async def get_product(id: int):
    product = db.get_product_by_id(id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@app.post("/api/Products", response_model=int, tags=["Products"], operation_id="CreateProduct")
async def create_product(command: CreateProductCommand):
    product_id = db.create_product(
        command.sku,
        command.name,
        command.price,
        command.stock,
        command.description,
        command.category_id
    )
    if product_id == -1:
        raise HTTPException(status_code=400, detail="SKU already exists")
    return product_id


@app.put("/api/Products/{id}", tags=["Products"], operation_id="UpdateProduct")
async def update_product(id: int, command: UpdateProductCommand):
    success = db.update_product(
        id,
        command.sku,
        command.name,
        command.price,
        command.stock,
        command.description,
        command.category_id
    )
    if not success:
        raise HTTPException(status_code=400, detail="Product not found or SKU conflict")
    return Response(status_code=200)


@app.delete("/api/Products/{id}", tags=["Products"], operation_id="DeleteProduct")
async def delete_product(id: int):
    success = db.delete_product(id)
    if not success:
        raise HTTPException(status_code=404, detail="Product not found")
    return Response(status_code=200)
