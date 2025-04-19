from django.shortcuts import render

# Create your views here.


def render_landing_page(request):
    return render(request=request,template_name='base.html')