from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import UserProfile

User = get_user_model()
class UserRegistrationForm(UserCreationForm):
    email=forms.EmailField(label='Email Address', required=True, error_messages={"required":'Email field must not be empty'})
    profile_pic=forms.ImageField(label='Profile Picture',required=False)

    class Meta:
        model = User
        fields=['email','password1','password2','profile_pic','first_name', 'middle_name','last_name']

    
    def save(self,commit=True):
        user=super().save(commit=False)
        # user.email=self.cleaned_data['email']
        if commit:
            user.save()
            image = self.cleaned_data.get('profile_pic')
            if image:
                user.userprofile.image = image
                user.userprofile.save()
        return user
    
class UserUpdateFrom(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'first_name','middle_name','last_name',]

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['image']