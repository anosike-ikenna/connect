from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import TimeLine

def home_page(request):
    if request.method == "POST":
        new_post = request.POST["new_post"]
        TimeLine.objects.create(text=new_post)
        return redirect("home")
    posts = TimeLine.objects.order_by("-created")
    return render(request, "main/index.html", {"posts": posts})