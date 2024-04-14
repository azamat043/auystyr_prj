from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

import core.views
from core.models import Post, BookExchangeRequest
from userauths.models import Profile, User
from userauths.forms import UserRegisterForm

from .forms import UserRegisterForm
from django.contrib.auth.decorators import login_required


@csrf_exempt
def RegisterView(request):
    if request.user.is_authenticated:
        messages.warning(request, f"Hey {request.user.username}, you are already logged in")
        return redirect('core:feed')
     
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        gender = request.POST.get('gender')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password == confirm_password:
            user = User.objects.create_user(email=email, password=password, username=username, phone=phone, gender=gender)
            user.save()

            auth = authenticate(request, email=email, password=confirm_password)
            login(request, auth)

            profile = Profile.objects.get(user=request.user)
            profile.full_name = full_name
            profile.phone = phone
            profile.gender = gender
            profile.save()

            messages.success(request, f'Account Created for {full_name}! You can now login')
            return redirect('core:feed')

        messages.error(request, 'Password does not match')
        return redirect("userauths:sign-up")

    template_name = "userauths/sign-up.html"

    return render(request, template_name)


@csrf_exempt
def LoginView(request):
    if request.user.is_authenticated:
        messages.warning(request, "You are already registered!")
        return redirect("core:feed")
    
    if request.method == "POST":
        email = request.POST.get('login_email')
        password = request.POST.get('login_password')

        try:
            user = User.objects.get(email=email)

            user = authenticate(request, email=email, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, "You are Logged In")
                return redirect('core:feed')
            else:
                messages.error(request, 'Username or password does not exit.')
        
        except:
            messages.error(request, 'User does not exist')
            return redirect("userauths:sign-up")

    return HttpResponseRedirect("/")


@csrf_exempt
def LogoutView(request):
    logout(request)
    messages.success(request, "You are logged in!")
    return redirect("userauths:sign-up")


@login_required
def my_profile(request):
    profile = request.user.profile
    posts = Post.objects.filter(active=True, user=request.user)
    count_exchange = BookExchangeRequest.objects.filter(sender=request.user).count()

    context = {
        "profile": profile,
        "posts": posts,
        "count_exchange": count_exchange
    }

    template_name = "userauths/my_profile.html"

    return render(request, template_name, context)


@csrf_exempt
def settings(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        birthday = request.POST.get('birthday')
        speciality = request.POST.get('speciality')
        course = request.POST.get('course')
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        user = request.user
        profile = Profile.objects.get(user=user)

        user.first_name = first_name if first_name else user.first_name
        user.last_name = last_name if last_name else user.last_name
        user.full_name = first_name + " " + last_name if first_name and last_name else user.full_name
        user.username = username if username else user.username
        user.email = email if email else user.email
        user.save()

        profile.full_name = first_name + " " + last_name if first_name and last_name else profile.full_name
        profile.birthday = birthday if birthday else profile.birthday
        profile.speciality = speciality if speciality else profile.speciality
        profile.course = course if course else profile.course
        profile.save()

        print("birthday:", birthday)

    return render(request, "userauths/settings.html")


@csrf_exempt
def change_password(request):
    if request.method == "POST":
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        user = request.user

        if user.check_password(current_password):
            if new_password == confirm_password:
                user.set_password(new_password)
                user.save()
                messages.success(request, "Password changed successfully")

                user = authenticate(request, email=user.email, password=new_password)
                login(request, user)

                return redirect("userauths:settings")
            messages.error(request, "Password does not match")
            return redirect("userauths:settings")
        messages.error(request, "Current Password does not match")
        return redirect("userauths:settings")

    return render(request, "userauths/settings.html")
