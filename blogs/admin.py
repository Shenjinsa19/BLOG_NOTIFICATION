from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Post, Follow

admin.site.register(Post)
admin.site.register(Follow)
