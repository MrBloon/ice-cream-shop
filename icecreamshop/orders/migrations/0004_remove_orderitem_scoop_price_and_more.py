# Generated by Django 4.2 on 2023-05-03 12:38

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("orders", "0003_orderitem_scoop_price_alter_orderitem_order"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="orderitem",
            name="scoop_price",
        ),
        migrations.AddField(
            model_name="orderitem",
            name="price_per_scoop",
            field=models.IntegerField(default=2, editable=False),
        ),
    ]
