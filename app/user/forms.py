from django.forms import ModelForm
from django import forms

from user.models import User


class SignupForm(forms.Form):
    username = forms.CharField(
        max_length=255,
        required=True,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )

    email = forms.EmailField(
        max_length=255,
        required=True,
        widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": "email@email.com"}),
    )

    password = forms.CharField(
        max_length=255,
        required=True,
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
    )

    surname = forms.CharField(
        max_length=255,
        required=True,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )

    dob = forms.DateField(
        required=True,
        widget=forms.DateInput(attrs={"class": "form-control", "type": "date"}),
    )

    city = forms.CharField(
        required=True,
        max_length=255,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )

    country = forms.CharField(
        required=True,
        max_length=255,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )

    class Meta:
        model = User
        fields = ["username" "password", "surname", "dob", "city", "country"]



class SigninForm(forms.Form):
    email = forms.EmailField(
        max_length=255,
        required=True,
        widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": "email@email.com"}),
    )

    password = forms.CharField(
        max_length=255,
        required=True,
        widget=forms.PasswordInput(attrs={"class": "form-control"}),

    )