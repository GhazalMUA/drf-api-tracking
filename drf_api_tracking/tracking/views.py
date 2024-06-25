from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .mixins import LoggingMixin


class HomeAPIView(LoggingMixin,APIView):
    '''
        moshakhas kardim k pass ye kalameye hasase vase ma dar vaghe ye
        field hasase vaa mikhaym k in field tooye model hamon save nashe. 
    '''
    logging_methods=['GET']
    sensitive_fields ={'pass'}      
    def get(self,request):
        return Response('hello there')
  
