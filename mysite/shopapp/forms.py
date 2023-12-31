from django import forms
from django.contrib.auth.models import Group
from django.core import validators
from . models import Product, Order



class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = "name",

class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["name", "price", "description", "diccount", "preview"]

    images = MultipleFileField()



 

# class ProductForm(forms.Form):
#     name = forms.CharField(max_length=100)
#     price = forms.DecimalField(min_value=1, max_value=100000)
#     description = forms.CharField(
#         label="product description", 
#         widget=forms.Textarea(attrs={"rows": 5, "cols": 30}),
#         validators=[validators.RegexValidator(
#             regex="great",
#             message="Field must contain word 'Great'"
#         )]
#     )



class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = "user", "products", "delivery_address", "promocode"
