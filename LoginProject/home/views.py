from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control,never_cache
from django.contrib import messages
# Create your views here.

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def loginPage(request):
   
    if request.session.session_key:
        if request.user.is_staff:
                
            return redirect('admins')
        else:
    
            return redirect('home')

    if request.method=='POST':
        username=request.POST.get('username')
        pass1=request.POST.get('pass')
        user=authenticate(request,username=username,password=pass1)
        
        if user is not None:
            login(request,user)
            if request.user.is_staff:
                
                return redirect('admins')
    
            return redirect(home)
        elif not username or not pass1:
            messages.error(request,"Can'nt Leave Username or Password Empty")
            return redirect(loginPage)  
        else:
            messages.error(request,"Check your Username Or Password")
            return redirect(loginPage)
        
    return render(request, 'login.html')

@never_cache
def signupPage(request):
    if request.session.session_key:
        if request.user.is_staff:
            return redirect('admins')
        else:
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

@never_cache
@login_required(login_url='loginPage')
def home(request):
    if request.user.is_superuser:
        return redirect('admins')
   
    return render(request,'home.html')

def logoutpage(request):
    logout(request)
    return redirect('loginPage')


@login_required(login_url='loginPage')
@never_cache
def admins(request):
    if not request.user.is_superuser:
        return redirect('home')
    else:
        txt=User.objects.filter(is_superuser=False)
        if request.method=='GET':
            username=request.GET.get('q','')
            txt=User.objects.filter(username__icontains=username,is_superuser=False)
           
        return render(request,'admin.html',{'txt':txt})
            
            
            
        
         
    
@login_required(login_url='loginPage') 
@never_cache   
def add(request):
    if request.method == 'POST':
        name=request.POST.get('name1')
        email=request.POST.get('email1')
        newuser=User.objects.create_user(name,email)
        newuser.save()
        return redirect('admins')
    return render(request,'admin.html')
@login_required(login_url='loginPage')
@never_cache
def edit(request):
    
    return render(request,'admin.html')

@login_required(login_url='loginPage')
@never_cache
def update(request,id):
    if request.method == 'POST':
        name=request.POST.get('name2')
        email=request.POST.get('email2')
        newuser2=User(id=id,username=name,email=email)
        newuser2.save()
        return redirect('admins')
    return redirect(request,'admins')

@login_required(login_url='loginPage')  
@never_cache 
def delete(request,id):
    txt=User.objects.filter(id=id).delete()
    return redirect('admins')
    