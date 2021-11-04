from django.shortcuts import render
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib import messages
from django.urls import reverse
from django.conf import settings
from django.contrib import auth
from .models import Token
import datetime

User = auth.get_user_model()

def send_login_email(request):
    email = request.POST["email"]
    username = request.POST["username"]
    token = Token.objects.create(email=email, username=username)
    token_timedelta = datetime.timedelta(seconds=settings.PASSWORD_RESET_TIMEOUT)
    token.expires = token.created + token_timedelta
    token.save()
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

def pre_login(request):
    if request.method == "POST":
        try:
            user = User.objects.get(email=request.POST["email"])
        except User.DoesNotExist:
            error = {"error": "Email does not exist"}
        else:
            request.POST = request.POST.copy()
            request.POST["username"] = user.username
            return send_login_email(request)
    return render(request, "user/pre_login.html")

def login(request):
    user = auth.authenticate(uid=request.GET.get("token"))
    if user:
        auth.login(request, user)
    return redirect("/")