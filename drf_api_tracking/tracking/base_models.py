from django.db import models
from django.conf import settings


class BaseAPIRequestLog(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL , null=True , blank=True)
    username_persistent=models.CharField(max_length=getattr(settings,'DRF_TRACKING_USERNAME_LENGTH',200),null=True,blank=True)  #age in meghdare 'DRF_TRACKING_USERNAME_LENGTH' tooye settings.py meghdar dehi shode bood k hichi ag nashode bood az meghdar default 
    requested_at=models.DateTimeField(db_index=True)
    response_ms=models.PositiveIntegerField(default=0)
    path=models.CharField(max_length=getattr(settings,'DFR_TRACKING_PATH_LENGTH', 200) , help_text='url path', db_index=True)
    view=models.CharField(max_length=getattr(settings , 'DRF_TRACKING_VIEW_LENGTH',200) , blank=True , null=True , db_index=True)
    view_method=models.CharField(max_length=getattr(settings,'DRF_TRACLING_VIEWMETHOD_LENGTH' , 200) , blank=True, null=True, db_index=True)
    remote_addr=models.GenericIPAddressField()
    host=models.URLField()
    method=models.CharField(max_length=10)
    query_params=models.TextField(blank=True,null=True)
    data=models.TextField(null=True,blank=True)          #age az tarighe method post etelaati omade bashe inja zakhire mishe
    response=models.TextField(null=True,blank=True)     #har pasokhi be karbar midin inja zakhire mishe hala mikhad safe html i bashe ya mikhad api bashe yaa harchize digei.
    errors=models.TextField(null=True,blank=True)
    status_code=models.PositiveIntegerField(null=True,blank=True,db_index=True)
    
    
    class Meta:
        abstract = True
        verbose_name= ' API request log'
        
        
    def __str__(self):
        return '{} {}'.format(self.method,self.path)
