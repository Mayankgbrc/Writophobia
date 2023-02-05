from django.shortcuts import render
from blog.models import Post, PostViews, Profile, PostLikes, ContentToPost, Category, SubCategory
from django.http import HttpResponse
from django.db.models import F
from django.views import View
from blog.filter import PostFilter
from django.db.models import Case, When, Count
from blog.utils import get_image_url

# Create your views here.
def home(request):
    return render(request, 'home.html')

class BlogSelectedView(View):
    queryset = Post.objects.filter(visible = True)
    template_name = 'home.html'

    def get_queryset(self, post_id):
        return self.queryset.filter(
            id = post_id,
            visible = True
        )

    def get_categories_queryset(self):
        return Category.objects.filter(
            visible = True
        ).annotate(
            total_count = Count('post')
        )

    def get_suggested_queryset(self, post_obj):
        exclude_list = [post_obj.id]

        _qs1 = self.queryset.filter(
            subcategory = post_obj.subcategory,
            category = post_obj.category
        ).exclude(
            id = post_obj.id
        ).order_by(
            '-priority',
            '-created_at'
        ).values_list(
            'id', 
            flat = True
        )
        exclude_list.extend(_qs1)

        if len(exclude_list) < 10:
            _qs2 = self.queryset.filter(
                category = post_obj.category
            ).exclude(
                id__in = exclude_list
            ).order_by(
                '-priority',
                '-created_at'
            ).values_list(
                'id', 
                flat = True
            )
            exclude_list.extend(_qs2)
            
            if len(exclude_list) < 10:
                _qs3 = self.queryset.exclude(
                    id__in = exclude_list
                ).order_by(
                    '-priority',
                    '-created_at'
                ).values_list(
                    'id', 
                    flat = True
                )
                exclude_list.extend(_qs3)
        
        exclude_list = exclude_list[1:]
        preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(exclude_list)])
        final_list = self.queryset.filter(id__in=exclude_list).order_by(preserved)
        
        return final_list

    def get(self, request, pk):
        obj = self.get_queryset(
            pk
        )
        if obj.count():
            categories = self.get_categories_queryset()
            post_obj = obj.first()
            post_obj.views += 1
            post_obj.save()

            post_obj.contents = ContentToPost.objects.filter(
                post__id = pk
            ).order_by(
                'priority',
                'created_at',
                'updated_at',
                'id'
            )


            suggestions = self.get_suggested_queryset(
                post_obj
            )[:10]
            
            for each in suggestions:
                each.image_url = get_image_url(each)
            
            post_obj.image_url = get_image_url(post_obj)


            if request.user.is_authenticated:
                PostViews.objects.create(
                    user = request.user,
                    post = post_obj
                )
            
            context = {
                "post_obj": post_obj,
                "suggestions": suggestions,
                "categories": categories
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