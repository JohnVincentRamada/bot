from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from . import views
from django.contrib import admin


urlpatterns = [
    path('', views.home, name='home'),
    path('A-Bot', views.a_bot, name='a-bot'),
    path(r'aut/', include('authentication.urls'), name='aut'),
    path('recognize/', views.recognize, name='recognize'),
    path('rectemplate/', views.rectemplate, name='rectemplate'),
    path('log/', views.log, name='log'),
    path('requestcontext', views.request_context, name='request_context'),
    
    
    
] 

