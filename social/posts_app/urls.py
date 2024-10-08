from django.urls import path
from rest_framework import routers
from .views import PostListView
from .views import PostDetailView, UserListView, CommentListView
from . import views



urlpatterns = [
    path('api/posts/', PostListView.as_view(), name='post-list'),
    path('api/register/', views.create_user, name='create_user'),
    path('api/login/', views.login_user, name='login_user'),
    path('api/users/', UserListView.as_view(), name='user-list'),
    path('api/user/<int:pk>/', views.get_user_by_key, name='user'),
    path('api/user/', views.get_authenticated_user, name='get_authenticated_user'),
    path('api/posts/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('api/posts/user/<int:pk>/', views.get_posts_by_user, name='post_by_user'),
    path('api/comment/', views.create_comment, name='make_comment'),
    path('api/comments/', CommentListView.as_view(), name='get_comments'),
    path('api/comments/<int:pk>/', views.get_comments_by_post, name='get_comments'),
    path('api/likes/comment/<int:pk>/', views.update_comment_likes, name='update_comments'),
    path('api/likes/post/<int:pk>/', views.update_post_likes, name='update_posts'),
    path('api/followers/', views.get_followers, name='followers'),
    path('api/following/', views.get_following, name='following'),
    path('api/follow/<int:pk>/', views.follow_user, name='follow'),
    path('api/unfollow/<int:pk>/', views.unfollow_user, name='unfollow'),
    path('api/delete/user/<int:pk>', views.delete_user, name='delete_user'),
    path('api/delete/post/<int:pk>', views.delete_post, name='delete_post'),
    path('api/delete/comment/<int:pk>', views.delete_comment, name='delete_comment'),
    path('api/caption/<int:pk>/', views.update_caption, name='caption'), 

]