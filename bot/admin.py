from django.contrib import admin
from bot.models import RequestContext

class RequestContextAdmin(admin.ModelAdmin):
    list_display = ('id','request', 'comment', 'status', 'created_at') 

admin.site.register(RequestContext, RequestContextAdmin)