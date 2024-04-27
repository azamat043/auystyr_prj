from django.urls import path
from userauths import views

app_name = 'userauths'

urlpatterns = [
    path("sign-up/", views.RegisterView, name="sign-up"),
    path("sign-in/", views.LoginView, name="sign-in"),
    path("sign-out/", views.LogoutView, name="sign-out"),
    path("my-profile/", views.my_profile, name="my-profile"),
    path('settings', views.settings, name='settings'),
    path('change_password', views.change_password, name='change_password'),
<<<<<<< HEAD
=======

    path('upload_image', views.upload_image, name='upload_image'),
    path('upload_cover_image', views.upload_cover_image, name='upload_cover_image'),
    path('delete_image', views.delete_image, name='delete_image'),
>>>>>>> d6be1699d7337e7f3e743afbf9877a22324f4ce1
]
