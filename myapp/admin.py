from django.contrib import admin
from .models import Author, NewsStory


# Register your models here.
from .models import Post

admin.site.register(Post)
admin.site.register(Author)
admin.site.register(NewsStory)