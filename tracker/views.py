from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect

def delete_item(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    item.delete()
    return redirect('home')

# Create your views here.
