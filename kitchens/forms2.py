from django import forms
from .models import Review


class ReviewsForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = '__all__'