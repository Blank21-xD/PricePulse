from django.shortcuts import render, get_object_or_404, redirect
from tracker.models import Item, PriceHistory
from tracker.forms import ItemForm
from django.contrib import messages
from django.db.models import Avg
import random
import csv
from django.http import HttpResponse
from django.db.models import Q


def home(request):
    query = request.GET.get('q')
    store_filter = request.GET.get('store')

    items = Item.objects.all()

    # Apply Search
    if query:
        items = items.filter(Q(name__icontains=query))

    # Apply Store Filter
    if store_filter:
        items = items.filter(store=store_filter)

    return render(request, 'home.html', {
        'items': items,
        'query': query,
        'store_filter': store_filter
    })


def delete_item(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    item.delete()
    messages.warning(request, f"Deleted {item.name}.")
    return redirect('home')


def check_price(request, item_id):
    item = get_object_or_404(Item, id=item_id)

    # Simulate a price change
    variation = round(random.uniform(-2.0, 2.0), 2)
    new_price = max(0.01, float(item.target_price) + variation)

    # Save the pulse check
    PriceHistory.objects.create(item=item, price=new_price)
    messages.success(
        request, f"Pulse Check complete for {item.name}! New price: ${new_price:.2f}")

    return redirect('home')


def export_history(request):
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="price_history.csv"'

    writer = csv.writer(response)
    # Write the header row
    writer.writerow(['Item Name', 'Store', 'Price', 'Date Recorded'])

    # Get all history records
    history = PriceHistory.objects.all().select_related('item')
    for record in history:
        writer.writerow([record.item.name, record.item.store,
                        record.price, record.recorded_at])

    return response
