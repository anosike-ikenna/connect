from django.shortcuts import render
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib import messages
from django.urls import reverse
from .models import Token

def send_login_email(request):
    email = request.POST["email"]
    username = request.POST["username"]
    token = Token.objects.create(email=email, username=username)
    url = request.build_absolute_uri(
        reverse("login") + "?token=" + str(token.uid)
    )
    message_body = f"Use this link to log in:\n\n{url}"
    send_mail(
        "Your login link for connect",
        message_body,
        "noreply@connect",
        [email],
    )
    messages.success(
        request,
        "Check your email, we've sent you a link you can use to log in"
    )
    return redirect("/")


def signup(request): 
    return render(request, "user/signup.html")

def login(request):
    return redirect("/")