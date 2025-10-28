from django.shortcuts import render,redirect
from .forms import (
    UserRegistrationForm,
    UserUpdateFrom,
    ProfileUpdateForm,
)
from django.contrib.auth.decorators import login_required
from postapp.models import Post
from django.core.paginator import Paginator
from django.contrib.auth import get_user_model

User = get_user_model()
def register(request):
    try:
        if request.method == 'POST':
            form=UserRegistrationForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                return redirect('home_page')
        else:
            form = UserRegistrationForm()
        return render(request,'userapp/register.html', {'form':form})
    except Exception as e:
        print(e)
        return render(request,'userapp/register.html', {'form':form,'error':e})


@login_required
def profile_view(request):
    if request.method == "POST":
        user_form=UserUpdateFrom(request.POST, instance=request.user)
        profile_form=ProfileUpdateForm(request.POST,request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect("profile")
    else:
        user_form=UserUpdateFrom(instance=request.user)
        profile_form=ProfileUpdateForm(instance=request.user.profile)
    return render(
        request=request,template_name='userapp/user_profile.html', 
        context= {'u_form':user_form, 'p_form':profile_form}
    )

def author_all_posts(request,author):
    user=User.objects.get(pk=author)

    posts=Post.objects.filter(author=user).order_by('-date')
    paginator=Paginator(posts,3)
    page=request.GET.get('page')
    post_objs=paginator.get_page(page)
    return render(request,'userapp/author_all_posts.html',{'posts':post_objs,'user_name':user.get_fullname()})


