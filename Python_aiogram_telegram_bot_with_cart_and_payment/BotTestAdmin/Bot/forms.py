from django import forms

from .models import People, Catalog


class PeopleForm(forms.ModelForm):
    class Meta:
        model = People
        fields = (
            'user_id',
            'user_name',
            'user_surname',
            'username',
            'active',
            'user_phone',
        )

        widgets = {
            'user_name': forms.TextInput,
            'user_surname': forms.TextInput,
            'username': forms.TextInput,
            'user_phone': forms.NumberInput,
        }


class CatalogForm(forms.ModelForm):
    class Meta:
        model = Catalog
        fields = (
            'prod_id',
            'prod_name',
            'prod_description',
            'prod_price',
            'prod_photo',
        )

        widgets = {
            'prod_name': forms.TextInput,
            'prod_description': forms.Textarea,
            'prod_photo': forms.TextInput,
        }
