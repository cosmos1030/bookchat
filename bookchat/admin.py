from django.contrib import admin

from .models import Book, Chat, UserProfile

# Register your models here.
admin.site.register(Book)
admin.site.register(Chat)
admin.site.register(UserProfile)