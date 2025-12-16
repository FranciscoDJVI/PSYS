from django.test import TestCase
from api.models import User, Product, Sell, SellItem
from rest_framework.test import APITestCase
from rest_framework import status


class SellStockTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpass", is_staff=True
        )
        self.client.force_authenticate(user=self.user)
        self.product = Product.objects.create(
            name="Test Product",
            brand="Brand",
            model="Model",
            sizes="M",
            description="Desc",
            price=10.0,
            stock=5,
        )

    def test_sell_decreases_stock(self):
        data = {
            "type_pay": "Efectivo",
            "sells": [{"product": self.product.pk, "quantity": 2}],
        }
        response = self.client.post("/api/v1.0/sells/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.product.refresh_from_db()
        self.assertEqual(self.product.stock, 3)

    def test_sell_insufficient_stock(self):
        data = {
            "type_pay": "Efectivo",
            "sells": [
                {
                    "product": self.product.id,
                    "quantity": 10,  # more than stock
                }
            ],
        }
        response = self.client.post("/api/v1.0/sells/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.product.refresh_from_db()
        self.assertEqual(self.product.stock, 5)  # unchanged
