from django.db import models
from django.contrib.auth.models import User
from tinymce.models import HTMLField

class Profile(User):
    user_type = models.CharField(max_length=20)
    description = models.TextField(blank=True, null=True)
    picture = models.ImageField(upload_to='user/picture', blank=True, null=True)
    visible = models.BooleanField(default=True)
    verified = models.BooleanField(default=False)
    is_blacklisted = models.BooleanField(default=False)
    facebook_url = models.CharField(max_length=100, blank=True, null=True)
    youtube_url = models.CharField(max_length=100, blank=True, null=True)
    twitter_url = models.CharField(max_length=100, blank=True, null=True)
    linkedin_url = models.CharField(max_length=100, blank=True, null=True)
    instagram_url = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Category(models.Model):
    title = models.CharField(max_length=50)
    thumbnail = models.ImageField(upload_to='category/thumbnail', blank=True, null=True)
    visible = models.BooleanField(default=True)
    priority = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.title


class SubCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    thumbnail = models.ImageField(upload_to='subcategory/thumbnail', blank=True, null=True)
    visible = models.BooleanField(default=True)
    priority = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.title


class Post(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    tags = models.TextField(blank=True, null=True, help_text="Add tags comma separated without space")
    views = models.IntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    thumbnail = models.ImageField(upload_to='post/thumbnail', blank=True, null=True)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, blank=True, null=True)
    visible = models.BooleanField(default=True)
    visible_at_homepage = models.BooleanField(default=False)
    code = models.CharField(max_length=50, blank=True, null=True)
    priority = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.title
    # Multieditor reference link: https://blog.devgenius.io/best-free-wysiwyg-editor-python-django-admin-panel-integration-d9cb30da1dba


class ContentToPost(models.Model): 
    post = models.ForeignKey(Post, on_delete=models.CASCADE, blank=True, null=True)
    image = models.ImageField(upload_to='post/image', blank=True, null=True)
    content = models.TextField(blank=True, null=True, help_text="If image has been chosen, this field will work as image description")
    content_type = models.CharField(max_length=64, blank=True, null=True, default = "text")
    editor_type = models.CharField(max_length=64, blank=True, null=True) 
    priority = models.IntegerField(default=1, help_text="Here priority in ascending order like 1 will appear on top")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class PostLikes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    like_type = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class PostViews(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)