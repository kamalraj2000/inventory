from typing import List, Optional, Dict
from models import Product, ProductCategory
from decimal import Decimal
import threading


class InMemoryDatabase:
    def __init__(self):
        self._products: Dict[int, Product] = {}
        self._product_categories: Dict[int, ProductCategory] = {}
        self._next_product_id = 1
        self._next_category_id = 1
        self._lock = threading.Lock()
        self._initialize_sample_data()
    
    # Product Category Methods
    def get_all_categories(self) -> List[ProductCategory]:
        with self._lock:
            return list(self._product_categories.values())
    
    def get_category_by_id(self, id: int) -> Optional[ProductCategory]:
        with self._lock:
            return self._product_categories.get(id)
    
    def create_category(self, name: str, description: Optional[str] = None) -> int:
        with self._lock:
            category = ProductCategory(
                id=self._next_category_id,
                name=name,
                description=description
            )
            self._product_categories[category.id] = category
            self._next_category_id += 1
            return category.id
    
    def update_category(self, id: int, name: str, description: Optional[str] = None) -> bool:
        with self._lock:
            if id in self._product_categories:
                self._product_categories[id].name = name
                self._product_categories[id].description = description
                return True
            return False
    
    def delete_category(self, id: int) -> bool:
        with self._lock:
            if id in self._product_categories:
                # Check if any products use this category
                for product in self._products.values():
                    if product.category_id == id:
                        return False  # Cannot delete category with products
                del self._product_categories[id]
                return True
            return False
    
    # Product Methods
    def get_all_products(self) -> List[Product]:
        with self._lock:
            products = list(self._products.values())
            # Add category details to each product
            for product in products:
                if product.category_id:
                    product.category = self._product_categories.get(product.category_id)
            return products
    
    def get_product_by_id(self, id: int) -> Optional[Product]:
        with self._lock:
            product = self._products.get(id)
            if product and product.category_id:
                product.category = self._product_categories.get(product.category_id)
            return product
    
    def get_products_by_category(self, category_id: int) -> List[Product]:
        with self._lock:
            products = [p for p in self._products.values() if p.category_id == category_id]
            for product in products:
                product.category = self._product_categories.get(category_id)
            return products
    
    def create_product(self, sku: str, name: str, price: Decimal, stock: int = 0, 
                      description: Optional[str] = None, category_id: Optional[int] = None) -> int:
        with self._lock:
            # Check if SKU already exists
            for product in self._products.values():
                if product.sku == sku:
                    return -1  # SKU already exists
            
            product = Product(
                id=self._next_product_id,
                sku=sku,
                name=name,
                description=description,
                category_id=category_id,
                stock=stock,
                price=price
            )
            self._products[product.id] = product
            self._next_product_id += 1
            return product.id
    
    def update_product(self, id: int, sku: str, name: str, price: Decimal, stock: int,
                      description: Optional[str] = None, category_id: Optional[int] = None) -> bool:
        with self._lock:
            if id in self._products:
                # Check if new SKU conflicts with another product
                for product_id, product in self._products.items():
                    if product_id != id and product.sku == sku:
                        return False  # SKU already exists
                
                self._products[id].sku = sku
                self._products[id].name = name
                self._products[id].description = description
                self._products[id].category_id = category_id
                self._products[id].stock = stock
                self._products[id].price = price
                return True
            return False
    
    def delete_product(self, id: int) -> bool:
        with self._lock:
            if id in self._products:
                del self._products[id]
                return True
            return False
    
    def _initialize_sample_data(self):
        # Create sample categories
        electronics_id = self.create_category("Electronics", "Electronic devices and accessories")
        clothing_id = self.create_category("Clothing", "Apparel and fashion items")
        books_id = self.create_category("Books", "Physical and digital books")
        home_id = self.create_category("Home & Garden", "Home improvement and garden supplies")
        sports_id = self.create_category("Sports & Outdoors", "Sports equipment and outdoor gear")
        
        # Create 20 sample products
        sample_products = [
            ("ELEC001", "Laptop Pro 15", Decimal("1299.99"), 15, "High-performance laptop with 15-inch display", electronics_id),
            ("ELEC002", "Wireless Mouse", Decimal("29.99"), 50, "Ergonomic wireless mouse with USB receiver", electronics_id),
            ("ELEC003", "USB-C Hub", Decimal("49.99"), 30, "7-in-1 USB-C hub with HDMI and card reader", electronics_id),
            ("ELEC004", "Mechanical Keyboard", Decimal("89.99"), 25, "RGB backlit mechanical gaming keyboard", electronics_id),
            ("CLOTH001", "Cotton T-Shirt", Decimal("19.99"), 100, "100% cotton crew neck t-shirt", clothing_id),
            ("CLOTH002", "Denim Jeans", Decimal("59.99"), 75, "Classic fit denim jeans", clothing_id),
            ("CLOTH003", "Running Shoes", Decimal("79.99"), 40, "Lightweight running shoes with cushioned sole", clothing_id),
            ("BOOK001", "Python Programming", Decimal("39.99"), 20, "Complete guide to Python programming", books_id),
            ("BOOK002", "Data Science Handbook", Decimal("49.99"), 15, "Comprehensive data science reference", books_id),
            ("BOOK003", "Cloud Architecture", Decimal("54.99"), 12, "Modern cloud architecture patterns", books_id),
            ("HOME001", "LED Desk Lamp", Decimal("34.99"), 35, "Adjustable LED desk lamp with USB charging", home_id),
            ("HOME002", "Plant Pot Set", Decimal("24.99"), 45, "Set of 3 ceramic plant pots", home_id),
            ("HOME003", "Tool Kit", Decimal("69.99"), 20, "25-piece home tool kit with case", home_id),
            ("SPORT001", "Yoga Mat", Decimal("29.99"), 60, "Non-slip exercise yoga mat", sports_id),
            ("SPORT002", "Dumbbell Set", Decimal("149.99"), 10, "Adjustable dumbbell set 5-50 lbs", sports_id),
            ("SPORT003", "Tennis Racket", Decimal("89.99"), 18, "Professional grade tennis racket", sports_id),
            ("ELEC005", "Webcam HD", Decimal("59.99"), 28, "1080p HD webcam with microphone", electronics_id),
            ("CLOTH004", "Winter Jacket", Decimal("129.99"), 30, "Waterproof insulated winter jacket", clothing_id),
            ("BOOK004", "Machine Learning", Decimal("44.99"), 16, "Introduction to machine learning", books_id),
            ("HOME004", "Storage Bins", Decimal("19.99"), 55, "Set of 4 stackable storage bins", home_id)
        ]
        
        for sku, name, price, stock, description, category_id in sample_products:
            self.create_product(sku, name, price, stock, description, category_id)


db = InMemoryDatabase()