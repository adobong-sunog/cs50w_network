import json
from re import S
from turtle import title
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator
from django.db.models import OuterRef, Count
from django.views.decorators.csrf import csrf_exempt
from .models import *

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


def index(request):
    # Pagination, setting the most recent posts to show up first
    if request.user.is_authenticated:
        numof_likes = Like.objects.filter(postID_id=OuterRef('id'), liker_id=request.session["_auth_user_id"])
        p = Post.objects.all().order_by("-date").annotate(num_likes=Count(numof_likes.values("id")))
        print(p)
    else:
        p = Post.objects.all().order_by("-date")

    paginator = Paginator(p, 10)
    page_number = request.GET.get('page')
    eachP = paginator.get_page(page_number)

    return render(request, "network/index.html", {
        "posts": eachP,
        "title": "All posts",
    })

def only_following(request):
    userID = request.session["_auth_user_id"]
    f = Follows.objects.filter(followers_id=userID).values_list("following_id", flat=True)

    # If queryset is empty
    if not f:
        return render(request, "network/index.html", {
        "message": "It seems that you haven't follow anyone yet / None of the people you follow has posted anything.",
        "title": "Following"
    })

    # Pagination
    numof_likes = Like.objects.filter(postID_id=OuterRef('id'), liker_id=request.session["_auth_user_id"])
    p = Post.objects.filter(poster_id__in=f).order_by("-date").annotate(num_likes=Count(numof_likes.values("id")))
    paginator = Paginator(p, 10)
    page_number = request.GET.get('page')
    eachP = paginator.get_page(page_number)

    return render(request, "network/index.html", {
        "posts": eachP,
        "title": "Following"
    })

def create_post(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    posted = json.loads(request.body)
    txt = posted.get('text')

    # Make sure post is not empty
    if len(txt) == 0:
        return JsonResponse({
            "error": "User tried to make an empty post."
        }, status=400)

    # Accept post with no image URL    
    img = posted.get('image')
    if len(img) == 0:
        img = None

    choice = posted.get('choice')

    # Check if user wants to create or edit post
    if choice == 'post':
        try:
            sender = int(posted.get('sender'))
            savepost = Post(
                text=txt,
                image=img,
                poster=User.objects.get(id=sender)
            )
            savepost.save()
            return JsonResponse({"message": "Post successfully created"}, status=201)
        except:
            return JsonResponse({"error": "Input value error in creating post."}, status=400)
    elif choice == 'edit':
        try:
            postid = posted.get('postid')
            Post.objects.filter(id=postid).update(text=txt, image=img)
            return JsonResponse({"message": "Post successfully edited", "newtxt": Post.objects.filter(id=postid).values_list("text", flat=True).first(), "newimg": Post.objects.filter(id=postid).values_list("image", flat=True).first() ,"status": 201})
        except:
            return JsonResponse({"error": "Input value error in editing post."}, status=400)
    else:
        return JsonResponse({"error": "Option error in creating/editing post."}, status=400)

def profile(request, name):
    current_user = request.session["_auth_user_id"]
    check_info = User.objects.filter(username=name).values_list("id", flat=True).first()
    info = User.objects.filter(username=name)
    numof_likes = Like.objects.filter(postID_id=OuterRef("id"), liker_id=check_info)
    follow_info = Post.objects.filter(poster_id=check_info).order_by("-date").annotate(num_likes=Count(numof_likes.values("id")))

    # Check if user is checking their own profile
    same = False
    if check_info == int(current_user):
        same = True

    # Count following & followers
    following_count = Follows.objects.filter(followers_id=check_info).count()
    follower_count = Follows.objects.filter(following_id=check_info).count()

    # Check if user already follows the profile they're checking
    already = False
    is_following = Follows.objects.filter(followers_id=current_user).filter(following_id=check_info)
    if is_following.exists():
        already = True

    return render(request, "network/profile.html", {
        "info": info,
        "follow_info": follow_info,
        "followers": follower_count,
        "following": following_count,
        "same": same,
        "already": already
    })

def follow(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    info = json.loads(request.body)
    followed = int(info.get('followed'))
    follower = int(info.get('follower'))
    check = info.get('check')

    # Check if user wants to follow/unfollow
    if check == "follow":
        try:
            save_follow = Follows(
                following=User.objects.get(id=followed),
                followers=User.objects.get(id=follower)
            )
            save_follow.save()
            return JsonResponse({"message": "User successfully followed."}, status=201)
        except:
            return JsonResponse({"error": "User already followed."}, status=400)
    elif check == "unfollow":
        try:
            remove = Follows.objects.filter(followers_id=follower).filter(following_id=followed)
            remove.delete()
            return JsonResponse({"message": "User successfully unfollowed."}, status=201)
        except:
            return JsonResponse({"error": "User not followed."}, status=400)
    else:
        return JsonResponse({"error": "Option error."}, status=400)

@csrf_exempt
def to_like(request):
    if request.method == "POST":
        data = json.loads(request.body)
        post = data.get('postid')
        userid = data.get('userid')

        # Remove like if user already liked the post
        check = Like.objects.filter(liker_id=userid).filter(postID_id=post)
        if check.exists():
            check.delete()
            new_total = Like.objects.filter(postID_id=post).count()
            return JsonResponse({"message": "Post successfully unliked.", "numlikes": new_total, "status":201})
        else:
            addlike = Like(
                liker_id = User.objects.filter(id=userid).values_list("id", flat=True).first(),
                postID_id = Post.objects.filter(id=post).values_list("id", flat=True).first()
            )
            addlike.save()
            new_total = Like.objects.filter(postID_id=post).count()
            return JsonResponse({"message": "Post successfully liked.", "numlikes": new_total,"status":201})
    else:
        return JsonResponse({"error": "method is not POST."}, status=400)
