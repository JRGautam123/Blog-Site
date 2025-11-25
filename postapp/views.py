from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .froms import PostForm
from .models import Category,Like,Comments,Post
from django.utils.text import slugify
from django.db.models import Q
from django.core.paginator import Paginator
from django.http import JsonResponse
import json
from django.contrib.auth.models import User
from django.utils.timesince import timesince

# Create your views here.


def render_home_page(request):
    latest_post=Post.objects.all().order_by("-date")[:3]
    return render(request=request,template_name='postapp/home_page.html',context={'posts':latest_post})


def render_article_page(request):
    categories=Category.objects.all()
    title_query=request.GET.get("title","")
    category_query=request.GET.get("category","")

    if title_query or category_query:
        all_posts=Post.objects.all()
        if title_query and category_query:
            posts=all_posts.filter(
                Q(title__icontains=title_query),
                Q(category__name__iexact=category_query)
            )
        elif title_query:
            posts=all_posts.filter(title__icontains=title_query)
        elif category_query:
            posts=all_posts.filter(category__name__iexact=category_query)
    else:
        posts=Post.objects.order_by('-date')[:5]

    paginator=Paginator(posts,3)
    page_number=request.GET.get('page')
    post_objs=paginator.get_page(page_number)

    context={
        "categories":categories,
        "posts":post_objs
    }

    return render(request=request,template_name='postapp/articles.html',context=context)




def render_full_article(request,slug):
    requested_post=Post.objects.get(slug=slug)
    like_count=Like.objects.filter(post=requested_post).count()
    user_has_liked=False
    if request.user.is_authenticated:
        user_has_liked=Like.objects.filter(user=request.user,post=requested_post).exists()

    parent_comments=Comments.objects.filter(post=requested_post,parent_id__isnull=True ).order_by('-date')


    descendents_map={}
    descendents_count={}
    for comment in parent_comments:
        all_descendents=comment.get_all_descendents()
        descendents_map[comment]=all_descendents
        descendents_count[comment]=len(all_descendents)



    return render(request=request,template_name="postapp/view_article.html",context={
        'post':requested_post,
        'user_has_liked':user_has_liked,
        'like_count':like_count,
        'parent_comments':parent_comments,
        'descendent_map':descendents_map,
        'descendent_count':descendents_count
    })



@require_POST
def post_comment(request,slug):
    post=Post.objects.get(slug=slug)
    try:
        data=json.loads(request.body)
        if not data.get('parent_id'):
            comment=Comments.objects.create(
                user=request.user,
                post=post,
                comment=data.get('comment')
            )

            if comment.user.profile.image:
                profile_pic=comment.user.profile.image.url
            else:
                profile_pic=""

            response_data={
               'comment_id':comment.id,
               'comment':comment.comment,
               'user_name':request.user.get_fullname()  or request.user.username,
               'date':timesince(comment.date),
               'image':profile_pic,
               'post_slug':slug,
               'descendant_count':len(comment.get_all_descendents())
            }
        else:

            super_parent_id=data.get('super_parent_id')
            parent_id=data.get('parent_id')
            super_parent_comment=Comments.objects.get(id=super_parent_id)
            parent_comment=Comments.objects.get(id=parent_id)
            comment=Comments.objects.create(
                user=request.user,
                post=post,
                comment=data.get('comment'),
                parent_id=parent_comment
            )

            if comment.user.profile.image:
                profile_pic=comment.user.profile.image.url
            else:
                profile_pic=""


            response_data={
                'comment_id':comment.id,
                'comment':comment.comment,
               'user_name':request.user.get_fullname(),
               'replied_to':parent_comment.user.get_fullname(),
               'date':timesince(comment.date),
               'image':profile_pic,
               'parent_id':comment.parent_id.id,
               'post_slug':slug,
               'descendant_count':len(super_parent_comment.get_all_descendents()),
               'super_parent_id':super_parent_id
            }
            print(response_data)

        return JsonResponse({'response':response_data}, status=200)


    except Exception as e:
        print(e)
        return JsonResponse({"error": "Invalid request"}, status=400)


@require_POST
def toggle_like(request,slug):
    if not request.user.is_authenticated:
        return JsonResponse({'error':"login required"},status=401)


    try:
        post=Post.objects.get(slug=slug)
        like,created=Like.objects.get_or_create(
            user=request.user,
            post=post
        )
        if not created:
            like.delete()
            action='unliked'
        else:
            action='liked'

        like_count=Like.objects.filter(post=post).count()
        return JsonResponse(
            {'action':action,
            'like_count':like_count,
            'user_has_liked':created
            })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=404)



@login_required
def create_post(request):
    categories=Category.objects.all()
    if request.method=="POST":
        form=PostForm(request.POST,request.FILES)

        if form.is_valid():
            post=form.save(commit=False)

            category_name=form.cleaned_data['category_input'].strip()
            category,created=Category.objects.get_or_create(
                name__iexact=category_name,
                defaults={'name':category_name}
                )
            post.author=request.user
            post.category=category
            post.save()
            return redirect('full-article', slug=post.slug)



    else:
        form=PostForm()

    return render(request=request,template_name='postapp/create_post.html',context={
        'form':form,
        'categories':categories
    })

@login_required
def edit_post(request,slug):
    categories=Category.objects.all()
    post=Post.objects.get(slug=slug)
    if request.method=="POST":
        form=PostForm(request.POST,request.FILES,instance=post)
        if form.is_valid():
            post=form.save(commit=False)

            category_name=form.cleaned_data['category_input'].strip()
            category,created=Category.objects.get_or_create(
                name__iexact=category_name,
                defaults={'name':category_name}
                )
            post.author=request.user
            post.category=category
            post.save()
            return redirect('full-article', slug=post.slug)

    else:
            form=PostForm(instance=post,initial={'category_input':post.category.name})
    return render(request,'postapp/create_post.html',{'form':form,'edit_post':True,'categories':categories})


def delete_post(request, slug):
    post = Post.objects.get(slug=slug)
    author_username = post.author.username
    post.delete()
    return redirect('author_all_posts', author=author_username)