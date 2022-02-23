from django import forms
from .models import Reviews

class RewiesForm(forms.ModelForm):
    """Форма отзывов"""
    class Meta:
        model = Reviews
        fields = ['name', 'email', 'text']