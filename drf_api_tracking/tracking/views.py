from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .mixins import LoggingMixin


class HomeAPIView(LoggingMixin,APIView):
    logging_methods=['GET']
    
    def get(self,request):
        return Response('hello there')
    
