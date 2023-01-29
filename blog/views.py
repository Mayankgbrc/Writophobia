from django.shortcuts import render
from blog.models import Post, PostViews, Profile, PostLikes
from django.http import HttpResponse
from django.db.models import F
from django.views import View
from blog.filter import PostFilter

# Create your views here.
def home(request):
    return render(request, 'home.html')

class BlogSelectedView(View):
    queryset = Post.objects.all()
    template_name = 'home.html'

    def get_queryset(self, post_id):
        return self.queryset.filter(
            id = post_id,
            visible = True
        )

    def get(self, request, post_id):
        obj = self.get_queryset(
            post_id
        )
        if obj.count():
            post_obj = obj.first()
            post_obj.update(
                views = F('views') + 1
            )
            
            if request.user.is_authenticated:
                PostViews.objects.create(
                    user = request.user,
                    post = post_obj
                )
            
            context = {
                "post_obj": post_obj
            }
            return render(
                request, 
                self.template_name, 
                context
            )
        return HttpResponse("Not Found")



class BlogDetailView(View):
    queryset = Post.objects.all()
    template_name = 'home.html'
    filter_class = PostFilter

    def get_queryset(self):
        return self.filter_class(
            self.request.GET, 
            self.queryset
        ).qs.order_by(
            '-priority',
            '-views',
            '-id',
        )
        

    def get(self, request):
        obj = self.get_queryset()
        context = {
            "post_obj": obj
        }
        return render(
            request, 
            self.template_name, 
            context
        )

from django.shortcuts import get_object_or_404

class BlogLikeView(View):
    queryset = Post.objects.all()

    def get_queryset(self):
        return get_object_or_404(
            self.queryset, 
            self.request.query_params.get('post_id')
        )
        

    def post(self, request):
        post_obj = self.get_queryset()
        obj, created = PostLikes.objects.get_or_create(
            post = post_obj, 
            user = request.user
        ) 
        if not created:
            obj.delete()
        return HttpResponse({'status': 200, "created": created})