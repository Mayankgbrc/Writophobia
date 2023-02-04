
from django_filters import rest_framework as filters
from django_filters import Filter
from blog.models import Post, PostViews, Profile, PostLikes


class PostFilter(filters.FilterSet):
    class Meta:
        model = Post
        fields = ['category', 'subcategory']