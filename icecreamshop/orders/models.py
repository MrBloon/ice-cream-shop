import random
import string

from django.core.exceptions import ValidationError
from django.db import models

from icecream_tubs.models import IceCreamTub


class Order(models.Model):
    email = models.EmailField(max_length=254, unique=True)
    total_price = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    order_number = models.CharField(max_length=8, unique=True, blank=True)
    is_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return f"Order {self.order_number}: price ({self.total_price} euros)"

    def update_total_price(self, scoops_requested):
        self.total_price += scoops_requested * 2
        self.save()

    def update_scoops_available_in_tubs(self):
        for item in self.orderitem_set.all():
            tub = item.ice_cream_tub
            tub.scoops_available -= item.scoops_requested
            tub.save()

    def confirm(self):
        self.is_confirmed = True
        self.save()
        self.update_scoops_available_in_tubs()

    def save(self, *args, **kwargs):
        if not self.order_number:
            # Generate a random 8-character alphanumeric order number
            self.order_number = "".join(
                random.choices(string.ascii_uppercase + string.digits, k=8)
            )
        super().save(*args, **kwargs)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    ice_cream_tub = models.ForeignKey(IceCreamTub, on_delete=models.CASCADE)
    scoops_requested = models.PositiveIntegerField()

    def __init__(self, *args, **kwargs):
        if self.order.is_confirmed:
            raise ValidationError(f"Order {self.order.order_number} is already confirmed")
        super().__init__(*args, **kwargs)

    def __str__(self):
        return f"{self.ice_cream_tub.flavor} - {self.scoops_requested} scoops"

    def clean(self):
        if self.scoops_requested > self.ice_cream_tub.scoops_available:
            raise ValidationError(
                "Number of scoops_requested exceeds number of scoops available in ice cream tub."
            )

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        self.order.update_total_price(self.scoops_requested)
