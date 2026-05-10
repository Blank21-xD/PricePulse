import csv
import random
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.db.models import Q
from .models import Item, PriceHistory


def home(request):
    # 1. Get query parameters from the URL
    query = request.GET.get('q')
    store_filter = request.GET.get('store')

    # 2. Start with all items
    items = Item.objects.all()

    # 3. Apply Search Logic (Case-insensitive name search)
    if query:
        items = items.filter(Q(name__icontains=query))

    # 4. Apply Store Filtering
    if store_filter:
        items = items.filter(store=store_filter)

    # 5. Calculate Dashboard Statistics
    total_tracked = items.count()
    # sum(1...) counts how many items return True for the is_on_sale() model method
    on_sale_count = sum(1 for item in items if item.is_on_sale())

    context = {
        'items': items,
        'query': query,
        'store_filter': store_filter,
        'total_tracked': total_tracked,
        'on_sale_count': on_sale_count,
    }

    return render(request, 'home.html', context)


def check_price(request, item_id):
    """
    Simulates a price scraper. In a real app, this is where 
    you would call BeautifulSoup or Selenium.
    """
    item = get_object_or_404(Item, id=item_id)

    # Simulate price fluctuation (-$2.00 to +$2.00)
    variation = round(random.uniform(-2.0, 2.0), 2)
    new_price = float(item.target_price) + variation

    # Save the new price to history
    PriceHistory.objects.create(item=item, price=max(0, new_price))

    return redirect('home')


def export_history(request):
    """
    Generates a downloadable CSV file of all price records.
    """
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="price_pulse_history.csv"'

    writer = csv.writer(response)
    writer.writerow(['Item Name', 'Store', 'Price', 'Date Recorded'])

    # Optimization: select_related('item') prevents hitting the DB for every row
    history = PriceHistory.objects.all().select_related(
        'item').order_by('-recorded_at')

    for record in history:
        writer.writerow([
            record.item.name,
            record.item.store,
            f"${record.price}",
            record.recorded_at.strftime("%Y-%m-%d %H:%M")
        ])

    return response
