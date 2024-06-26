from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from django.contrib import messages
# Create your views here.

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def loginPage(request):
    if request.session.session_key:
        return redirect('home')
    if request.method=='POST':
        username=request.POST.get('username')
        pass1=request.POST.get('pass')
        user=authenticate(request,username=username,password=pass1)
        if user is not None:
            login(request,user)
            return redirect(home)
        elif not username or not pass1:
            messages.error(request,"Can'nt Leave Username or Password Empty")
            return redirect(loginPage)
        else:
            messages.error(request,"Check your Username Or Password")
            return redirect(loginPage)
        
    return render(request, 'login.html')


def signupPage(request):
    if request.user.is_authenticated:
        return redirect('home')
  
    if request.method=='POST':
        username=request.POST.get('username')
        email=request.POST.get('email')
        pass1=request.POST.get('password1')
        pass2=request.POST.get('password2')
        if pass1!=pass2:
             messages.error(request,"Password Does'nt Match")
             return redirect(signupPage)
        elif not username or not email or not pass1 or not pass2:
            messages.error(request,"Can'nt Leave Any Feild  Empty")
            return redirect(signupPage)
        else:
            my_user=User.objects.create_user(username,email,pass1)
            my_user.save()
            return redirect('loginPage')
            
    return render(request, 'signup.html')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='loginPage')
def home(request):
   
    return render(request,'home.html')

def logoutpage(request):
    logout(request)
    return redirect('loginPage')

    