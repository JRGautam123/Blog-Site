from django.urls import path
from . import views
from django.contrib.auth.views import LoginView,LogoutView

urlpatterns = [
    path('register',views.register,name='user-register'),
    path(r"verify/<str:uid>/<str:token>/", views.verify_email, name="verify email"),

    path("login/",LoginView.as_view(template_name='userapp/login_page.html'),name='login'),
    path("logout/",LogoutView.as_view(next_page='login'),name='logout'),
    path('profile',views.profile_view,name='profile'),
    path('<int:author>/all_posts/',views.author_all_posts,name='author_all_posts'),

    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path("resend-email-verification-link/", views.resend_email_verification_link, name='resend_email_verification_link'),
    path("verify-otp/", views.verify_otp, name="verify_otp"),

    path("reset-password/", views.reset_password, name="reset_password")

]
