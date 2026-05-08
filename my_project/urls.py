from django.contrib import admin
from django.urls import path
from .views import home
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('delete/<int:item_id>/', views.delete_item, name='delete_item'),
    path('check/<int:item_id>/', views.check_price, name='check_price'),
    path('export/', views.export_history, name='export_history'),
]
