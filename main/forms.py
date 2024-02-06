from django import forms

from main.models import Location
from users.models import User
from main.utils import get_weather_by_city


class CreateLocationForm(forms.ModelForm):
    name = forms.CharField(
        required=False, widget=forms.TextInput(attrs={"class": "clrtxt", "placeholder": "Название населенного пункта"})
    )

    class Meta:
        model = Location
        fields = ["name"]  
    
    def clean_name(self):
        name = self.cleaned_data.get("name")
        if name and not name.isspace():
            return name
        else:
            raise forms.ValidationError("Введите корректное название города!")
