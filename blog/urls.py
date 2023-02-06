from django.urls import path, include
from blog.views import BlogSelectedView, HomeView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('view/<int:pk>/', BlogSelectedView.as_view(), name='blog-detail'),
]
