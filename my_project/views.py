from django.shortcuts import render, get_object_or_404, redirect
from tracker.models import Item, PriceHistory
from tracker.forms import ItemForm
from django.contrib import messages
from django.db.models import Avg
import random


def home(request):
    # 1. Get the search query from the URL
    query = request.GET.get('search')

    # 2. Start with all items and prefetch history for speed
    items = Item.objects.prefetch_related('history').all()

    # 3. Filter if the user searched for something
    if query:
        items = items.filter(name__icontains=query)

    # 4. Handle Adding New Items (POST)
    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            new_item = form.save()
            # Create initial history entry
            PriceHistory.objects.create(
                item=new_item,
                price=new_item.target_price
            )
            messages.success(request, f"Successfully added {new_item.name}!")
            return redirect('home')
    else:
        form = ItemForm()

    # 5. Calculate Dashboard Stats
    stats = {
        'total_count': items.count(),
        'total_pulses': PriceHistory.objects.filter(item__in=items).count(),
        'avg_price': items.aggregate(Avg('target_price'))['target_price__avg'] or 0
    }

    return render(request, 'home.html', {
        'items': items,
        'form': form,
        'query': query,
        'stats': stats
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
