from django.shortcuts import render
from blog.models import Post, PostViews, Profile, PostLikes, ContentToPost, Category, SubCategory
from django.http import HttpResponse
from django.db.models import F
from django.views import View
from blog.filter import PostFilter
from django.db.models import Case, When, Count
from blog.utils import get_image_url
from django.core.paginator import Paginator

class BlogSelectedView(View):
    main_queryset = Post.objects.filter(visible = True)
    queryset = Post.objects.filter(visible = True, visible_at_homepage = True)
    template_name = 'blog/blog_main.html'

    def get_categories_queryset(self):
        return Category.objects.filter(
            visible = True
        ).annotate(
            total_count = Count('post')
        )
    
    def get_subcategories_queryset(self):
        return SubCategory.objects.filter(
            visible = True
        ).order_by(
            '-priority'
        )

    def get_queryset(self, post_id):
        return self.main_queryset.filter(
            id = post_id
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
        final_list = self.queryset.filter(id__in=exclude_list).order_by(preserved)[0:10]
        
        return final_list

    def get(self, request, pk):
        obj = self.get_queryset(
            pk
        )
        if obj.count():
            post_obj = obj.first()
            if post_obj.code != request.GET.get('code', None):
                return HttpResponse("Password Protected")

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

            popular_posts = self.queryset.order_by('-views')[0:3]
            for each in popular_posts:
                each.image_url = get_image_url(each)

            latest_posts = self.queryset.order_by('-created_at')[0:3]
            for each in latest_posts:
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
                "popular_posts": popular_posts,
                "latest_posts": latest_posts,
                "categories": self.get_categories_queryset(),
                "subcategories": self.get_subcategories_queryset()
            }
            return render(
                request, 
                self.template_name, 
                context
            )
        return HttpResponse("Not Found")



class HomeView(View):
    queryset = Post.objects.filter(
        visible = True,
        visible_at_homepage = True
    )
    template_name = 'blog/home_main.html'
    filter_class = PostFilter

    def get_categories_queryset(self):
        return Category.objects.filter(
            visible = True
        ).annotate(
            total_count = Count('post')
        ).order_by(
            '-priority'
        )
    
    def get_subcategories_queryset(self):
        return SubCategory.objects.filter(
            visible = True
        ).order_by(
            '-priority'
        )
        #subcat_dict = {}
        #for each in _qs:
        #    if each.category.title not in subcat_dict:
        #        subcat_dict[each.category] = each
        #    else:
        #        subcat_dict[each.category].append(each)
        
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
        page_number = request.GET.get('page')
        searched = request.GET.get('search','').strip(" ")
        post_objects = self.get_queryset()
        paginator = Paginator(post_objects, 3)
        page_obj = paginator.get_page(page_number)
        for each in page_obj:
            each.image_url = get_image_url(each)

        params = ""
        for each in request.GET:
            if each != "page":
                params+= f'&{each}={request.GET[each]}'

        context = {
            "post_objects": page_obj,
            "page_range": range(1, page_obj.paginator.num_pages + 1),
            "params": params,
            "categories": self.get_categories_queryset(),
            "subcategories": self.get_subcategories_queryset(),
            "searched": searched
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