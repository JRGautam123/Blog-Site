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
from django.contrib import messages
from django.conf import settings
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives
from blogsite.utils import EmailThread, generate_verification_token, generate_otp
from datetime import timedelta
from django.contrib.auth import login
import json
from django.http import JsonResponse
from http import HTTPStatus
from django.urls import reverse


User = get_user_model()
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
        'link': f"{app_domain}/user/verify/{uid}/{token}"
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
    EmailThread(msg=msg, user=user).start()

def send_otp(user, otp):
    """
    It send an email to the user with an OTP to reset the password
    :param: The user object that is beight sent the mail
    :param: OTP code
    """    

    email_from = settings.EMAIL_HOST_USER

    # generate and save the OPT before sending the mail
    user.password_rest_token = otp
    user.password_rest_token_sent_at = timezone.now()
    user.is_email_send_failed = False
    user.save()

    subject = "Universal Canvas Reset OTP"
    message = f"Your OTP code is: {otp}\n\n Use this code to reset your password. It will expire soon."
    recipient = [user.email]

    msg = EmailMultiAlternatives(
        subject=subject,
        body=message,
        from_email=email_from,
        to = recipient
    )
    EmailThread(msg=msg, user=user).start()
    


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
def verify_email(request, uid, token):
    try:
        uid = urlsafe_base64_decode(uid).decode()
        user = User.objects.get(pk=uid)

        if str(user.email_verification_token) == token:
            expiry_time = user.verification_link_sent_at + timedelta(days=1)

            if timezone.now() > expiry_time:
                messages.error(request, "Verification link has expired.")
                return render(request, "userapp/verification_error.html")

            user.is_active = True
            user.is_email_verified = True
            user.save()

            login(request, user)
            messages.success(request, "Email verified successfully! Welcome.")
            return redirect("home_page")

        else:
            messages.error(request, "Invalid verification token.")
            return render(request, 'userapp/verification_error.html')

    except Exception as e:
        messages.error(request, "Invalid verification link")
        return render(request, "userapp/verification_error.html")


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


def forgot_password(request):

    if request.method == 'POST':
        email = request.POST.get('email', None)
        if not email:
            return render(request, "userapp/forgot_password.html", context={"error": "Email is required"})
        try:
            user  = User.objects.get(email=email)

        except User.DoesNotExist:
            messages.error(request, "User with this mail doesn't exist. please register first.")
            return render(request, "userapp/forgot_password.html", context={"error": "User Doesn't exist"})

        otp_code = generate_otp()
        send_otp(user, otp_code)
        request.session['reset_email'] = email
        messages.success(request, "OTP code has been sent successfully. Please check your email")
        return render(request, "userapp/verify_otp.html", context={"success": "OTP code has been sent successfully. Please Check your email"})

    if request.method == "GET":
        return render(request, "userapp/forgot_password.html", context={"site_domain": settings.APP_DOMAIN})
    
    
def resend_email_verification_link(request):
    if request.method == "POST":
        email = request.POST.get("email")
        if not email:
            return render(request, "userapp/resend_email_verification_link.html", context={"error": 'Please provide an email which you used while account registration'})
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return render(request, "userapp/resend_email_verification_link.html", context={"error": "User with this email doesn't exist. Please register your account with this email first."})
        send_mail(user)
        return render(request, "userapp/resend_email_verification_link.html", context={"success": "We have sent you a mail with a email verification Link. Please Check your Email."})
    if request.method == "GET":
        return render(request, "userapp/resend_email_verification_link.html")
    

def verify_otp(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        otp = data.get('otp')

        if not otp:
            return JsonResponse(
                {"error": "Please send the  otp that we have sent you in your email."},
                status=400
            )
        email = request.session.get("reset_email")
        if email and otp:
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return JsonResponse(
                    {
                        "error": "User with this email doesn't exist."
                    },
                    status=400
                )
            otp_expiry_time = user.password_rest_token_sent_at + timedelta(minutes=5)

            if timezone.now() > otp_expiry_time :
                return JsonResponse({
                    "error": "Opt expired."
                }, status=400)
            
            if user.password_rest_token == otp:
                user.is_otp_verified = True
                user.save()

                return JsonResponse({
                    "success": True,
                    "redirect_url": reverse('reset_password')
                })
            return JsonResponse({
                "error": 'invalid otp'
            }, status=400)
    return redirect(reverse('forgot_password'))


def reset_password(request):

    email = request.session.get('reset_email')
    print(email)
    try:
        user = User.objects.get(email=email)
    except  User.DoesNotExist:
        return redirect(reverse("user_register"))
    
    if request.method == 'POST':
        password1 = request.POST.get("newPassword")
        password2 = request.POST.get("confirmPassword")

        if password1 != password2:
            return render(
                request, 
                "userapp/reset_password.html",
                context={'error':"password1 doesn't match with password2"}
            )
        
        user.set_password(password1)
        user.is_otp_verified = False
        user.password_rest_token = None
        user.password_rest_token_sent_at = None
        user.save()
        
        return redirect(reverse("login"))

    if request.method == 'GET':
        if not user.is_otp_verified:
            return redirect(reverse("forgot_password"))
        
        return render(request, "userapp/reset_password.html")