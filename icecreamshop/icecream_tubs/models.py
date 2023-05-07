import os

from django.conf import settings
from django.db import models


class Flavor(models.Model):
    NAME_CHOICES = [
        ("CHOCOLATE_ORANGE", "Chocolate Orange"),
        ("MAPLE_SYRUP_WALNUT", "Maple Syrup Walnut"),
        ("MINT_CHOCOLATE", "Mint Chocolate"),
        ("VANILLA_STRAWBERRY_CHOCOLATE", "Vanilla Strawberry Chocolate"),
        ("WHITE_CHOCOLATE_RASPBERRY", "White Chocolate Raspberry"),
    ]

    name = models.CharField(choices=NAME_CHOICES, max_length=30, unique=True)
    photo = models.ImageField(upload_to="flavor_photos", null=True, blank=True)
    recipe = models.TextField(max_length=400)

    def __str__(self) -> str:
        return f"{self.name}"

    def save(self, *args, **kwargs) -> None:
        if not self.photo:
            # Set the photo attribute based on the selected name
            photo_name = self.name.lower().replace(" ", "_") + ".png"
            photo_path = os.path.join(settings.MEDIA_ROOT, "flavor_photos", photo_name)
            if os.path.exists(photo_path):
                self.photo.name = os.path.join("flavor_photos", photo_name)
        super().save(*args, **kwargs)


class IceCreamTub(models.Model):
    flavor = models.OneToOneField(Flavor, on_delete=models.CASCADE)
    scoops_available = models.IntegerField(default=40)

    scoops_initial_stock = 40

    def __str__(self) -> str:
        return f"{self.flavor} ({self.scoops_available} scoops)"

    @property
    def is_empty(self) -> bool:
        return self.scoops_available == 0

    @property
    def filling_rate(self) -> str:
        return f"{self.scoops_available / self.scoops_initial_stock * 100} %"

    def refill(self) -> None:
        self.scoops_available = self.scoops_initial_stock
        self.save()

    def save(self, *args, **kwargs) -> None:
        if self.is_empty:
            print(
                f"EMAIL: {self.flavor.name} tub is empty. Refill it in the admin back office!"
            )

        super().save(*args, **kwargs)
