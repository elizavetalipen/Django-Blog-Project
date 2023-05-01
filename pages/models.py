from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import User 
    
# информация для отображения в профиле
class UserInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar_image = models.ImageField(upload_to='images/userimg', blank=True)
    cover_image = models.ImageField(upload_to='images/userimg', blank=True)
    bio = models.CharField(max_length=500)


class Post(models.Model):
    # author id
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField()
    post_image = models.ImageField(upload_to=f'images/postimg/', blank=True)
    published = models.DateTimeField(default=timezone.now)
    edited = models.DateTimeField(blank=True, null=True)
    likes = models.IntegerField(default=0)  # add this field to track likes

    def __str__(self):
        return self.title

    def update_edited_date(self):
        self.edited = timezone.now()
        self.save()


class Cathegory(models.Model):
    title = models.CharField(max_length=50)
    description =  models.TextField()
    cathegory_image = models.ImageField(upload_to='images')

    def __str__(self):
        return self.title


class Post_Cathegory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_cathegory')
    cathegory = models.ForeignKey(Cathegory, on_delete=models.CASCADE)


class Tag(models.Model):
    title = models.CharField(max_length=50)
    def __str__(self):
        return self.title


class Post_Tag(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE,  related_name='post_tag')
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    published = models.DateTimeField(default=timezone.now)
    edited = models.DateTimeField(blank=True, null=True)


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'post')



