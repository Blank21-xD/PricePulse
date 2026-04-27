from django.shortcuts import render
from tracker.models import Item  # Import your model


def home(request):
    items = Item.objects.all()  # Fetch all items from the database
    # Pass them to the HTML
    return render(request, 'home.html', {'items': items})


def delete_item(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    item.delete()
    return redirect('home')
