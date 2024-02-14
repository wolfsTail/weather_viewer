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
    
    def clean_name(self):
        name = self.cleaned_data.get("name")

        if not name or not name.isspace():
            raise forms.ValidationError("Введите корректное название города!")
        
        return name

