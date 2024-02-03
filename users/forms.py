from django import forms
from django.contrib.auth import get_user_model


USER = get_user_model()

class RegistrationForm(forms.ModelForm):
    email = forms.CharField(required=True)
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].label = 'E-mail'
        self.fields['password'].label = 'Пароль'
        self.fields['confirm_password'].label = 'Повторите пароль'
        self.fields['username'].label = "Отображаемое имя пользователя"
        self.fields['username'].help_text = ""
        self.fields['first_name'].label = 'Ваше имя'
        self.fields['last_name'].label = 'Вашa фамилия'
    
    def clean_email(self):
        email = self.cleaned_data['email']
        if USER.objects.filter(email=email).exists():
            raise forms.ValidationError("Регистрационные данные не верны, измените пароль или E-mail")
        return email
    
    def clean(self):
        password = self.cleaned_data['password']
        confirm_password = self.cleaned_data['confirm_password']
        if password != confirm_password:
            raise forms.ValidationError("Введенные Вами пароли не совпадают!")
        return self.cleaned_data
    
    class Meta:
        model = USER
        fields = (
            'email',
            'password',
            'confirm_password',
            'username',
            'first_name',
            'last_name',
        )


class LoginForm(forms.ModelForm):
    email = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].label = 'Ваш E-mail'
        self.fields['password'].label = 'Пароль'
    
    def clean(self):
        email = self.cleaned_data['email']
        password = self.cleaned_data['password']
        user_qs = USER.objects.filter(email=email)
        if not user_qs.exists():
            raise forms.ValidationError(
                "Проверьте введенные регистрационные данные!"
                )
        else:
            user = user_qs.first()
            if not user.check_password(password):
                raise forms.ValidationError(
                "Введен неверный пароль. Попробуйте ещё раз. Не сдавайтесь!"
                )
        return self.cleaned_data
    
    class Meta:
        model = USER
        fields = (
            'email',
            'password',
        )


class UserProfileForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['readonly'] = True
        self.fields['username'].widget.attrs['readonly'] = True
        self.fields['username'].help_text = ""

    class Meta:
        model = USER
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
        )
