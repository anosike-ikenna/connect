from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.exceptions import ValidationError
from .models import TimeLine, Post
from .forms import PostForm

def home_page(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            timeline = TimeLine.objects.create()
            Post.objects.create(text=request.POST["text"], timeline=timeline)
            return redirect(f"/{timeline.id}/timeline/")
        else:
            return render(request, "main/index.html", {"form": form})
    posts = Post.objects.order_by("-created")
    return render(request, "main/index.html", {"posts": posts})

def view_timeline(request, id):
    timeline = TimeLine.objects.get(id=id)
    error = None
    if request.method == "POST":
        try:
            post = Post.objects.create(text=request.POST["text"], timeline=timeline)
            post.full_clean()
            return redirect(f"/{timeline.id}/timeline/")
        except ValidationError:
            error = "You can't have an empty post"
            post.delete()
    posts = timeline.post_set.order_by("-created")
    return render(
        request, 
        "main/timeline.html", 
        {
            "posts": posts,
            "timeline": timeline,
            "error": error,
        }
    )

def view_timeline(request, id):
    timeline = TimeLine.objects.get(id=id)
    form = PostForm()
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            Post.objects.create(text=request.POST["text"], timeline=timeline)
            return redirect(f"/{timeline.id}/timeline/")
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