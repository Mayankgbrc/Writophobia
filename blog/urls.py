from django.urls import path, include
from blog.views import BlogDetailView, BlogSelectedView

urlpatterns = [
    path('view/<int:pk>/', BlogSelectedView.as_view(), name='blog-detail'),
]
