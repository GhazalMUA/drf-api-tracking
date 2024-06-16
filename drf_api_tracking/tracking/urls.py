from django.urls import path
from .import views

app_name='tracking'
urlpatterns=[
    path('home/' , views.HomeAPIView.as_view() , name ='home'),
    
]