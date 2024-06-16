from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .base_mixins import BaseLoggingMixin


class HomeAPIView(BaseLoggingMixin,APIView):
    def get(self,request):
        return Response('hello there')