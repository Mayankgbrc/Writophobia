from django.urls import path, include
from blog.views import home

urlpatterns = [
    path('admin/', home),
]
