from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
import json

from .models import User, Post


def index(request):
    all_posts = Post.objects.all().order_by('-timestamp')
    paginator = Paginator(all_posts, 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "network/index.html", {
        "page_obj": page_obj,
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

def profile(request, username):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return render(request, "network/profile.html",{
            "exists": False
        })
    
    posts = Post.objects.filter(user=user).order_by('-timestamp')
    paginator = Paginator(posts, 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
     
    return render(request, "network/profile.html",{
        "exists": True, 
        "user": user,
        "is_following": request.user.following.filter(username=username).exists(),
        "followers": user.followers.count(),
        "following": user.following.count(),
        "page_obj": page_obj,
    })

@csrf_exempt
@login_required
def follow(request, username):
    if request.method != "POST":
        return JsonResponse({
            "error": "POST request required."
        }, status=400)

    try:
        already_follow = request.user.following.filter(username=username).exists()
        user = User.objects.get(username=username)
        if already_follow:
            request.user.following.remove(user)
            return JsonResponse({
                "newStatus": "Follow",
                "followers": user.followers.count()
            }, status=200)
        else:
            request.user.following.add(user)
            return JsonResponse({
                "newStatus": "Unfollow",
                "followers": user.followers.count()
            }, status=200)
        
    except:
        return HttpResponse(status=400)

@csrf_exempt
@login_required
def create_post(request):

    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)
    
    data = json.loads(request.body)
    content = data.get("content")
    if content == "":
        return JsonResponse({"error": "Content cannot be empty."}, status=400)
    
    post = Post(content=content, user=request.user)
    post.save()
    return JsonResponse({"message": "Post created succesfully."}, status=201)

@login_required
def following(request):
    following_pks = request.user.following.values_list('id', flat=True)
    posts = Post.objects.filter(user__pk__in=following_pks).order_by('-timestamp')

    paginator = Paginator(posts, 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "network/following.html", {
        "page_obj": page_obj,
    })

@csrf_exempt
@login_required
def edit_post(request):

    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)
    
    data = json.loads(request.body)
    post_id = data.get("post_id")

    try:
        post = Post.objects.get(pk=post_id)
    except:
        return JsonResponse({"error": "This post does not exist."}, status=400)
    
    if post.user != request.user:
        return JsonResponse({"error": "You are not the creator of this post."}, status=400)
    
    content = data.get("content")
    if content == "":
        return JsonResponse({"error": "Content cannot be empty."}, status=400)
    
    post.content = content
    post.save()

    return JsonResponse({"message": "Post updated successfully."}, status=201)

@csrf_exempt
@login_required
def like_post(request):

    if request.method == "POST":
        data = json.loads(request.body)
        post_id = data.get("post_id")

        try:
            post = Post.objects.get(pk=post_id)
        except:
            return JsonResponse({"error": "This post does not exist."}, status=400)
        
        if request.user in post.liked_by.all():
            post.liked_by.remove(request.user)
            num_likes = post.liked_by.count()
            return JsonResponse({"message": "Post unliked successfully.", "liked": False, "num_likes": num_likes}, status=201)
        else:
            post.liked_by.add(request.user)
            num_likes = post.liked_by.count()
            return JsonResponse({"message": "Post liked successfully.", "liked": True, "num_likes": num_likes}, status=201)
