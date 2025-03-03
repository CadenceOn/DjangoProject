from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Request, AnimatorOffer

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text="Введите ваш email.")
    role = forms.ChoiceField(choices=[
        ('customer', 'Пользователь'),
        ('animator', 'Аниматор'),
    ], label="Выберите вашу роль")

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'role']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Этот email уже используется.")
        return email

class RequestForm(forms.ModelForm):
    class Meta:
        model = Request
        fields = ['event_date', 'location', 'description']
        widgets = {
            'event_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

class AnimatorOfferForm(forms.ModelForm):
    class Meta:
        model = AnimatorOffer
        fields = ['available_date', 'location', 'description']
        widgets = {
            'available_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }