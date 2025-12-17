from django.test import TestCase
from api.models import User, Product, Sell, SellItem
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse


class ProductModelTestCase(TestCase):
    def setUp(self):
        self.product = Product.objects.create(
            name="Test Product",
            brand="Brand",
            model="Model",
            sizes="M",
            description="Desc",
            price=10.0,
            stock=5,
        )

    def test_decrease_stock_success(self):
        self.product.decrease_stock(2)
        self.assertEqual(self.product.stock, 3)

    def test_decrease_stock_insufficient(self):
        with self.assertRaises(ValueError):
            self.product.decrease_stock(10)
        self.assertEqual(self.product.stock, 5)  # unchanged


class UserAPITestCase(APITestCase):
    def setUp(self):
        self.admin_user = User.objects.create_user(
            username="admin",
            email="admin@test.com",
            password="adminpass",
            is_staff=True,
            is_superuser=True,
        )
        self.normal_user = User.objects.create_user(
            username="user", email="user@test.com", password="userpass", is_staff=False
        )
        self.user_data = {
            "username": "newuser",
            "email": "newuser@test.com",
            "password": "newpass",
            "is_staff": False,
        }

    def test_list_users(self):
        response = self.client.get("/api/v1.0/users/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 2)

    def test_retrieve_user(self):
        response = self.client.get(f"/api/v1.0/users/{self.admin_user.pk}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["username"], "admin")

    def test_create_user_unauthenticated(self):
        response = self.client.post("/api/v1.0/users/", self.user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 3)


class ProductAPITestCase(APITestCase):
    def setUp(self):
        self.admin_user = User.objects.create_user(
            username="admin",
            email="admin@test.com",
            password="adminpass",
            is_staff=True,
            is_superuser=True,
        )
        self.normal_user = User.objects.create_user(
            username="user", email="user@test.com", password="userpass", is_staff=False
        )
        self.product = Product.objects.create(
            name="Test Product",
            brand="Brand",
            model="Model",
            sizes="M",
            description="Desc",
            price=10.0,
            stock=5,
        )
        self.product_zero_stock = Product.objects.create(
            name="Zero Stock Product",
            brand="Brand",
            model="Model",
            sizes="L",
            description="Desc",
            price=15.0,
            stock=0,
        )
        self.product_data = {
            "name": "New Product",
            "brand": "New Brand",
            "model": "New Model",
            "sizes": "XL",
            "description": "New Desc",
            "price": 20.0,
            "stock": 10,
        }

    def test_list_products(self):
        response = self.client.get("/api/v1.0/products/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 2)  # Includes zero stock

    def test_list_products_in_stock_filter(self):
        response = self.client.get("/api/v1.0/products/?in_stock=true")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)  # Only stock > 0

    def test_retrieve_product(self):
        response = self.client.get(f"/api/v1.0/products/{self.product.pk}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Test Product")

    def test_create_product_admin(self):
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.post("/api/v1.0/products/", self.product_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 3)

    def test_create_product_normal_user_forbidden(self):
        self.client.force_authenticate(user=self.normal_user)
        response = self.client.post("/api/v1.0/products/", self.product_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_product_admin(self):
        self.client.force_authenticate(user=self.admin_user)
        update_data = {"name": "Updated Product"}
        response = self.client.patch(
            f"/api/v1.0/products/{self.product.pk}/", update_data
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.product.refresh_from_db()
        self.assertEqual(self.product.name, "Updated Product")

    def test_delete_product_admin(self):
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.delete(f"/api/v1.0/products/{self.product.pk}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Product.objects.count(), 1)

    def test_search_products(self):
        response = self.client.get("/api/v1.0/products/?search=Test")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)

    def test_ordering_products(self):
        response = self.client.get("/api/v1.0/products/?ordering=price")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"][0]["price"], "10.00")


class SellItemAPITestCase(APITestCase):
    def setUp(self):
        self.admin_user = User.objects.create_user(
            username="admin_si",
            email="admin_si@test.com",
            password="adminpass",
            is_staff=True,
        )
        self.normal_user = User.objects.create_user(
            username="user_si", email="user_si@test.com", password="userpass"
        )
        self.product = Product.objects.create(
            name="Test Product SI",
            brand="Brand",
            model="Model",
            sizes="M",
            description="Desc",
            price=10.0,
            stock=5,
        )
        self.sell = Sell.objects.create(
            user=self.admin_user,
            type_pay="Efectivo",
        )
        self.sell_item_data = {
            "sell": self.sell.pk,
            "product": self.product.pk,
            "quantity": 2,
        }

    def test_list_sell_items(self):
        response = self.client.get("/api/v1.0/sellitems/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_sell_item_admin(self):
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.post("/api/v1.0/sellitems/", self.sell_item_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_sell_item_normal_user_forbidden(self):
        self.client.force_authenticate(user=self.normal_user)
        response = self.client.post("/api/v1.0/sellitems/", self.sell_item_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class SellAPITestCase(APITestCase):
    def setUp(self):
        self.admin_user = User.objects.create_user(
            username="admin_s",
            email="admin_s@test.com",
            password="adminpass",
            is_staff=True,
        )
        self.normal_user = User.objects.create_user(
            username="user_s", email="user_s@test.com", password="userpass"
        )
        self.normal_user = User.objects.create_user(
            username="user", email="user@test.com", password="userpass"
        )
        self.product = Product.objects.create(
            name="Test Product",
            brand="Brand",
            model="Model",
            sizes="M",
            description="Desc",
            price=10.0,
            stock=5,
        )
        self.sell_data = {
            "type_pay": "Efectivo",
            "sells": [{"product": self.product.pk, "quantity": 2}],
        }

    def test_list_sells(self):
        response = self.client.get("/api/v1.0/sells/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_sell_authenticated(self):
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.post("/api/v1.0/sells/", self.sell_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.product.refresh_from_db()
        self.assertEqual(self.product.stock, 3)

    def test_create_sell_unauthenticated_forbidden(self):
        response = self.client.post("/api/v1.0/sells/", self.sell_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_sell_total_price_calculation(self):
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.post("/api/v1.0/sells/", self.sell_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(float(response.data["total_price"]), 20.0)  # 10 * 2


class AuthenticationAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser_a", email="testuser_a@test.com", password="testpass"
        )

    def test_token_obtain_success(self):
        data = {"username": "testuser_a", "password": "testpass"}
        response = self.client.post("/api/v1.0/auth/token/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_token_obtain_invalid_credentials(self):
        data = {"username": "testuser_a", "password": "wrongpass"}
        response = self.client.post("/api/v1.0/auth/token/", data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
