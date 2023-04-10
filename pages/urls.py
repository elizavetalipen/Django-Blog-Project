from django.urls import path
from .views import *


urlpatterns = [
    path('', home_view, name='home'),
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    # профиль (личный кабинет)
    path('profile/<int:pk>/', user_profile_view, name='profile'),
    path('profile/edit/', edit_profile_view, name='edit_profile'),
    path('profile/delete/', delete_profile_view, name='delete_profile'),
    path('profile/change_password/', change_password_view, name='change_password'),
    # список всех постов
    path('all_posts/', all_posts_view, name='all_posts'),
    # читать пост полностью
    path('post/<int:pk>/', post_view, name='post'),
    path('post/<int:pk>/like/', like_view, name='like'),
    # форма добавления поста (добавить стили и категорию, теги)
    path('post/new/', newpost_view, name='newpost'),
    # форма редактирования поста
    path('post/<int:pk>/edit/', edit_post_view, name='edit_post'),
    path('post/<int:pk>/delete/', delete_post_view, name='delete_post'),
    # страница категории
    path('cathegory/<int:pk>/', cathegory_view, name='cathegory'),
    path('comment/<int:pk>/delete/', delete_comment_view, name='delete_comment'),
    path('comment/<int:pk>/edit/', edit_comment_view, name='edit_comment'),
]