from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from store.models import Game, Developer, Category


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('There exists an account with this email already!', code="invalid")
        return email

class ForgotPasswordForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Enter your email'}))


class ResetPasswordForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'New password'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm new password'}))

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', 'Passwords do not match.')

class GameForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Game name'}))
    price = forms.DecimalField(widget=forms.NumberInput(attrs={'placeholder': 'Price'}))
    image = forms.ImageField(widget=forms.FileInput(attrs={'placeholder': 'Image'}), required=False)
    quantity = forms.IntegerField(widget=forms.NumberInput(attrs={'placeholder': 'Quantity'}))

    # platform choice
    platform = forms.ChoiceField(
        choices=Game.PLATFORM_CHOICES,
        required=True,
        widget=forms.Select()
    )

    # dev choice
    developer = forms.ModelChoiceField(
        queryset=Developer.objects.all(),
        required=True,
        empty_label="Select a developer",
        widget=forms.Select()
    )

    # cat choice
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=True,
        empty_label="Select a category",
        widget=forms.Select()
    )
    class Meta:
        model = Game
        fields = ('name', 'price', 'quantity', 'developer', 'category', 'platform', 'image')