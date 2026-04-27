from django.shortcuts import render
from tracker.models import Item  # Import your model


def home(request):
    items = Item.objects.all()  # Fetch all items from the database
    # Pass them to the HTML
    return render(request, 'home.html', {'items': items})
