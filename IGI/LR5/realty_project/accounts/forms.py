from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User
from django.core.exceptions import ValidationError
import datetime


class RegisterForm(forms.ModelForm):
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Подтвердите пароль', widget=forms.PasswordInput)
    phone = forms.CharField(label='Телефон', required=True)
    budget = forms.DecimalField(
        label='Бюджет', 
        max_digits=12, 
        decimal_places=2, 
        required=False
    )

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'middle_name', 'birth_date', 'password1', 'password2']

    def clean_birth_date(self):
        birth_date = self.cleaned_data.get('birth_date')
        if not birth_date:
            raise ValidationError("Дата рождения обязательна")
        
        today = datetime.date.today()
        age = (today.year - birth_date.year) - (
            (today.month, today.day) < (birth_date.month, birth_date.day)
        )

        if age < 18:
            raise ValidationError("Вы должны быть старше 18 лет для регистрации")

        return birth_date

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise ValidationError({'password2': "Пароли не совпадают"})

        return cleaned_data


class AvatarUploadForm(forms.Form):
    avatar = forms.ImageField(label='Выберите аватар')