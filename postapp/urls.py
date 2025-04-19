from django.urls import path
from .import views

urlpatterns = [
    path("",views.render_landing_page,name='landing_page'),
]
