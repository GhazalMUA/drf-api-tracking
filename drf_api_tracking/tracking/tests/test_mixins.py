from rest_framework.test import APITestCase , APIRequestFactory
from tracking.models import APIRequestLog
from .views import MockLoggingView
from django.test import TestCase, override_settings , RequestFactory
from tracking.models import APIRequestLog
from django.urls import reverse


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
        
        
        
    #inja khodam behesh query parameters ro testi dadam bbinm kar mikone ya na k didam kar kard    
    def test_logging_create_log(self):
        self.client.get('/with_logging/',{'key1':'value1'})    
        self.assertEqual(APIRequestLog.objects.all().count(),1)
    
    
    
    def test_path(self):
        self.client.get('/with_logging/')
        log = APIRequestLog.objects.first()    # miad avalin record i k save shode tooye modele APIRequest ro mirize tooye moteghayere log. 
        self.assertEqual(log.path , '/with_logging/')   # tooye modele APIRequest, miad field e path esh ro check mikone va ba in url i tooye client moshakhas kardim moghayese mikonim.
        
        
        
    def test_log_ip_remote(self):
        rf = RequestFactory().get('/with_logging/')
        rf.META['REMOTE_ADDR']= '127.0.0.9'
        MockLoggingView.as_view()(rf).render()
        log=APIRequestLog.objects.first()
        self.assertEqual(log.remote_addr,'127.0.0.9')