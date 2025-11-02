from django.shortcuts import render,redirect
from .forms import (
    UserRegistrationForm,
    UserUpdateFrom,
    ProfileUpdateForm,
)
from django.contrib.auth.decorators import login_required
from postapp.models import Post
from django.core.paginator import Paginator
from django.utils.encoding import force_bytes
from django.utils import timezone
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.template.loader import get_template
from django.contrib.auth import get_user_model
from django.conf import settings
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives
from blogsite.utils import EmailThread, generate_verification_token


def send_mail(user):
    """
        It sends an email to the user with a link to verify their account
        :param: The user object that is being sent the email.
    """

    subject = "Verify your Universal Canvas Account"
    email_from = settings.EMAIL_HOST_USER
    app_domain = settings.APP_DOMAIN

    # generate and save the tokne before sending the email.
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = generate_verification_token()
    user.email_verification_token = token
    user.verification_link_sent_at  = timezone.now()
    user.is_email_send_failed = False
    user.save()

    context = {
        "user": user,
        "app_domain": app_domain,
        'link': f"{app_domain}/verify/{uid}/{token}"
    }
    template = get_template("userapp/verify_email.html")
    html_messag = template.render(context=context)
    
    msg  = EmailMultiAlternatives(
        subject=subject,
        body=html_messag,
        from_email=email_from,
        to=[user.email]
    )
    msg.attach_alternative(html_messag, "text/html")
    EmailThread(msg=msg, token=token, user=user).start()
    

User = get_user_model()
def register(request):
    try:
        if request.method == 'POST':
            form=UserRegistrationForm(request.POST, request.FILES)
            if form.is_valid():
                user = form.save()
                send_mail(user)
                return redirect('home_page')
        else:
            form = UserRegistrationForm()
        return render(request,'userapp/register.html', {'form':form})
    except Exception as e:
        print(e)
        return render(request,'userapp/register.html', {'form':form,'error':e})

# user email verification.
def verify_email(request, uuid, token):
    pass




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


