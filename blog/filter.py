
from django_filters import rest_framework as filters
from django_filters import Filter
from blog.models import Post, PostViews, Profile, PostLikes


class PostFilter(filters.FilterSet):
    visible = Filter(method = 'visible_filter')

    class Meta:
        model = Post
        fields = ['category', 'subcategory']
    
    def visible_filter(self, queryset):
        return queryset.filter(
            visible = True
        )