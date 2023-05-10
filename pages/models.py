from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import User 
from cloudinary.models import CloudinaryField
    
# информация для отображения в профиле
class UserInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    #avatar_image = models.ImageField(upload_to='images/userimg', blank=True)
    #cover_image = models.ImageField(upload_to='images/userimg', blank=True)
    avatar_image = CloudinaryField("avatar", blank=True)
    cover_image = CloudinaryField("cover", blank=True)
    bio = models.CharField(max_length=500)


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField()
    #post_image = models.ImageField(upload_to=f'images/postimg/', blank=True)
    post_image = CloudinaryField("post_image", blank=True)
    published = models.DateTimeField(default=timezone.now)
    edited = models.DateTimeField(blank=True, null=True)
    likes = models.IntegerField(default=0) 

    def __str__(self):
        return self.title


class Cathegory(models.Model):
    title = models.CharField(max_length=50)
    description =  models.TextField()
    #cathegory_image = models.ImageField(upload_to='images')
    cathegory_image = CloudinaryField("cath_image", blank=True)

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



