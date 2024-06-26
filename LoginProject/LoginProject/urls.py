
from django.contrib import admin
from django.urls import path
from home import views

urlpatterns = [
    path('',views.loginPage,name="loginPage"),
    path('signup/',views.signupPage,name="signupPage"),
    path('home/',views.home,name="home"),
    path('logout/',views.logoutpage,name="logout"),
    path('admin/', admin.site.urls),
]
