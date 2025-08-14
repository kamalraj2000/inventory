import pytest
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from fastapi.testclient import TestClient
from main import app
from database import db


@pytest.fixture(autouse=True)
def reset_database():
    """Reset the database before each test"""
    # Clear existing data
    db._products.clear()
    db._product_categories.clear()
    db._next_product_id = 1
    db._next_category_id = 1
    yield
    # Clean up after test
    db._products.clear()
    db._product_categories.clear()
    db._next_product_id = 1
    db._next_category_id = 1
    # Re-initialize sample data for next test
    db._initialize_sample_data()


class TestProductCategoryAPI:
    """Integration tests for the Product Category API endpoints"""
    
    def setup_method(self):
        """Create a test client for each test"""
        self.client = TestClient(app)
    
    def test_get_empty_categories(self):
        """Test getting categories when database is empty"""
        response = self.client.get("/api/ProductCategories")
        assert response.status_code == 200
        assert response.json() == []
    
    def test_create_category(self):
        """Test creating a new category"""
        response = self.client.post(
            "/api/ProductCategories",
            json={"name": "Test Category", "description": "Test Description"}
        )
        assert response.status_code == 200
        assert response.json() == 1
        
        # Verify it was created
        response = self.client.get("/api/ProductCategories")
        assert response.status_code == 200
        categories = response.json()
        assert len(categories) == 1
        assert categories[0]["id"] == 1
        assert categories[0]["name"] == "Test Category"
        assert categories[0]["description"] == "Test Description"
    
    def test_get_category_by_id(self):
        """Test getting a specific category by ID"""
        # Create a category
        create_response = self.client.post(
            "/api/ProductCategories",
            json={"name": "Electronics", "description": "Electronic devices"}
        )
        category_id = create_response.json()
        
        # Get the category
        response = self.client.get(f"/api/ProductCategories/{category_id}")
        assert response.status_code == 200
        category = response.json()
        assert category["id"] == category_id
        assert category["name"] == "Electronics"
        assert category["description"] == "Electronic devices"
    
    def test_get_nonexistent_category(self):
        """Test getting a category that doesn't exist"""
        response = self.client.get("/api/ProductCategories/999")
        assert response.status_code == 404
        assert response.json()["detail"] == "Category not found"
    
    def test_update_category(self):
        """Test updating an existing category"""
        # Create a category
        create_response = self.client.post(
            "/api/ProductCategories",
            json={"name": "Original", "description": "Original Description"}
        )
        category_id = create_response.json()
        
        # Update it
        update_response = self.client.put(
            f"/api/ProductCategories/{category_id}",
            json={"name": "Updated", "description": "Updated Description"}
        )
        assert update_response.status_code == 200
        
        # Verify the update
        response = self.client.get(f"/api/ProductCategories/{category_id}")
        category = response.json()
        assert category["name"] == "Updated"
        assert category["description"] == "Updated Description"
    
    def test_update_nonexistent_category(self):
        """Test updating a category that doesn't exist"""
        response = self.client.put(
            "/api/ProductCategories/999",
            json={"name": "Updated", "description": "Updated Description"}
        )
        assert response.status_code == 404
        assert response.json()["detail"] == "Category not found"
    
    def test_delete_category(self):
        """Test deleting an existing category"""
        # Create two categories
        response1 = self.client.post("/api/ProductCategories", json={"name": "Category 1"})
        id1 = response1.json()
        response2 = self.client.post("/api/ProductCategories", json={"name": "Category 2"})
        id2 = response2.json()
        
        # Delete the first one
        delete_response = self.client.delete(f"/api/ProductCategories/{id1}")
        assert delete_response.status_code == 200
        
        # Verify only second remains
        response = self.client.get("/api/ProductCategories")
        categories = response.json()
        assert len(categories) == 1
        assert categories[0]["id"] == id2
        assert categories[0]["name"] == "Category 2"
    
    def test_delete_category_with_products(self):
        """Test that category with products cannot be deleted"""
        # Create a category
        cat_response = self.client.post(
            "/api/ProductCategories",
            json={"name": "Category with Products"}
        )
        category_id = cat_response.json()
        
        # Create a product in that category
        self.client.post(
            "/api/Products",
            json={
                "sku": "PROD001",
                "name": "Product 1",
                "price": 99.99,
                "stock": 10,
                "category_id": category_id
            }
        )
        
        # Try to delete the category
        delete_response = self.client.delete(f"/api/ProductCategories/{category_id}")
        assert delete_response.status_code == 400
        assert "Cannot delete category" in delete_response.json()["detail"]


class TestProductAPI:
    """Integration tests for the Product API endpoints"""
    
    def setup_method(self):
        """Create a test client for each test"""
        self.client = TestClient(app)
    
    def test_get_empty_products(self):
        """Test getting products when database is empty"""
        response = self.client.get("/api/Products")
        assert response.status_code == 200
        assert response.json() == []
    
    def test_create_product(self):
        """Test creating a new product"""
        response = self.client.post(
            "/api/Products",
            json={
                "sku": "TEST001",
                "name": "Test Product",
                "description": "Test Description",
                "price": 99.99,
                "stock": 10,
                "category_id": None
            }
        )
        assert response.status_code == 200
        assert response.json() == 1
        
        # Verify it was created
        response = self.client.get("/api/Products")
        assert response.status_code == 200
        products = response.json()
        assert len(products) == 1
        assert products[0]["id"] == 1
        assert products[0]["sku"] == "TEST001"
        assert products[0]["name"] == "Test Product"
        assert products[0]["price"] == 99.99
        assert products[0]["stock"] == 10
    
    def test_create_product_with_category(self):
        """Test creating a product with a category"""
        # Create a category first
        cat_response = self.client.post(
            "/api/ProductCategories",
            json={"name": "Electronics", "description": "Electronic items"}
        )
        category_id = cat_response.json()
        
        # Create product with category
        response = self.client.post(
            "/api/Products",
            json={
                "sku": "ELEC001",
                "name": "Laptop",
                "price": 1299.99,
                "stock": 5,
                "category_id": category_id
            }
        )
        assert response.status_code == 200
        product_id = response.json()
        
        # Verify product has category info
        response = self.client.get(f"/api/Products/{product_id}")
        product = response.json()
        assert product["category_id"] == category_id
        assert product["category"]["name"] == "Electronics"
    
    def test_create_product_duplicate_sku(self):
        """Test that duplicate SKU is rejected"""
        # Create first product
        self.client.post(
            "/api/Products",
            json={
                "sku": "DUP001",
                "name": "Product 1",
                "price": 50.00,
                "stock": 10
            }
        )
        
        # Try to create second product with same SKU
        response = self.client.post(
            "/api/Products",
            json={
                "sku": "DUP001",
                "name": "Product 2",
                "price": 60.00,
                "stock": 20
            }
        )
        assert response.status_code == 400
        assert "SKU already exists" in response.json()["detail"]
    
    def test_get_product_by_id(self):
        """Test getting a specific product by ID"""
        # Create a product
        create_response = self.client.post(
            "/api/Products",
            json={
                "sku": "PROD001",
                "name": "Test Product",
                "price": 99.99,
                "stock": 10
            }
        )
        product_id = create_response.json()
        
        # Get the product
        response = self.client.get(f"/api/Products/{product_id}")
        assert response.status_code == 200
        product = response.json()
        assert product["id"] == product_id
        assert product["sku"] == "PROD001"
        assert product["name"] == "Test Product"
    
    def test_get_nonexistent_product(self):
        """Test getting a product that doesn't exist"""
        response = self.client.get("/api/Products/999")
        assert response.status_code == 404
        assert response.json()["detail"] == "Product not found"
    
    def test_get_products_by_category(self):
        """Test filtering products by category"""
        # Create two categories
        cat1_response = self.client.post(
            "/api/ProductCategories",
            json={"name": "Category 1"}
        )
        cat1_id = cat1_response.json()
        
        cat2_response = self.client.post(
            "/api/ProductCategories",
            json={"name": "Category 2"}
        )
        cat2_id = cat2_response.json()
        
        # Create products in different categories
        self.client.post(
            "/api/Products",
            json={"sku": "CAT1_P1", "name": "Product 1", "price": 10.00, "stock": 5, "category_id": cat1_id}
        )
        self.client.post(
            "/api/Products",
            json={"sku": "CAT1_P2", "name": "Product 2", "price": 20.00, "stock": 10, "category_id": cat1_id}
        )
        self.client.post(
            "/api/Products",
            json={"sku": "CAT2_P1", "name": "Product 3", "price": 30.00, "stock": 15, "category_id": cat2_id}
        )
        
        # Get products from category 1
        response = self.client.get(f"/api/Products?category_id={cat1_id}")
        products = response.json()
        assert len(products) == 2
        assert all(p["category_id"] == cat1_id for p in products)
        
        # Get products from category 2
        response = self.client.get(f"/api/Products?category_id={cat2_id}")
        products = response.json()
        assert len(products) == 1
        assert products[0]["category_id"] == cat2_id
    
    def test_update_product(self):
        """Test updating an existing product"""
        # Create a product
        create_response = self.client.post(
            "/api/Products",
            json={
                "sku": "ORIG001",
                "name": "Original Product",
                "price": 99.99,
                "stock": 10,
                "description": "Original Description"
            }
        )
        product_id = create_response.json()
        
        # Update it
        update_response = self.client.put(
            f"/api/Products/{product_id}",
            json={
                "sku": "UPD001",
                "name": "Updated Product",
                "price": 149.99,
                "stock": 20,
                "description": "Updated Description"
            }
        )
        assert update_response.status_code == 200
        
        # Verify the update
        response = self.client.get(f"/api/Products/{product_id}")
        product = response.json()
        assert product["sku"] == "UPD001"
        assert product["name"] == "Updated Product"
        assert product["price"] == 149.99
        assert product["stock"] == 20
        assert product["description"] == "Updated Description"
    
    def test_update_product_sku_conflict(self):
        """Test that updating product with existing SKU fails"""
        # Create two products
        self.client.post(
            "/api/Products",
            json={"sku": "PROD001", "name": "Product 1", "price": 50.00, "stock": 10}
        )
        response2 = self.client.post(
            "/api/Products",
            json={"sku": "PROD002", "name": "Product 2", "price": 60.00, "stock": 20}
        )
        product2_id = response2.json()
        
        # Try to update product 2 with product 1's SKU
        response = self.client.put(
            f"/api/Products/{product2_id}",
            json={"sku": "PROD001", "name": "Product 2 Updated", "price": 70.00, "stock": 30}
        )
        assert response.status_code == 400
        assert "SKU conflict" in response.json()["detail"]
    
    def test_delete_product(self):
        """Test deleting an existing product"""
        # Create two products
        response1 = self.client.post(
            "/api/Products",
            json={"sku": "DEL001", "name": "Product 1", "price": 50.00, "stock": 10}
        )
        id1 = response1.json()
        response2 = self.client.post(
            "/api/Products",
            json={"sku": "DEL002", "name": "Product 2", "price": 60.00, "stock": 20}
        )
        id2 = response2.json()
        
        # Delete the first one
        delete_response = self.client.delete(f"/api/Products/{id1}")
        assert delete_response.status_code == 200
        
        # Verify only second remains
        response = self.client.get("/api/Products")
        products = response.json()
        assert len(products) == 1
        assert products[0]["id"] == id2
        assert products[0]["sku"] == "DEL002"
    
    def test_delete_nonexistent_product(self):
        """Test deleting a product that doesn't exist"""
        response = self.client.delete("/api/Products/999")
        assert response.status_code == 404
        assert response.json()["detail"] == "Product not found"
    
    def test_cors_headers(self):
        """Test that CORS headers are properly set"""
        # Make a request with an Origin header to trigger CORS
        response = self.client.get(
            "/api/Products",
            headers={"Origin": "http://localhost:3000"}
        )
        assert response.status_code == 200
        # CORS headers should be present in the response
        assert "access-control-allow-origin" in response.headers
        assert response.headers["access-control-allow-origin"] == "*"
        assert "access-control-allow-credentials" in response.headers
    
    def test_decimal_price_handling(self):
        """Test that decimal prices are handled correctly"""
        response = self.client.post(
            "/api/Products",
            json={
                "sku": "DEC001",
                "name": "Decimal Product",
                "price": 123.456789,  # Will be rounded/handled as Decimal
                "stock": 1
            }
        )
        assert response.status_code == 200
        product_id = response.json()
        
        # Verify price is stored correctly
        response = self.client.get(f"/api/Products/{product_id}")
        product = response.json()
        # Price should be a valid decimal number
        assert isinstance(product["price"], (int, float))
        assert product["price"] > 0