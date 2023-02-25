from django.urls import path
from .views import *


urlpatterns = [
    path('', home_view, name='home'),
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    #path('profile/', my_profile_view, name='my_profile'),
    # список всех постов
    path('all_posts/', all_posts_view, name='all_posts'),
    # читать пост полностью
    path('post/<int:pk>/', post_view, name='post'),
    # форма добавления поста (добавить стили и категорию, теги)
    path('post/new/', newpost_view, name='newpost'),
    # форма редактирования поста
    #path('post/<int:pk>/edit/', editpost_view, name='editpost'),
    # страница категории
    path('cathegory/<int:pk>/', cathegory_view, name='cathegory'),
]