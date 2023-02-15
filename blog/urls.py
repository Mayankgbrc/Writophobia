from django.urls import path, include
from blog.views import BlogSelectedView, HomeView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('view/<str:pk>/', BlogSelectedView.as_view(), name='blog-detail'),
]
