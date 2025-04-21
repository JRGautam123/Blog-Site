from django.shortcuts import render

# Create your views here.


def render_home_page(request):
    return render(request=request,template_name='postapp/home_page.html')


def render_article_page(request):
    return render(request=request,template_name='postapp/articles.html')