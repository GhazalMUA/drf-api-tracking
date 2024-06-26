from rest_framework.test import APITestCase , APIRequestFactory
from tracking.models import APIRequestLog
from .views import MockLoggingView
from django.test import TestCase, override_settings
from tracking.models import APIRequestLog


'''
    midooniim ke vaghti ye urls.py tooye app haye django darim hatman 
    bayad in urls.py ro be url aslie barname k tppye project django 
    hastesh mparefi bokonim va inke ba dastoore `include` in kar ro
    anjaam midim. hsls y masalei hastesh vase inke url mon ro shologh 
    ankonim az property @override_settings estefade mikonim k url aslie 
    barname ro moshakhas mikone k inja chon mohite testmon hastesh mitonim 
    be shekle movaghat url testimon ro be onvane url asli moarefi konim ke 
    django ham beshnasatesh. aval bayad az django.test import esh konim
    badesh @override_settings() dakhelesh oon configi k niaz darim ro minevisiim
    masalan alan ROOT_URLCONF ro gharare override bokonim.
'''
@override_settings(ROOT_URLCONF='tracking.tests.urls')

class TestLoggingMixin(APITestCase):
    def test_no_logging_no_log_created(self):
        self.client.get('/no_logging/')
        self.assertEqual(APIRequestLog.objects.all().count(),0)
        
        
    def test_logging_create_log(self):
        self.client.get('/with_logging/',{'key1':'value1'})    
        self.assertEqual(APIRequestLog.objects.all().count(),1)
    