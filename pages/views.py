from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.utils import timezone
from django.shortcuts import redirect
from .models import Post, Cathegory
from .forms import NewPostForm, NewUserForm


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
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'login_form': form})


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
                return redirect('/')
        else:
            print(form.errors)
    else:
        form = NewUserForm()
    return render(request, "registration/register.html", {"register_form":form})


def logout_view(request):
	logout(request)
	messages.info(request, "You have logged out") 
	return redirect("home")


def my_profile_view(request):
    return render(request, 'userprofile/my_profile.html')

'''def edit_profile_view(request):
    return render(request, 'edit_profile.html')

def text_editor_view(request):
    return render(request, 'text_editor.html')'''

def cathegory_view(request, pk):
    posts = Post.objects.order_by('published')
    cathegory = get_object_or_404(Cathegory, pk=pk)
    return render(request, 'cathegories.html', {'cathegory': cathegory, 'posts':posts})
