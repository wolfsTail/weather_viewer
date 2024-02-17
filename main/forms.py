from django import forms

from main.models import Location
from users.models import User
from main.utils import get_weather_by_city


class CreateLocationForm(forms.ModelForm):
    name = forms.CharField(
        required=True, widget=forms.TextInput(attrs={"class": "clrtxt", "placeholder": "Населенный пункт"})
    )

    class Meta:
        model = Location
        fields = ["name",]      
