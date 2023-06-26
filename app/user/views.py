import json
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from user.forms import SigninForm, SignupForm
from user.models import User
from django.contrib import messages


# from .emailsend import email_send
# messages.add_message(request, messages.INFO, "Hello world.")


def login_view(request):
    form = SigninForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            print("form is valid")
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            user = authenticate(email=email, password=password)
            if user:
                login(request, user)
                return redirect("/")
            else:
                return render(
                    request,
                    "login.html",
                    {"error": "Invalid credentials", "form": form},
                )

    return render(request, "login.html", {"form": form})


def signup_view(request):
    form = SignupForm(request.POST or None)
    if request.method == "POST":
        # Name surname IBAN date of birth city country
        if form.is_valid():
            print("form is valid")
            username = form.cleaned_data.get("username")
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            surname = form.cleaned_data.get("surname")
            dob = form.cleaned_data.get("dob")
            city = form.cleaned_data.get("city")
            country = form.cleaned_data.get("country")
        else:
            return render(request, "register.html", {"form": form})

        if User.objects.filter(email=email).exists():
            messages.add_message(
                request, messages.ERROR, "A User with this email already exists."
            )

            return render(request, "register.html", {"form": form})

        else:
            user = User.objects.create(
                email=email,
                username=username,
                surname=surname,
                dob=dob,
                city=city,
                country=country,
            )
            user.set_password(password)
            user.is_active = True
            user.save()
            messages.add_message(
                request, messages.SUCCESS, "User created successfully."
            )
            return redirect("/login")

    return render(request, "register.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("/login")
