from django.contrib import admin
from blog.models import (
    Profile, 
    Post, 
    PostLikes, 
    PostViews, 
    Category, 
    ContentToPost, 
    SubCategory,
    TrackHits
)
from django.contrib.auth.models import User

# Register your models here.
class ContentToPostAdmin(admin.ModelAdmin):
    model = ContentToPost
    list_display = ('post', 'short_description', 'content_type', 'editor_type', 'priority')

class PostAdmin(admin.ModelAdmin):
    model = Post
    list_display = ('title', 'category', 'subcategory', 'thumbnail', 'author')

class SubCategoryAdmin(admin.ModelAdmin):
    model = SubCategory
    list_display = ('title', 'category', 'thumbnail')

class CategoryAdmin(admin.ModelAdmin):
    model = Category
    list_display = ('title', 'thumbnail')
    
class TrackHitsAdmin(admin.ModelAdmin):
    model = TrackHits
    list_display = ('user', 'city', 'country', 'ip_address', 'requested_url', 'page_title', 'successful', 'created_at')

#admin.site.register(User)
admin.site.register(Post, PostAdmin)
admin.site.register(Profile)
admin.site.register(Category, CategoryAdmin)
admin.site.register(PostLikes)
admin.site.register(PostViews)
admin.site.register(SubCategory, SubCategoryAdmin)
admin.site.register(ContentToPost, ContentToPostAdmin)
admin.site.register(TrackHits, TrackHitsAdmin)