from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile


class UserRegistrationForm(UserCreationForm):
    email=forms.EmailField(label='Email Address', required=True, error_messages={"required":'Email field must not be empty'})
    profile_pic=forms.ImageField(label='Profile Picture',required=False)

    class Meta:
        model=User
        fields=['username','email','password1','password2','profile_pic']

    
    def save(self,commit=True):
        user=super().save(commit=False)
        # user.email=self.cleaned_data['email']
        if commit:
            user.save()
            image=self.cleaned_data.get('profile_pic')
            if image:
                user.userprofile.image=image
                user.userprofile.save()
        return user