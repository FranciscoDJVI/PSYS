import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import choices


class User(AbstractUser):
    pass


class Product(models.Model):
    name = models.CharField(max_length=200)
    brand = models.CharField(max_length=200)
    model = models.CharField(max_length=200)
    sizes = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()

    def __str__(self) -> str:
        return str(self.name)


class Sell(models.Model):
    class StatusChoices(models.TextChoices):
        PENDING = "Pending"
        CONFIRMED = "Confirmed"
        CANCELED = "Canceled"

    # ID unique in time and space.
    sell_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    status = models.CharField(
        max_length=10, choices=StatusChoices.choices, default=StatusChoices.PENDING
    )
    created_at = models.DateTimeField(auto_now_add=True)

    # Relation with model Product of ManyToMany.
    products = models.ManyToManyField(Product, through="SellItem", related_name="sells")

    def __str__(self) -> str:
        return str(self.sell_id)


class SellItem(models.Model):
    sell = models.ForeignKey(Sell, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    @property
    def sell_subtotal(self):
        return self.product.price * self.quantity

    def __str__(self):
        return f"{self.sell} {self.product}"
