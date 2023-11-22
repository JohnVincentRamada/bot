from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    
    path('', include('bot.urls')),
    path('admin/', include('customadmin.urls')),
    path('dj-admin/', admin.site.urls),
    path('captcha/', include('captcha.urls')),
    
]
