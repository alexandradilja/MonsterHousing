from django.forms import ModelForm, widgets
from Properties.models import *
from django_countries.fields import CountryField


class CitiesForm(ModelForm):
    country = CountryField(blank_label='Country').formfield(required=True)

    class Meta:
        model = Cities
        exclude = ['id', 'country']
        widgets = {
            'zip': widgets.NumberInput(attrs={'class': 'form-control', 'min': 0, 'placeholder': 'zip'}),
            'city': widgets.TextInput(attrs={'class': 'form-control', 'placeholder': 'City'})
        }


class AddressesForm(ModelForm):
    class Meta:
        model = Addresses
        exclude = ['id', 'city']
        widgets = {
            'street': widgets.TextInput(attrs={'class': 'form-control', 'placeholder': 'Street'}),
            'house_no': widgets.NumberInput(attrs={'class': 'form-control', 'min': 1, 'placeholder': 'House Number'})
        }


class TagsForm(ModelForm):
    class Meta:
        model = Tags
        exclude = ['id']
        widgets = {
            'elevator': widgets.CheckboxInput(attrs={'class': 'checkbox'}),
            'garage': widgets.CheckboxInput(attrs={'class': 'checkbox'}),
            'near_bloodbank': widgets.CheckboxInput(attrs={'class': 'checkbox'}),
            'dungeon': widgets.CheckboxInput(attrs={'class': 'checkbox'}),
            'secret_entrance': widgets.CheckboxInput(attrs={'class': 'checkbox'})
        }


class TypesForm(ModelForm):
    class Meta:
        CHOICES = [(types.id, types.type) for types in Types.objects.all()]
        model = Types
        exclude = ['id']
        widgets = {
            'type': widgets.Select(attrs={'class': 'dropdown'}, choices=CHOICES)
        }


class DetailsForm(ModelForm):
    class Meta:
        model = Details
        exclude = ['id', 'tags', 'type']
        widgets = {
            'size': widgets.TextInput(attrs={'class': 'form-control', 'min': 10, 'placeholder': 'Size'}),
            'price': widgets.NumberInput(attrs={'class': 'form-control', 'min': 0, 'placeholder': 'Price'}),
            'rooms': widgets.NumberInput(attrs={'class': 'form-control', 'min': 0, 'placeholder': 'Rooms'}),
            'description': widgets.TextInput(attrs={'class': 'form-control', 'placeholder': 'Description'}),
            'property_image': widgets.URLInput(attrs={'class': 'form-control', 'placeholder': 'Property Image Url'})
        }


class PropertiesForm(ModelForm):
    class Meta:
        model = Properties
        exclude = ['id', 'address', 'detail', 'user', 'is_active']
