from django import forms

from main.models import Location
from users.models import User
from main.utils import get_weather_by_city


class CreateLocationForm(forms.ModelForm):
    name = forms.CharField(
        required=False, widget=forms.TextInput(attrs={"class": "clrtxt", "placeholder": "Название населенного пункта"})
    )
    user = forms.ModelChoiceField(
        queryset=User.objects.none(), widget=forms.HiddenInput()
    )

    class Meta:
        model = Location
        fields = ["name", "user"]
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields["user"].queryset = User.objects.filter(pk=user.pk)
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        city = self.cleaned_data.get("name")
        weather_raw_data = get_weather_by_city(city)
        if weather_raw_data is not None:
            instance.latitude = weather_raw_data["coord"]["lat"]
            instance.longitude = weather_raw_data["coord"]["lon"]
        if commit:
            instance.save()
        return instance
