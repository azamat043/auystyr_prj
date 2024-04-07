import json

from django.shortcuts import render, redirect
import shortuuid
from rest_framework.views import APIView

from core.models import Post, Comment, BookExchangeRequest
from django.utils.text import slugify
from django.http import JsonResponse
from django.utils.timesince import timesince
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt


@login_required
def index(request):
    if not request.user.is_authenticated:
        return redirect("userauths:sign-in")
    posts = Post.objects.filter(active=True, visibility="Everyone").order_by('-id')

    my_posts = Post.objects.filter(user=request.user, active=True)

    context = {
        "posts": posts,
        "my_posts": my_posts
    }

    return render(request, "core/index.html", context)


@csrf_exempt
def create_post(request):
    if request.method == "POST":
        title = request.POST.get("post-caption")
        visibility = request.POST.get("visibility")
        image = request.FILES.get("post-thumbnail")

        print("title ===============", title)
        print("visibility ==========", visibility)
        print("image ===============", image)

        uuid_key = shortuuid.uuid()
        uniqueid = uuid_key[:4]

        if title and image:
            post = Post(
                title=title,
                image=image,
                visibility=visibility,
                user=request.user,
                slug=slugify(title) + "-" + str(uniqueid.lower())
            )

            post.save()

            return JsonResponse({"post" : {
                "title":post.title,
                "image":post.image.url,
                "full_name":post.user.profile.full_name,
                "profile_image":post.user.profile.image.url,
                "date": timesince(post.date),
                "id": post.id
            }})
        else:
            return JsonResponse({"error": "Image or title does not exists"})

    return JsonResponse({"data": "sent"})


def save_post(request):
    id = request.GET['id']
    post = Post.objects.get(id=id)
    user = request.user
    bool = False

    if user in post.likes.all():
        post.likes.remove(user)
        bool = False

    else:
        post.likes.add(user)
        bool = True

    data = {
        "bool": bool,
        "likes": post.likes.all().count()
    }

    return JsonResponse({"data": data})


def comment_on_post(request):
    id = request.GET['id']
    comment = request.GET['comment']
    post = Post.objects.get(id=id)
    comment_count = Comment.objects.filter(post=post).count()
    user = request.user

    new_comment = Comment.objects.create(
        post = post, 
        comment = comment,
        user = user,   
    )

    data = {
        "bool": True,
        "comment": new_comment.comment,
        "profile_image": new_comment.user.profile.image.url,
        "date": timesince(new_comment.date),
        "comment_id": new_comment.id,
        "post_id": new_comment.post.id,
        "comment_count": comment_count + int(1)

    }

    return JsonResponse({"data":data})


def like_comment(request):
    id = request.GET['id']
    comment = Comment.objects.get(id=id)
    user = request.user
    bool = False

    if user in comment.likes.all():
        comment.likes.remove(user)
        bool = False
    else:
        comment.likes.add(user)
        bool = True

    data = {
        "bool": bool,
        "likes": comment.likes.all().count()
    }

    return JsonResponse({"data": data})


def get_post_info(request, pk):
    post = Post.objects.get(id=pk)

    data = {
        "exchange_user_photo": post.user.get_photo(),
        "exchange_user_username": post.user.username,
        "exchange_user_post_image": post.image.url,
        "exchange_user_post_title": post.title,
        "exchange_user_post_author": post.author
    }

    return JsonResponse({"data": data})


def send_exchange_request(request):
    if request.method == "POST":
        data = json.loads(request.body)
        my_post = data['my_post']
        exchange_post = data['exchange_post']
        user = request.user

        BookExchangeRequest.objects.create(
            sender_post=Post.objects.get(id=int(my_post)),
            receiver_post=Post.objects.get(id=int(exchange_post)),
            sender=user,
            receiver=Post.objects.get(id=int(exchange_post)).user
        )

        return JsonResponse({"data": "Request sent!", "status": 200})
    else:
        return JsonResponse({"message": "No data", "status": 400})


def get_exchange_info(request, exchange_id):
    exchange = BookExchangeRequest.objects.get(id=exchange_id)

    data = {
        "sender_username": exchange.sender.username,
        "sender_photo": exchange.sender.get_photo(),
        "sender_post_image": exchange.sender_post.image.url,
        "sender_post_title": exchange.sender_post.title,
        "sender_post_author": exchange.sender_post.author,
        "receiver_username": exchange.receiver.username,
        "receiver_photo": exchange.receiver.get_photo(),
        "receiver_post_image": exchange.receiver_post.image.url,
        "receiver_post_title": exchange.receiver_post.title,
        "receiver_post_author": exchange.receiver_post.author,
        "current_status": exchange.status,
        "request_date": exchange.date_time.strftime("%Y-%m-%d"),
    }

    if exchange.sender == request.user:
        data["is_outgoing"] = True
    else:
        data["is_outgoing"] = False

    return JsonResponse({"data": data})


def change_status_exchange(request, exchange_id):
    if request.method == "POST":
        exchange = BookExchangeRequest.objects.get(id=exchange_id)
        data = json.loads(request.body)
        status = data['status']

        if status not in ["accepted", "rejected"]:
            return JsonResponse({"message": "Invalid status", "status": 400})

        exchange.status = status
        exchange.save()

        return JsonResponse({"data": "Status changed!", "status": 200})
    else:
        return JsonResponse({"message": "No data", "status": 400})