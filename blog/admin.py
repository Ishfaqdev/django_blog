from django.contrib import admin
from . models import Post, Category
# Register your models here.


admin.site.register(Category)


@admin.register(Post)
class UserAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "author", "views", "date_posted")
