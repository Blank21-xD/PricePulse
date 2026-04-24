from django.db import db


class Item(models.Model):
    name = models.CharField(max_length=200)
    store = models.CharField(max_length=100, default="Woolworths")
    target_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
