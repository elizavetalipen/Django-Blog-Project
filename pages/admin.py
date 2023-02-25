from django.contrib import admin
from .models import Post, UserInfo, Cathegory
from .models import Post_Cathegory, Tag, Post_Tag, Comment


admin.site.register(Post)
admin.site.register(Cathegory)
admin.site.register(UserInfo)
admin.site.register(Comment)
admin.site.register(Tag)
admin.site.register(Post_Tag)
admin.site.register(Post_Cathegory)
