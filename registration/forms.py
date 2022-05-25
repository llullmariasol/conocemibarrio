from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import views as auth_views
from .models import Neighborhood


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=100)

    password1 = forms.CharField(
        label='Contraseña',
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
    )

    password2 = forms.CharField(
        label='Confirmar contraseña',
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        strip=False,
    )

    def clean_password2(self):
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']

        if password1 != password2:
            raise forms.ValidationError("Las contraseñas no coinciden.")

        if len(password1) < 8:
            raise forms.ValidationError('Las contraseñas no pueden tener menos de 8 caracteres.')

        return password2

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.exclude().filter(username=username).exists():
            raise forms.ValidationError('El nombre elegido ya existe.')

        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.exclude().filter(email=email).exists():
            raise forms.ValidationError('El email elegido ya está en uso.')

        return email

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'password1',
            'password2',
        )
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': ''}),
            'email': forms.EmailInput(attrs={'placeholder': ''}),
        }
        labels = {
            'username': 'Nombre de usuario',
            'email': 'Correo electrónico',
        }
        help_texts = {
            'username': 'Ingrese 8 caracteres',
            'password1': ('Su contraseña no puede ser muy similar a su otra información personal.',
                          'Su contraseña debe contener al menos 8 caracteres.',
                          'Su contraseña no puede ser una contraseÃ±a de uso común.',
                          'Tu contraseña no puede ser completamente numérica.',)
        }
        error_messages = {
            'username': {
                'max_length': 'Nombre de usuario demasiado largo.',
            },
        }


class LogInForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Usuario'}), required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)

    def clean_password(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            self.user_cache = authenticate(username=username, password=password)
            if self.user_cache is None:
                raise forms.ValidationError("Por favor, ingrese el Usuario y la Contraseña correctos.")
        return password

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            raise forms.ValidationError("El nombre de Usuario ingresado no existe.")
        return username

    def login(self, request):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        return user


class PasswordResetForm(auth_views.PasswordResetForm):
    email = forms.EmailField(required=True)


class JoinNeighborhoodForm(forms.Form):
    ns = Neighborhood.objects.filter(is_active=1)
    n = forms.ModelMultipleChoiceField(queryset=Neighborhood.objects.all(), required=False)
