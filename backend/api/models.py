import uuid
from django.db import models
from django.db.models import F
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)


class Product(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    brand = models.CharField(max_length=200)
    model = models.CharField(max_length=200)
    sizes = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()

    class Meta:
        unique_together = ("name", "brand", "model")

    # Decrease stock in a single product.
    def decrease_stock(self, quantity):
        if self.stock < quantity:
            raise ValueError(
                f"Stock insuficiente para {self.name}: disponible {self.stock}, solicitado {quantity}"
            )
        self.stock -= quantity
        self.save()

    # Decrease stock in bulk for multiple products. for more efficiency.
    @staticmethod
    def bulk_decrease_stock(sell_items_data):
        """Decrementa stock en bulk para múltiples productos."""
        for product, quantity in [
            (item["product"], item["quantity"]) for item in sell_items_data
        ]:
            product.stock = F("stock") - quantity
            product.save(update_fields=["stock"])

    def __str__(self) -> str:
        return str(self.name)


class Sell(models.Model):
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

    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    # Relation with model Product of ManyToMany.
    products = models.ManyToManyField(
        Product, through="SellItem", related_name="sell_items"
    )

    def __str__(self) -> str:
        return str(self.sell_id)


class SellItem(models.Model):
    sell = models.ForeignKey(Sell, on_delete=models.CASCADE, related_name="sells")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    @property
    def sell_subtotal(self):
        return float(self.product.price * self.quantity)

    def __str__(self):
        return f"{self.sell} {self.product}"
