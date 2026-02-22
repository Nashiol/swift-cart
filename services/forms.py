# forms.py
from django import forms
from .models import Product, ProductImage, NewsLetterSubscription, Review, Category

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'status', 'stock', 'category']

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)

        # Add default placeholder to the 'status' field
        self.fields['status'].choices = [('', 'Select Condition')] + list(self.fields['status'].choices)

        # Apply 'form-control' to all fields
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

        # Apply additional classes to 'category' field
        self.fields['category'].widget.attrs.update({'class': 'form-select select2'})

class ProductImageForm(forms.ModelForm):
    class Meta:
        model = ProductImage
        fields = ['image']


class MessageForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea)

class NewsletterForm(forms.ModelForm):
    class Meta:
        model = NewsLetterSubscription
        fields = ['email']
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'})
        }


class SearchForm(forms.Form):
    query = forms.CharField(label='Search', max_length=100)


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.NumberInput(attrs={'min': 1, 'max': 5}),
        }
