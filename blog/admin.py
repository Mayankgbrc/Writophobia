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
    list_display = ('title', 'category', 'subcategory')

#admin.site.register(User)
admin.site.register(Post, PostAdmin)
admin.site.register(Profile)
admin.site.register(Category)
admin.site.register(PostLikes)
admin.site.register(PostViews)
admin.site.register(SubCategory)
admin.site.register(ContentToPost, ContentToPostAdmin)