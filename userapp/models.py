from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from blogsite.models import TimeStampedModel


from .managers import UserManager
class User(AbstractBaseUser, PermissionsMixin, TimeStampedModel):
    email = models.EmailField(max_length=255, verbose_name="Email Address", unique=True)
    first_name = models.CharField(max_length=100,)
    middle_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, )
    is_staff = models.BooleanField(
        "Can Login Admin Site?",
        default=False,
        help_text=(
            "Designates Whether the user can login into this admin site."
        ),
    )
    is_active = models.BooleanField(
        "Is Account Active?",
        default=True,
        help_text=(
             "Designates whether this user should be treated as active. Unselect this instead of deleting accounts."
             ),
    )

    is_email_verified = models.BooleanField(default=False, verbose_name="verfied")
    email_verification_token = models.UUIDField(null=True, blank=True)
    verification_link_sent_at = models.DateTimeField(blank=True, null=True)

    password_rest_token = models.CharField(max_length=6, blank=True, null=True)
    password_rest_token_sent_at = models.DateTimeField(blank=True, null=True)

    objects = UserManager()

    class Meta:
        verbose_name = "User"
        verbose_name_plural = f"{verbose_name}'s"
        ordering = ("-created_at", )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'middle_name', 'last_name']


    def get_fullname(self):
        if self.middle_name:
            return f"{self.first_name} {self.middle_name} {self.last_name}"
        else:
            return f"{self.first_name} {self.last_name}"
    
    def __str__(self):
        return self.get_fullname()

class UserProfile(TimeStampedModel):
    user = models.OneToOneField(User,on_delete=models.CASCADE, related_name='profile')
    image = models.ImageField(upload_to='profile_pic', blank=True, null=True)

    def __str__(self):
       return self.user.get_fullname()
