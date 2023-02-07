from django.contrib import admin
from blog.models import (
    Profile, 
    Post, 
    PostLikes, 
    PostViews, 
    Category, 
    ContentToPost, 
    SubCategory
)
from django.contrib.auth.models import User

# Register your models here.
class ContentToPostAdmin(admin.ModelAdmin):
    model = ContentToPost
    list_display = ('post', 'content_type', 'editor_type', 'priority')

class PostAdmin(admin.ModelAdmin):
    model = Post
    list_display = ('title', 'category', 'subcategory', 'thumbnail')

class SubCategoryAdmin(admin.ModelAdmin):
    model = SubCategory
    list_display = ('title', 'category', 'thumbnail')

class CategoryAdmin(admin.ModelAdmin):
    model = Category
    list_display = ('title', 'thumbnail')

#admin.site.register(User)
admin.site.register(Post, PostAdmin)
admin.site.register(Profile)
admin.site.register(Category, CategoryAdmin)
admin.site.register(PostLikes)
admin.site.register(PostViews)
admin.site.register(SubCategory, SubCategoryAdmin)
admin.site.register(ContentToPost, ContentToPostAdmin)