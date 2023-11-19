from django.conf import settings
from django.conf.urls.static import static
from django.urls import path,include
from . import views

urlpatterns = [
    path('login', views.sign_in, name='login'),
    path('registration', views.register, name='register'),
    path('signout', views.signout, name='signout'),
    
    
    
    
] 
