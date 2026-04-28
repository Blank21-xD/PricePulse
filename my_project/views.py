from django.shortcuts import render, get_object_or_404, redirect
from tracker.models import Item, PriceHistory
from tracker.forms import ItemForm


def home(request):
    """
    Handles displaying the item list and the 'Add Item' form.
    When a new item is saved, it also logs the initial price in PriceHistory.
    """
    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            # Save the item first
            new_item = form.save()

            # Create the initial history entry automatically
            PriceHistory.objects.create(
                item=new_item,
                price=new_item.target_price
            )

            return redirect('home')
    else:
        form = ItemForm()

    # Prefetch history to keep the database queries efficient
    items = Item.objects.prefetch_related('history').all()

    return render(request, 'home.html', {
        'items': items,
        'form': form
    })


def delete_item(request, item_id):
    """
    Deletes a specific item and all its history (due to CASCADE).
    """
    item = get_object_or_404(Item, id=item_id)
    item.delete()
    return redirect('home')
