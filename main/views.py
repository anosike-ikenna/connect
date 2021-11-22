from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.exceptions import ValidationError
from .models import TimeLine, Post
from .forms import PostForm

def home_page(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save(for_timeline=request.user.timeline)
            return redirect(f"/timeline/")
        else: 
            return render(request, "main/index.html", {"form": form})
    posts = Post.objects.order_by("-created")
    return render(request, "main/index.html", {"posts": posts})

def view_timeline(request):
    timeline = TimeLine.objects.get(user=request.user)
    form = PostForm()
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save(for_timeline=timeline)
            return redirect(f"/timeline/")
    posts = timeline.post_set.order_by("-created")
    return render(
        request, 
        "main/timeline.html", 
        {
            "posts": posts,
            "timeline": timeline,
            "form": form,
        }
    )