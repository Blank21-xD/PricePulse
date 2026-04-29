from django import forms
from .models import Item


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'store', 'target_price']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Item Name'}),
            'store': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Woolworths'}),
            'target_price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0.00'}),
        }
