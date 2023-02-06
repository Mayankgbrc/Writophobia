
from django_filters import rest_framework as filters
from django_filters import Filter
from blog.models import Post, PostViews, Profile, PostLikes


class PostFilter(filters.FilterSet):
    category = Filter(method = 'category_filter')
    subcategory = Filter(method = 'subcategory_filter')
    class Meta:
        model = Post
        fields = ['category', 'subcategory']
    
    def category_filter(self, queryset, name, value):
        return queryset.filter(
            category__title = value
        )
    def subcategory_filter(self, queryset, name, value):
        return queryset.filter(
            subcategory__title = value
        )