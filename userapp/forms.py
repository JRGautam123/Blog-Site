from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import UserProfile

User = get_user_model()
class UserRegistrationForm(UserCreationForm):
    profile_pic=forms.ImageField(label='Profile Picture',required=False)
    class Meta:
        model = User
        fields=['email','password1','password2','profile_pic','first_name', 'middle_name','last_name']

    def save(self,commit=True):
        profile_pic = self.cleaned_data.pop("profile_pic", None)
        user=super().save(commit=False)

        if commit:
            user.is_active = False
            user.save()

        UserProfile.objects.create(user=user, image=profile_pic)

        return user

class UserUpdateFrom(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'first_name','middle_name','last_name',]

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['image']