from django.shortcuts import render
from django.http import HttpResponse

def home_page(request):
    return render(request, "main/index.html", {
        "new_post": request.POST.get("new_post", "")
    })