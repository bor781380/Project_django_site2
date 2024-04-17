from django import forms
import datetime
from .models import Product

class ProductForm(forms.Form):
    #id = forms.IntegerField(widget=forms.HiddenInput())
    name = forms.CharField(max_length=100, label="Наименование")
    description = forms.CharField(widget=forms.Textarea, label="Описание")
    price = forms.DecimalField(max_digits=8, decimal_places=2, label="Цена")
    quantity = forms.IntegerField(label="Количество")
    image = forms.ImageField(required=False)

class EditProductForm(forms.Form):
    product_options = forms.ChoiceField(label="Выберите товар", choices=[])
    name = forms.CharField(label="Название")
    description = forms.CharField(label="Описание")
    price = forms.DecimalField(label="Цена")
    quantity = forms.IntegerField(label="Количество")
    image = forms.ImageField(required=False)

    def __init__(self, *args, **kwargs):
        super(EditProductForm, self).__init__(*args, **kwargs)
        self.fields['product_options'].choices = [(obj.id, obj.name) for obj in Product.objects.all()]

class ImageForm(forms.Form):
    image = forms.ImageField()
    # file = forms.FileField()