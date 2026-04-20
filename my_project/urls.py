from django.contrib import admin
from django.urls import path
from .views import home  # Import your new view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home),  # This makes it the homepage
]
