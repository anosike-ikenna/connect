from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.exceptions import ValidationError
from .models import TimeLine, Post

def home_page(request):
    if request.method == "POST":
        timeline = TimeLine.objects.create()
        new_post = request.POST["new_post"]
        post = Post.objects.create(text=new_post, timeline=timeline)
        try:
            post.full_clean()
        except ValidationError:
            timeline.delete()
            error = "You can't have an empty post"
            return render(request, "main/index.html", {"error": error})
        return redirect(f"/{timeline.id}/timeline/")
    posts = Post.objects.order_by("-created")
    return render(request, "main/index.html", {"posts": posts})

def view_timeline(request, id):
    timeline = TimeLine.objects.get(id=id)
    if request.method == "POST":
        Post.objects.create(text=request.POST["new_post"], timeline=timeline)
        return redirect(f"/{timeline.id}/timeline/")
    posts = timeline.post_set.order_by("-created")
    return render(
        request, 
        "main/timeline.html", 
        {
            "posts": posts,
            "timeline": timeline,
        }
    )