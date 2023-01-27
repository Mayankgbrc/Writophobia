from django.urls import path, include
from blog.views import home, BlogDetailView

urlpatterns = [
    path('admin/', home),
    path('view/<int:pk>/', BlogDetailView.as_view(), name='blog-detail'),
]
