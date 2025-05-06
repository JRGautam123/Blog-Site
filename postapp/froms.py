from django import forms

from .models import Category,Post

class PostForm(forms.ModelForm):
    category_input=forms.CharField(
        label="Category",
        max_length=100,
        help_text="Type or select a category",
        widget=forms.TextInput(attrs={'list':'category-options'})
    )
    class Meta:
        model=Post
        fields=['title','excerpt','image','content']

