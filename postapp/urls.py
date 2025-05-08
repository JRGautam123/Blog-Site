from django.urls import path
from .import views

urlpatterns = [
    path("",views.render_home_page,name='home_page'),
    path("articles",views.render_article_page,name='article_page'),
    path('article/<slug:slug>/',views.render_full_article,name='full-article'),
    path("create-post/",views.create_post,name='create-post'),
    path('edit-post/<slug:slug>/',views.edit_post,name='edit-post'),
    path("<slug:slug>/like",views.toggle_like,name='toggle_like'),
    path("<slug:slug>/comment",views.post_comment,name='comment'),
    path('delete-post/<slug:slug>/',views.delete_post,name='delete-post')
]
