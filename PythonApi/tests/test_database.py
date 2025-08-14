import pytest
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from database import InMemoryDatabase
from models import Product, ProductCategory
from decimal import Decimal


class TestInMemoryDatabase:
    """Unit tests for the InMemoryDatabase class"""
    
    def setup_method(self):
        """Create a fresh database instance for each test"""
        self.db = InMemoryDatabase()
        # Clear sample data for isolated tests
        self.db._products.clear()
        self.db._product_categories.clear()
        self.db._next_product_id = 1
        self.db._next_category_id = 1
    
    def test_initial_state(self):
        """Test that database can be initialized"""
        assert self.db._products == {}
        assert self.db._product_categories == {}
        assert self.db._next_product_id == 1
        assert self.db._next_category_id == 1


class TestProductCategoryDatabase:
    """Unit tests for Product Category database operations"""
    
    def setup_method(self):
        """Create a fresh database instance for each test"""
        self.db = InMemoryDatabase()
        # Clear sample data for isolated tests
        self.db._products.clear()
        self.db._product_categories.clear()
        self.db._next_product_id = 1
        self.db._next_category_id = 1
    
    def test_create_category(self):
        """Test creating a single category"""
        category_id = self.db.create_category("Electronics", "Electronic devices")
        assert category_id == 1
        
        categories = self.db.get_all_categories()
        assert len(categories) == 1
        assert categories[0].id == 1
        assert categories[0].name == "Electronics"
        assert categories[0].description == "Electronic devices"
    
    def test_create_multiple_categories(self):
        """Test creating multiple categories with unique IDs"""
        id1 = self.db.create_category("Category 1", "Description 1")
        id2 = self.db.create_category("Category 2", "Description 2")
        id3 = self.db.create_category("Category 3", None)
        
        assert id1 == 1
        assert id2 == 2
        assert id3 == 3
        
        categories = self.db.get_all_categories()
        assert len(categories) == 3
        assert categories[0].name == "Category 1"
        assert categories[1].name == "Category 2"
        assert categories[2].name == "Category 3"
        assert categories[2].description is None
    
    def test_get_category_by_id(self):
        """Test retrieving a specific category by ID"""
        id1 = self.db.create_category("Category 1", "Desc 1")
        id2 = self.db.create_category("Category 2", "Desc 2")
        
        category = self.db.get_category_by_id(id1)
        assert category is not None
        assert category.id == id1
        assert category.name == "Category 1"
        
        category = self.db.get_category_by_id(id2)
        assert category is not None
        assert category.id == id2
        assert category.name == "Category 2"
        
        category = self.db.get_category_by_id(999)
        assert category is None
    
    def test_update_category(self):
        """Test updating an existing category"""
        category_id = self.db.create_category("Original", "Original Desc")
        
        success = self.db.update_category(category_id, "Updated", "Updated Desc")
        assert success == True
        
        category = self.db.get_category_by_id(category_id)
        assert category is not None
        assert category.name == "Updated"
        assert category.description == "Updated Desc"
    
    def test_update_nonexistent_category(self):
        """Test updating a category that doesn't exist"""
        success = self.db.update_category(999, "Name", "Description")
        assert success == False
    
    def test_delete_category(self):
        """Test deleting an existing category"""
        id1 = self.db.create_category("Category 1", None)
        id2 = self.db.create_category("Category 2", None)
        
        success = self.db.delete_category(id1)
        assert success == True
        
        categories = self.db.get_all_categories()
        assert len(categories) == 1
        assert categories[0].id == id2
    
    def test_delete_nonexistent_category(self):
        """Test deleting a category that doesn't exist"""
        success = self.db.delete_category(999)
        assert success == False
    
    def test_cannot_delete_category_with_products(self):
        """Test that category with products cannot be deleted"""
        category_id = self.db.create_category("Category", None)
        product_id = self.db.create_product("SKU001", "Product", Decimal("99.99"), 10, None, category_id)
        
        success = self.db.delete_category(category_id)
        assert success == False
        
        # Category should still exist
        category = self.db.get_category_by_id(category_id)
        assert category is not None


class TestProductDatabase:
    """Unit tests for Product database operations"""
    
    def setup_method(self):
        """Create a fresh database instance for each test"""
        self.db = InMemoryDatabase()
        # Clear sample data for isolated tests
        self.db._products.clear()
        self.db._product_categories.clear()
        self.db._next_product_id = 1
        self.db._next_category_id = 1
    
    def test_create_product(self):
        """Test creating a single product"""
        product_id = self.db.create_product(
            "SKU001", "Test Product", Decimal("99.99"), 10, "Description", None
        )
        assert product_id == 1
        
        products = self.db.get_all_products()
        assert len(products) == 1
        assert products[0].id == 1
        assert products[0].sku == "SKU001"
        assert products[0].name == "Test Product"
        assert products[0].price == Decimal("99.99")
        assert products[0].stock == 10
        assert products[0].description == "Description"
    
    def test_create_product_with_category(self):
        """Test creating a product with a category"""
        category_id = self.db.create_category("Electronics", None)
        product_id = self.db.create_product(
            "ELEC001", "Laptop", Decimal("1299.99"), 5, None, category_id
        )
        
        product = self.db.get_product_by_id(product_id)
        assert product is not None
        assert product.category_id == category_id
        assert product.category is not None
        assert product.category.name == "Electronics"
    
    def test_create_product_duplicate_sku(self):
        """Test that duplicate SKU returns -1"""
        id1 = self.db.create_product("DUP001", "Product 1", Decimal("50.00"), 10)
        id2 = self.db.create_product("DUP001", "Product 2", Decimal("60.00"), 20)
        
        assert id1 > 0
        assert id2 == -1
        
        # Only first product should exist
        products = self.db.get_all_products()
        assert len(products) == 1
        assert products[0].name == "Product 1"
    
    def test_get_product_by_id(self):
        """Test retrieving a specific product by ID"""
        id1 = self.db.create_product("SKU001", "Product 1", Decimal("10.00"), 5)
        id2 = self.db.create_product("SKU002", "Product 2", Decimal("20.00"), 10)
        
        product = self.db.get_product_by_id(id1)
        assert product is not None
        assert product.id == id1
        assert product.sku == "SKU001"
        
        product = self.db.get_product_by_id(id2)
        assert product is not None
        assert product.id == id2
        assert product.sku == "SKU002"
        
        product = self.db.get_product_by_id(999)
        assert product is None
    
    def test_get_products_by_category(self):
        """Test filtering products by category"""
        cat1_id = self.db.create_category("Category 1", None)
        cat2_id = self.db.create_category("Category 2", None)
        
        # Create products in different categories
        self.db.create_product("P1", "Product 1", Decimal("10.00"), 5, None, cat1_id)
        self.db.create_product("P2", "Product 2", Decimal("20.00"), 10, None, cat1_id)
        self.db.create_product("P3", "Product 3", Decimal("30.00"), 15, None, cat2_id)
        self.db.create_product("P4", "Product 4", Decimal("40.00"), 20, None, None)
        
        # Get products from category 1
        products = self.db.get_products_by_category(cat1_id)
        assert len(products) == 2
        assert all(p.category_id == cat1_id for p in products)
        assert all(p.category.name == "Category 1" for p in products)
        
        # Get products from category 2
        products = self.db.get_products_by_category(cat2_id)
        assert len(products) == 1
        assert products[0].category_id == cat2_id
        
        # Get products from non-existent category
        products = self.db.get_products_by_category(999)
        assert len(products) == 0
    
    def test_update_product(self):
        """Test updating an existing product"""
        product_id = self.db.create_product(
            "ORIG001", "Original", Decimal("99.99"), 10, "Original Desc", None
        )
        
        success = self.db.update_product(
            product_id, "UPD001", "Updated", Decimal("149.99"), 20, "Updated Desc", None
        )
        assert success == True
        
        product = self.db.get_product_by_id(product_id)
        assert product is not None
        assert product.sku == "UPD001"
        assert product.name == "Updated"
        assert product.price == Decimal("149.99")
        assert product.stock == 20
        assert product.description == "Updated Desc"
    
    def test_update_product_sku_conflict(self):
        """Test that updating with existing SKU fails"""
        id1 = self.db.create_product("SKU001", "Product 1", Decimal("10.00"), 5)
        id2 = self.db.create_product("SKU002", "Product 2", Decimal("20.00"), 10)
        
        # Try to update product 2 with product 1's SKU
        success = self.db.update_product(
            id2, "SKU001", "Product 2 Updated", Decimal("30.00"), 15
        )
        assert success == False
        
        # Product 2 should remain unchanged
        product = self.db.get_product_by_id(id2)
        assert product.sku == "SKU002"
        assert product.name == "Product 2"
    
    def test_update_nonexistent_product(self):
        """Test updating a product that doesn't exist"""
        success = self.db.update_product(
            999, "SKU999", "Product", Decimal("99.99"), 10
        )
        assert success == False
    
    def test_delete_product(self):
        """Test deleting an existing product"""
        id1 = self.db.create_product("SKU001", "Product 1", Decimal("10.00"), 5)
        id2 = self.db.create_product("SKU002", "Product 2", Decimal("20.00"), 10)
        
        success = self.db.delete_product(id1)
        assert success == True
        
        products = self.db.get_all_products()
        assert len(products) == 1
        assert products[0].id == id2
    
    def test_delete_nonexistent_product(self):
        """Test deleting a product that doesn't exist"""
        success = self.db.delete_product(999)
        assert success == False
    
    def test_id_persistence_after_deletion(self):
        """Test that IDs continue incrementing even after deletions"""
        id1 = self.db.create_product("SKU001", "Product 1", Decimal("10.00"), 5)
        id2 = self.db.create_product("SKU002", "Product 2", Decimal("20.00"), 10)
        
        # Delete all products
        self.db.delete_product(id1)
        self.db.delete_product(id2)
        
        # Create new products - IDs should continue from 3
        id3 = self.db.create_product("SKU003", "Product 3", Decimal("30.00"), 15)
        id4 = self.db.create_product("SKU004", "Product 4", Decimal("40.00"), 20)
        
        assert id3 == 3
        assert id4 == 4
        
        products = self.db.get_all_products()
        assert len(products) == 2
        assert products[0].id == 3
        assert products[1].id == 4


class TestDatabaseConcurrency:
    """Test thread safety of database operations"""
    
    def setup_method(self):
        """Create a fresh database instance for each test"""
        self.db = InMemoryDatabase()
        # Clear sample data for isolated tests
        self.db._products.clear()
        self.db._product_categories.clear()
        self.db._next_product_id = 1
        self.db._next_category_id = 1
    
    def test_concurrent_product_creation(self):
        """Test thread safety with concurrent product creation"""
        import threading
        
        results = []
        
        def create_products():
            for i in range(10):
                product_id = self.db.create_product(
                    f"SKU{threading.current_thread().name}_{i}",
                    f"Product {i}",
                    Decimal("99.99"),
                    10
                )
                results.append(product_id)
        
        # Create multiple threads
        threads = [threading.Thread(target=create_products, name=str(i)) for i in range(3)]
        
        # Start all threads
        for t in threads:
            t.start()
        
        # Wait for completion
        for t in threads:
            t.join()
        
        # Check that we have 30 products with unique IDs
        products = self.db.get_all_products()
        assert len(products) == 30
        assert len(set(results)) == 30  # All IDs should be unique
        assert -1 not in results  # No SKU conflicts should occur
    
    def test_concurrent_category_operations(self):
        """Test thread safety with concurrent category operations"""
        import threading
        
        category_ids = []
        
        def create_categories():
            for i in range(5):
                cat_id = self.db.create_category(
                    f"Category {threading.current_thread().name}_{i}",
                    "Description"
                )
                category_ids.append(cat_id)
        
        # Create multiple threads
        threads = [threading.Thread(target=create_categories, name=str(i)) for i in range(3)]
        
        # Start all threads
        for t in threads:
            t.start()
        
        # Wait for completion
        for t in threads:
            t.join()
        
        # Check that we have 15 categories with unique IDs
        categories = self.db.get_all_categories()
        assert len(categories) == 15
        assert len(set(category_ids)) == 15  # All IDs should be unique


class TestSampleDataInitialization:
    """Test the sample data initialization"""
    
    def test_sample_data_created(self):
        """Test that sample data is created on initialization"""
        db = InMemoryDatabase()
        
        # Check categories were created
        categories = db.get_all_categories()
        assert len(categories) == 5
        category_names = [c.name for c in categories]
        assert "Electronics" in category_names
        assert "Clothing" in category_names
        assert "Books" in category_names
        assert "Home & Garden" in category_names
        assert "Sports & Outdoors" in category_names
        
        # Check products were created
        products = db.get_all_products()
        assert len(products) == 20
        
        # Check products have categories
        products_with_categories = [p for p in products if p.category_id is not None]
        assert len(products_with_categories) == 20
        
        # Check some specific products
        laptop = next((p for p in products if p.sku == "ELEC001"), None)
        assert laptop is not None
        assert laptop.name == "Laptop Pro 15"
        assert laptop.price == Decimal("1299.99")
        assert laptop.stock == 15
        assert laptop.category.name == "Electronics"