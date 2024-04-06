from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
import core.views
from core.models import Post
from userauths.models import Profile, User
from userauths.forms import UserRegisterForm

from .forms import UserRegisterForm
from django.contrib.auth.decorators import login_required


def RegisterView(request):
    if request.user.is_authenticated:
        messages.warning(request, f"Hey {request.user.username}, you are already logged in")
        return redirect('core:feed')
     
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            full_name = form.cleaned_data.get('full_name')
            phone = form.cleaned_data.get('phone')

            profile = Profile.objects.get(user=request.user)
            profile.full_name = full_name        
            profile.phone = phone

            profile.save()
            messages.success(request, f'Account Created for {full_name}! You can now login')

            return redirect('core:feed')
    else:
        form = UserRegisterForm()
    context = {'form': form}
    template_name = "userauths/sign-up.html"

    return render(request, template_name, context)



def LoginView(request):
    if request.user.is_authenticated:
        messages.warning(request, "You are already registered!")
        return redirect("core:feed")
    
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

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
