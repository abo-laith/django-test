from django import forms
from .models import Products

class UpdateProduct(forms.ModelForm):
    # barcode=forms.CharField(label='barcode')
    # name=forms.CharField(label='name')
    # image=forms.ImageField(label='image')
    class Meta:
        model=Products
        fields=('image',)

class AddProduct(forms.ModelForm):
    class Meta:
        model=Products
        fields=('image',)