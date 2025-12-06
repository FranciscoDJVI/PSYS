import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser


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

    class TypePayChoice(models.TextChoices):
        CREDITO = "Tarjeta credito"
        DEBITO = "Tarjeta debito"
        EFECTIVO = "Efectivo"
        TRANSFERENCIA = "Transferencia"

    # ID unique in time and space.
    sell_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    type_pay = models.CharField(
        max_length=15, choices=TypePayChoice.choices, default=TypePayChoice.EFECTIVO
    )

    created_at = models.DateField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    # Relation with model Product of ManyToMany.
    products = models.ManyToManyField(
        Product, through="SellItem", related_name="sells_items"
    )

    def __str__(self) -> str:
        return str(self.sell_id)


class SellItem(models.Model):
    sell = models.ForeignKey(Sell, on_delete=models.CASCADE, related_name="sells")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    @property
    def sell_subtotal(self):
        self.total = float(self.product.price * self.quantity)
        return self.total

    def __str__(self):
        return f"{self.sell} {self.product}"
