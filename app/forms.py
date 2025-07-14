from django.contrib.auth.forms import UserCreationForm
from . import models
from django import forms
from django.contrib.auth import authenticate

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Обязательное поле. Введите действующий email.')

    class Meta:
        model = models.CustomUser
        fields = ('username', 'email', 'password1', 'password2','image')

class LoginForm(forms.Form):
    email = forms.EmailField(label="Email", widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        password = cleaned_data.get("password")

        if email and password:
            user = authenticate(email=email, password=password)
            if not user:
                raise forms.ValidationError("Неверный email или пароль.")
        return cleaned_data

    def get_user(self):
        return authenticate(
            email=self.cleaned_data.get("email"),
            password=self.cleaned_data.get("password"),
        )