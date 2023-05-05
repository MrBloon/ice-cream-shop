import random
import string

from django.db import models

from icecream_tubs.models import IceCreamTub


class Order(models.Model):
    email = models.EmailField(max_length=254)
    total_price = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    order_number = models.CharField(max_length=8, unique=True, blank=True)
    is_confirmed = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"Order {self.order_number}: price ({self.total_price} euros)"

    def update_total_price(self, scoops_requested: int, price_per_scoop: float) -> None:
        self.total_price += scoops_requested * price_per_scoop
        self.save()

    def update_scoops_available_in_tubs(self) -> None:
        for item in self.order_items.all():
            tub = item.ice_cream_tub
            tub.scoops_available -= item.scoops_requested
            tub.save()

    def save(self, *args, **kwargs) -> None:
        if not self.order_number:
            # Generate a random 8-character alphanumeric order number
            self.order_number = "".join(
                random.choices(string.ascii_uppercase + string.digits, k=8)
            )
        super().save(*args, **kwargs)


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="order_items"
    )
    ice_cream_tub = models.ForeignKey(IceCreamTub, on_delete=models.CASCADE)
    scoops_requested = models.PositiveIntegerField()

    price_per_scoop = 2

    def __str__(self) -> str:
        return f"{self.ice_cream_tub.flavor} - {self.scoops_requested} scoops"

    def save(self, *args, **kwargs) -> None:
        super().save(*args, **kwargs)

        self.order.update_total_price(self.scoops_requested, self.price_per_scoop)
