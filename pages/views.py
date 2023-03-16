from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.shortcuts import redirect
from .models import Post, Cathegory, UserInfo
from .forms import NewPostForm, NewUserForm, UserProfileEditForm, UserEditForm, LoginForm


def home_view(request):
    cathegories = Cathegory.objects.all()
    return render(request, 'index.html', {'cathegories':cathegories})


# список всех постов
def all_posts_view(request):
    posts = Post.objects.order_by("published")
    return render(request, 'blogposts/all_posts.html', {'posts': posts})


# читать пост полностью
def post_view(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blogposts/post.html', {'post': post})

# написать новый пост
def newpost_view(request):
    if request.method == "POST":
        form = NewPostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.published = timezone.now()
            post.save()
            return redirect('post', pk=post.pk)
    else:
        form = NewPostForm()
    return render(request, 'blogposts/post_add.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = LoginForm()
    return render(request, 'registration/login.html', {'form': form})


def register_view(request):
    if request.method == 'POST':
        form = NewUserForm(request.POST)
        if form.is_valid():
            form.save()
            uname = form.cleaned_data['username']
            psw = form.cleaned_data['password1']
            user = authenticate(username=uname, password=psw)
            if user is not None:
                login(request, user)
                # по умолчанию создадется пустой профиль
                profile = UserInfo.objects.create(user=user, avatar_image='images/userimg/blank_img.png', 
                                                  cover_image='images/userimg/blank_cover.jpg',bio='...',)
                return redirect('/')
        else:
            print(form.errors)
    else:
        form = NewUserForm()
    return render(request, "registration/register.html", {"register_form":form})


def logout_view(request):
	logout(request)
	return redirect("home")


@login_required
def user_profile_view(request):
    user_info = UserInfo.objects.get(user=request.user)
    user_posts = Post.objects.filter(user=request.user)
    return render(request, 'profile/user_profile.html', {'user_info': user_info,'user_posts': user_posts})


@login_required
def edit_profile_view(request):
    if request.method == 'POST':
        account_form =  UserEditForm(request.POST, instance=request.user)
        profile_form =  UserProfileEditForm(request.POST, request.FILES, instance=request.user.userinfo)
        if profile_form.is_valid() and account_form.is_valid():
            profile_form.save()
            account_form.save()
            return redirect('profile')
    else:
        profile_form = UserProfileEditForm(instance=request.user.userinfo)
        account_form = UserEditForm(instance=request.user)
    return render(request, 'profile/edit_profile.html', {'profile_form': profile_form, 
                                                         'account_form': account_form})


def cathegory_view(request, pk):
    posts = Post.objects.order_by('published')
    cathegory = get_object_or_404(Cathegory, pk=pk)
    return render(request, 'cathegories.html', {'cathegory': cathegory, 'posts':posts})
