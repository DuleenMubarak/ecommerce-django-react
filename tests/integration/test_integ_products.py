from rest_framework.test import APITestCase
from base.models import Product
from rest_framework import status


BASE_URL = "localhost:8000/api/products/"


class TestProductsIntegration(APITestCase):
    #create 2 products
    def setUp(self):
        """Create initial test data for products."""
        self.product1 = Product.objects.create(name="Product 1", price=20.00, countInStock=100)
        self.product2 = Product.objects.create(name="Product 2", price=30.00, countInStock=50)

    #delete data
    def tearDown(self):
        self.product1.delete()
        self.product2.delete()

    #test getting all products
    def test_get_products(self):
        response = self.client.get(BASE_URL)  # Use self.client for API requests
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.json(), list)
        self.assertGreaterEqual(len(response.json()), 2)

    #test getting product by its id
    def test_get_product_by_id(self):
        response = self.client.get(f"{BASE_URL}/{self.product1.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["name"], self.product1.name)

    #test adding a new product using POST request
    def test_add_new_product(self):
        new_product = {
            "name": "Test new product",
            "image": "/media/images/H043735e6f3ba4332a2b9e11928ccecb84.jpg_720x720q50.jpg",
            "brand": "Xiamen Sunshine",
            "category": "Educational",
            "description": (
                "Spark creativity and learning with our Rainbow Wooden Educational Block Building Toys! "
                "These vibrant, eco-friendly wooden blocks are designed to engage little hands and curious minds. "
                "Perfectly crafted for durability and safety, each block is painted with non-toxic, child-safe colors "
                "in a beautiful rainbow palette. Ideal for toddlers and young children, these blocks encourage "
                "fine motor skill development, cognitive growth, and imaginative play. Inspire endless hours of play "
                "and learning with this versatile set!"
            ),
            "price": "35.00",
            "countInStock": 50,
        }
        response = self.client.post(BASE_URL, new_product, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response_data = response.json()
        self.assertEqual(response_data["name"], new_product["name"])
        self.assertEqual(response_data["category"], new_product["category"])
        self.assertEqual(response_data["brand"], new_product["brand"])
        self.assertEqual(response_data["price"], float(new_product["price"]))
        self.assertEqual(response_data["countInStock"], new_product["countInStock"])

    #test updating an existing product
    def test_update_product(self):
        update_data = {
            "name": "Updated Product Name",
            "price": 25.00,
            "countInStock": 90,
        }
        response = self.client.put(f"{BASE_URL}{self.product1.id}/", update_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        updated_product = Product.objects.get(id=self.product1.id)
        self.assertEqual(updated_product.name, update_data["name"])
        self.assertEqual(updated_product.price, update_data["price"])
        self.assertEqual(updated_product.countInStock, update_data["countInStock"])

    #sorting by category
    def test_filter_products_by_category(self):
        self.product1.category = "Electronics"
        self.product1.save()
        self.product2.category = "Toys"
        self.product2.save()

        response = self.client.get(f"{BASE_URL}?category=Electronics")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        products = response.json()
        self.assertEqual(len(products), 1)
        self.assertEqual(products[0]["category"], "Electronics")
