from django.contrib import admin
from . models import Post, Category, UserProfile
# Register your models here.


admin.site.register(Category)
admin.site.register(UserProfile)


@admin.register(Post)
class UserAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "author", "views", "date_posted")
