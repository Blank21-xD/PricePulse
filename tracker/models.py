from django.db import models


class Item(models.Model):
    name = models.CharField(max_length=200)
    store = models.CharField(max_length=100, default="Woolworths")
    target_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    # MOVE THIS INSIDE THE CLASS
    def get_trend(self):
        history = self.history.all()[:2]  # Get the 2 most recent prices
        if len(history) < 2:
            return "neutral"
        if history[0].price < history[1].price:
            return "down"
        if history[0].price > history[1].price:
            return "up"
        return "neutral"

    def is_on_sale(self):
        # Gets the newest price thanks to ordering = ['-recorded_at']
        latest_history = self.history.first()
        if latest_history:
            return latest_history.price <= self.target_price
        return False


class PriceHistory(models.Model):
    item = models.ForeignKey(
        Item, on_delete=models.CASCADE, related_name='history')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    recorded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-recorded_at']


def get_price_diff_percent(self):
    history = self.history.all()[:2]
    if len(history) < 2:
        return 0
    latest = float(history[0].price)
    previous = float(history[1].price)
    if previous == 0:
        return 0

    # Calculate percentage change
    diff = ((latest - previous) / previous) * 100
    return round(diff, 1)
