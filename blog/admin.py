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
class ProfileAdmin(admin.ModelAdmin):
    model = Profile
    fields = '__all__'

#admin.site.register(User)
admin.site.register(Post)
admin.site.register(Profile)
admin.site.register(Category)
admin.site.register(PostLikes)
admin.site.register(PostViews)
admin.site.register(SubCategory)
admin.site.register(ContentToPost)