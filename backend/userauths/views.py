from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

import core.views
from core.models import Post
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


    context = {
        "profile": profile,
        "posts": posts,

    }

    template_name = "userauths/my_profile.html"

    return render(request, template_name, context)














# def validate_username(request):
#     username = request.GET.get('username', None)
#     data = {
#         'is_taken': Profile.objects.filter(username__iexact=username).exists()
#     }
#     print(data)
#     return JsonResponse(data)



# @login_required
# def profile(request, username=None):
#     report_form = ReportUserForm()
#     user = get_object_or_404(User, username=username)
#     post_list = Post.objects.filter(author=user).order_by('-id')
#     post_count = post_list.count()
#     page = request.GET.get('page', 1)
#     paginator = Paginator(post_list, 4)
#     try:
#         posts = paginator.page(page)
#     except PageNotAnInteger:
#         posts = paginator.page(1)
#     except EmptyPage:
#         posts = paginator.page(paginator.num_pages)
#
#     context = {
#         'report_form': report_form,
#         'posts': posts,
#         'user_id': user,
#         'post_count': post_count,
#     }
#     template_name = 'users/profile.html'
#
#     return render(request, template_name, context)
