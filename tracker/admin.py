from django.contrib import admin
from .models import Item


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'store', 'target_price', 'created_at')
    search_fields = ('name',)
