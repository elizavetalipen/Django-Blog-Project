from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.utils import timezone
from django.shortcuts import redirect
from .models import Post, Cathegory, UserInfo, Post_Cathegory, Post_Tag, Tag, Comment
from .forms import PostForm, NewUserForm, UserProfileEditForm
from .forms import ChangePasswordForm, UserEditForm, LoginForm, CommentForm
from django.http import JsonResponse


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
    tags = post.post_tag.all()
    post_comments = Comment.objects.filter(post=post)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.user = request.user
        comment.save()
        form = CommentForm()
    return render(request, 'blogposts/post.html', {'post': post, 'tags': tags, 
                                                   'comments':post_comments,'form':form})


# написать новый пост
def newpost_view(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.published = timezone.now()
            post.save()
            # связываем этот пост с категорией
            cat = form.cleaned_data['category']
            post_cat = Post_Cathegory(post=post, cathegory_id=cat.id)
            post_cat.save()

            # парсим теги из ввода пользователя
            tags = form.cleaned_data['tags']
            tag_list = tags.split(',')
            
            for tag_title in tag_list:
                tag_title = tag_title.strip()
                if tag_title:
                    tag, created = Tag.objects.get_or_create(title=tag_title)
                    post_tag = Post_Tag(post=post, tag=tag)
                    post_tag.save()
            return redirect('post', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blogposts/post_add.html', {'form': form})


#редактировать пост
def edit_post_view(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            # категория
            category = form.cleaned_data['category']
            post_category, created = Post_Cathegory.objects.get_or_create(post=post)
            post_category.category = category
            post_category.save()
            # добавим новые теги к существующим и удалим те, которые убрали
            tags = form.cleaned_data['tags']
            tag_list = tags.split(',')
            post_tags = []
            for tag_title in tag_list:
                tag_title = tag_title.strip()
                if tag_title:
                    tag, created = Tag.objects.get_or_create(title=tag_title)
                    post_tag, created = Post_Tag.objects.get_or_create(post=post, tag=tag)
                    post_tags.append(post_tag)
            post.post_tag.exclude(id__in=[tag.id for tag in post_tags]).delete()
            return redirect('post', pk=post.pk)
    else: 
        # предварительно заполняем поля категории и тегов 
        post_cat = Post_Cathegory.objects.filter(post=post).first()
        initial_cat = post_cat.cathegory if post_cat else None
        post_tags = Post_Tag.objects.filter(post=post)
        initial_tags = [post_tag.tag.title for post_tag in post_tags]
        initial_data = {'category': initial_cat, 'tags': ','.join(initial_tags)}
        form = PostForm(instance=post, initial=initial_data)
    return render(request, 'blogposts/post_edit.html', {'form': form})


def delete_post_view(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('profile')


@login_required
def delete_comment_view(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post_pk = comment.post.pk
    comment.delete()
    return redirect('post', pk=post_pk)


@login_required
def edit_comment_view(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post_pk = comment.post.pk
    if comment.user == request.user:
        if request.method == 'POST':
            form = CommentForm(request.POST, instance=comment)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.edited = timezone.now()
                comment.save()
                return redirect('post', pk=post_pk)
        else:
            form = CommentForm(instance=comment)
    return render(request, 'blogposts/edit_comment.html', {'form': form, 'comment': comment})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
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
def user_profile_view(request, pk):
    user_info = get_object_or_404(UserInfo, user__pk=pk)
    user_posts = Post.objects.filter(user=user_info.user)
    return render(request, 'profile/user_profile.html', {'user_info': user_info,'user_posts': user_posts})


@login_required
def edit_profile_view(request):
    if request.method == 'POST':
        account_form =  UserEditForm(request.POST, instance=request.user)
        profile_form =  UserProfileEditForm(request.POST, request.FILES, instance=request.user.userinfo)
        if account_form.is_valid() and profile_form.is_valid():
            profile_form.save()
            account_form.save()
            return redirect('profile', pk=request.user.pk)
    else:
        profile_form = UserProfileEditForm(instance=request.user.userinfo)
        account_form = UserEditForm(instance=request.user)
    return render(request, 'profile/edit_profile.html', {'profile_form': profile_form, 
                                                         'account_form': account_form})


@login_required
def change_password_view(request):
    if request.method == 'POST':
        form = ChangePasswordForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('profile', pk=request.user.pk)
    else:
        form = ChangePasswordForm(request.user)
    return render(request, 'profile/change_password.html', {'form': form})


def delete_profile_view(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        user = authenticate(username=request.user.username, password=password)
        if user is not None:
            user.delete()
            return redirect('home')
    return render(request, 'profile/delete_profile.html')


def cathegory_view(request, pk):
    cathegory = get_object_or_404(Cathegory, pk=pk)
    posts = Post.objects.filter(post_cathegory__cathegory=cathegory).order_by('published')
    return render(request, 'cathegories.html', {'cathegory': cathegory, 'posts':posts})
