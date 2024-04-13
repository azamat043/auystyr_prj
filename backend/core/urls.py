from django.urls import path
from core import views

app_name = "core"

urlpatterns = [
    path("", views.index, name="feed"),
    path("create_post/", views.create_post, name="create_post"),
    path("save_post/", views.save_post, name="save_post"), 
    path("comment_post/", views.comment_on_post, name="comment_post"),
    path("like_comment/", views.like_comment, name="like_comment"),
    path("search_post", views.search_post, name="search_post"),

    path("get_post_info/<int:pk>", views.get_post_info, name="exchange_request"),
    path("send_exchange_request", views.send_exchange_request, name="send_exchange_request"),

    path('get_exchange_info/<int:exchange_id>', views.get_exchange_info, name='get_exchange_info'),
    path('change_status_exchange/<int:exchange_id>', views.change_status_exchange, name='change_status_exchange'),
]

