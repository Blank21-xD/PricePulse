from django.shortcuts import render, get_object_or_404, redirect
from tracker.models import Item, PriceHistory


def home(request):
    """
    Fetches all items and their related price history.
    Using 'prefetch_related' makes the page load faster by 
    grabbing the history in one database query.
    """
    items = Item.objects.prefetch_related('history').all()
    return render(request, 'home.html', {'items': items})


def delete_item(request, item_id):
    """
    Deletes a specific item and redirects back to the homepage.
    """
    item = get_object_or_404(Item, id=item_id)
    item.delete()
    return redirect('home')
