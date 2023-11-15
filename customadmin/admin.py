from django.contrib import admin
from customadmin.models import Description

class DescriptionAdmin(admin.ModelAdmin):
    list_display = ('id','title', 'category', 'answer', 'created_at') 

admin.site.register(Description, DescriptionAdmin)