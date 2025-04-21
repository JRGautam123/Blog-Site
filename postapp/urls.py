from django.urls import path
from .import views

urlpatterns = [
    path("",views.render_home_page,name='home_page'),
    path("articles",views.render_article_page,name='article_page')
]
