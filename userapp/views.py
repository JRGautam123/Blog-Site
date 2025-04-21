from django.shortcuts import render,redirect
from .forms import UserRegistrationForm

# Create your views here.

def register(request):
    if request.method=='POST':
        form=UserRegistrationForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home_page')
    else:
        form=UserRegistrationForm()
    return render(request,'userapp/register.html',{'form':form})
