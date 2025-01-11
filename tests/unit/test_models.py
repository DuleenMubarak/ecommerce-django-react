from django.test import TestCase
from base.models import Product, Review, Order
from django.contrib.auth.models import User
from django.utils.timezone import now

class ProductModelTest(TestCase):

    #creating test data
    def setUp(self):
        self.product = Product.objects.create(
            name="Test Product",
            price=100.0,
            brand="Test Brand",
            description="A product for testing purposes.",
            countInStock=10
        )
    #deleting the product after each test
    def tearDown(self):
        self.product.delete()

    #testing the creation of the product
    def test_product_creation(self):
        self.assertEqual(self.product.name, "Test Product")
        self.assertEqual(self.product.price, 100.0)
    
    #testing if a product can be updated
    def test_product_update(self):
        self.product.name = "Updated Product"
        self.product.price = 120.0
        self.product.save()
        self.assertEqual(self.product.name, "Updated Product")
        self.assertEqual(self.product.price, 120.0)

    #test negative stock - failed, value error didnt raise
    def test_product_negative_stock(self):
        self.product.countInStock = -5
        with self.assertRaises(ValueError):
            self.product.save()

class UserModelTest(TestCase):
    #creating user and superuser for tests
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="securepassword123"
        )
        self.superuser = User.objects.create_superuser(
            username="adminuser",
            email="adminuser@example.com",
            password="adminpassword123"
        )
    
    #delete data 
    def tearDown(self):
        self.user.delete()
        self.superuser.delete()

    #test creating normal user
    def test_user_creation(self):
        self.assertEqual(self.user.username, "testuser@example.com")
        self.assertEqual(self.user.email, "testuser@example.com")
        self.assertTrue(self.user.check_password("securepassword123"))
        self.assertFalse(self.user.is_staff)
        self.assertFalse(self.user.is_superuser)

    #test creating superuser
    def test_superuser_creation(self):
        self.assertEqual(self.superuser.username, "adminuser@example.com")
        self.assertEqual(self.superuser.email, "adminuser@example.com")
        self.assertTrue(self.superuser.check_password("adminpassword123"))
        self.assertTrue(self.superuser.is_staff)
        self.assertTrue(self.superuser.is_superuser)

    #test if usernames are unique
    def test_username_uniqueness(self):
        with self.assertRaises(Exception):
            User.objects.create_user(
                username="testuser",
                email="duplicate@example.com",
                password="password123"
            )

    #test updating the password
    def test_update_user_password(self):
        self.user.set_password("newsecurepassword123")
        self.user.save()
        self.assertTrue(self.user.check_password("newsecurepassword123"))

class ReviewModelTest(TestCase):
    
    #creating a user, a product and a review
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password123")
        self.product = Product.objects.create(
            name="Test Product",
            price=100.0,
            brand="Test Brand",
            description="Test Description",
            countInStock=10,
        )
        self.review = Review.objects.create(
            user=self.user,
            product=self.product,
            rating=5,
            comment="Excellent product!",
        )

    #delete data
    def tearDown(self):
        self.review.delete()
        self.product.delete()
        self.user.delete()
    
    #test creating the review
    def test_review_creation(self):
        self.assertEqual(self.review.user, self.user)
        self.assertEqual(self.review.product, self.product)
        self.assertEqual(self.review.rating, 5)
        self.assertEqual(self.review.comment, "Excellent product!")
        self.assertIsNotNone(self.review.created_at)
    
    #testing reviewing without writing a comment
    def test_review_without_comment(self):
        review_without_comment = Review.objects.create(
            user=self.user,
            product=self.product,
            rating=4,
        )
        self.assertEqual(review_without_comment.comment, None)
    
class OrderModelTest(TestCase):
    #create a user and an order 
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password123")
        self.order = Order.objects.create(
            user=self.user,
            paymentMethod="PayPal",
            taxPrice=10.00,
            shippingPrice=5.00,
            totalPrice=115.00,
            isPaid=False,
            isDelivered=False,
        )

    #delete data
    def tearDown(self):
        self.order.delete()
        self.user.delete()


    #test the order creation    
    def test_order_creation(self):
        self.assertEqual(self.order.user, self.user)
        self.assertEqual(self.order.paymentMethod, "PayPal")
        self.assertEqual(self.order.taxPrice, 10.00)
        self.assertEqual(self.order.shippingPrice, 5.00)
        self.assertEqual(self.order.totalPrice, 115.00)
        self.assertFalse(self.order.isPaid)
        self.assertFalse(self.order.isDelivered)
        self.assertIsNotNone(self.order.createdAt)
    
    #updating the paid status and timestamp of the order
    def test_order_paid_status(self):
        self.order.isPaid = True
        current_time = now()
        self.order.paidAt = current_time
        self.order.save()
        self.assertTrue(self.order.isPaid)
        self.assertEqual(str(self.order.paidAt), current_time)
    
    #testing the total amount of the order
    def test_order_total_calculation(self):
        self.order.totalPrice = self.order.taxPrice + self.order.shippingPrice + 100.00 #assuming the subtotal of the products is 100
        self.order.save()
        self.assertEqual(self.order.totalPrice, 115.00)