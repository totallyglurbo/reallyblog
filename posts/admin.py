from django.contrib import admin
from .models import Post, ReallyUser, Comment

admin.site.register(ReallyUser)
admin.site.register(Post)
admin.site.register(Comment)

