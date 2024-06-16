from django.contrib import admin
from .models import APIRequestLog

# Register your models here.
class BaseAPIRequestLog(admin.ModelAdmin):
    list_display = (
        'id',
        'requested_at' ,
        'response_ms' ,
        'status_code' , 
        'user' ,
        'view_method' ,
        'path' , 
        'remote_addr' , 
        'host' ,
        'query_params' ,
    )
    list_per_page = 20
    search_fields = ('status_code',)


admin.site.register(APIRequestLog,BaseAPIRequestLog)