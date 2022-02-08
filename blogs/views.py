from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.http import Http404

from .models import BlogPost
from .forms import PostForm

# Create your views here.


def index(request):
    # return HttpResponse("index")
    # posts = BlogPost.objects.filter(owner=request.user).order_by("date_added")
    posts = BlogPost.objects.all()
    context = {"posts": posts}
    return render(request, "blogs/index.html", context)


@login_required
def new_post(request):
    """function to create a new post"""
    if request.method != "POST":
        # Display blank registration form.
        form = PostForm()
    else:
        form = PostForm(data=request.POST)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.owner = request.user
            new_post.save()
            return redirect("blogs:index")

    # Display a blank form
    context = {"form": form}
    return render(request, "blogs/new_post.html", context)


@login_required
def edit_post(request, post_id):
    """Edit exiting post"""
    post = BlogPost.objects.get(id=post_id)
    check_post_owner(request, post)
    if request.method != "POST":
        # Initial reques, pre-fill from the current post
        form = PostForm(instance=post)
    else:
        # POST data submitted; process data
        form = PostForm(instance=post, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect("blogs:index")
    context = {"post": post, "form": form}
    return render(request, "blogs/edit_post.html", context)


def check_post_owner(request, post):
    if post.owner != request.user:
        raise Http404
