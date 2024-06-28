from rest_framework.test import APITestCase , APIRequestFactory
from tracking.models import APIRequestLog
from .views import MockLoggingView
from django.test import TestCase, override_settings 
from tracking.models import APIRequestLog
from django.contrib.auth.models import User
import ast
from tracking.mixins import BaseLoggingMixin
'''
    Use self.client when you want to test how the application handles
    a request end-to-end, including routing, middleware, and view rendering.
    Use APIRequestFactory when you want to test specific view logic in isolation 
    and need more control over the request setup.


    Mocking requests and responses in tests allows you to simulate
    various scenarios without the need for actual HTTP requests.
    This makes tests faster and more reliable.


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
        '''
        APIRequestFactory: This is a utility provided by Django REST Framework to create mock requests for testing.

        .get('urlpath'): This method creates a GET request to the `urlpath` endpoint.

        request.META: This is a dictionary-like object that contains all the HTTP headers sent with the request. META is a standard attribute for request objects in Django.

        (request): This passes the mock request object to the view for processing.
        
        .render(): This ensures that the response is fully rendered. Rendering the response is important in testing because some processing might only occur during this phase.
        '''
        
        request = APIRequestFactory().get('/with_logging/')
        request.META['REMOTE_ADDR']= '127.0.0.9'
        MockLoggingView.as_view()(request).render()
        log=APIRequestLog.objects.first()
        self.assertEqual(log.remote_addr,'127.0.0.9')
        
        
    
    def test_log_ip_remote_list(self):
        request=APIRequestFactory().get('/with_logging/')  
        request.META['REMOTE_ADDR']='127.0.0.9, 127.0.0.5, 127.0.0.4'
        MockLoggingView.as_view()(request).render()
        log=APIRequestLog.objects.first()
        self.assertEqual(log.remote_addr,'127.0.0.9')
        
        
        
    def test_log_ip_remote_v4_with_port(self):
        request=APIRequestFactory().get('/with_logging/')
        request.META['REMOTE_ADDR']='127.0.0.7:6640'
        MockLoggingView.as_view()(request).render()
        log = APIRequestLog.objects.first()
        self.assertEqual(log.remote_addr, '127.0.0.7')
        
        
        
        
    def test_log_ip_remote_v6(self):
        request=APIRequestFactory().get('/with_logging/')    
        request.META['REMOTE_ADDR']='2001:0db8:85a3:000:0000:8a2e:0370:7334'
        MockLoggingView.as_view()(request).render()
        log= APIRequestLog.objects.first()
        self.assertEqual(log.remote_addr, '2001:db8:85a3::8a2e:370:7334')



#in vase moghheiye k ip male khodemone(local)         
    def test_log_ip_remote_v6_loopback(self):   
        request= APIRequestFactory().get('/with_logging/')
        request.META['REMOTE_ADDR']='::1'
        MockLoggingView.as_view()(request).render()
        log= APIRequestLog.objects.first()
        self.assertEqual(log.remote_addr, '::1')


    def test_log_ip_remote_v6_with_port(self):
        request= APIRequestFactory().get('/with_logging/')
        request.META['REMOTE_ADDR']='[::1]:7000'        
        MockLoggingView.as_view()(request).render()
        log=APIRequestLog.objects.first()
        self.assertEqual(log.remote_addr,'::1')
        
    
    def test_log_ip_xforwarded(self):
        request=APIRequestFactory().get('/with_logging/')
        request.META['HTTP_X_FORWARDED_FOR']='127.0.0.7'
        MockLoggingView.as_view()(request).render()
        log=APIRequestLog.objects.first()
        self.assertEqual(log.remote_addr,'127.0.0.7')
        
        
    def test_log_ip_xforwarded_list(self):
        request=APIRequestFactory().get('/with_logging/')
        request.META['HTTP_X_FORWARDED_FOR']='127.0.0.7, 127.0.0.5, 127.0.0.2'
        MockLoggingView.as_view()(request).render()
        log=APIRequestLog.objects.first()
        self.assertEqual(log.remote_addr,'127.0.0.7')
        
  
    def test_log_host(self):
        self.client.get('/with_logging/')    
        log=APIRequestLog.objects.first()
        self.assertEqual(log.host, 'testserver')
        
        
    def test_log_method(self):
        self.client.get('/with_logging/')
        log=APIRequestLog.objects.first()
        self.assertEqual(log.method, 'GET')
        
    
    def test_log_status(self):
        self.client.get('/with_logging/')
        log=APIRequestLog.objects.first()
        self.assertEqual(log.status_code,200)    
        
        
        
    def test_login_explicit(self):
        self.client.get('/explicit_logging/')    
        self.client.post('/explicit_logging/')
        log=APIRequestLog.objects.all().count()
        self.assertEqual(log, 1)
        
        
    
    def test_custom_check_logging(self):
        self.client.get('custom_check_logging/') 
        self.client.post('custom_check_logging/')
        log=APIRequestLog.objects.all().count()   
        self.assertEqual(log, 0)
        
        
        
    def log_annon_user(self):
        self.client.get('/with_logging/')
        log=APIRequestLog.objects.first()
        self.assertEqual(log.user,None)
        
        
     
    def test_log_auth_user(self):
        User.objects.create_user(username='myname' , password='mypass')
        usermon=User.objects.get(username='myname')
        self.client.login(username='myname' , password='mypass')
        self.client.get('/session_auth_logging/')
        log=APIRequestLog.objects.first()
        self.assertEqual(log.user , usermon )
        
        
        
        
    def test_log_params(self):
        self.client.get('/with_logging/' , {'key1':'value1' , 'key2':'value2'})  
        log=APIRequestLog.objects.first()
        self.assertEqual(ast.literal_eval(log.query_params) , {'key1':'value1' , 'key2':'value2'})
        #chonke besorate string hamechiz zakhire mishe az ast.literal_eval() estefade mikonim k code pythonie tooye string ro vasamon biare
        
        
    
    def test_log_params_cleaned_from_personal_list(self):
        '''
            tooye on mixin moon vase query_params miomadim midadimesh be _cleaned_data ke vasamon 
            check kone bebine etelaate hasas toosh nabashe ag ham etelaate hasas toosh bod vasamon 
            on setareharo bezare setare haram tahte onvene clean_substitute variable ye string i
            ke toosh setarast save karde boodim
        '''    
        clst=BaseLoggingMixin.CLEANED_SUBSTITUTE 
        self.client.get('/sensitive_fields_logging/',{'api':'12344444' , 'my_field':'fresh' , 'ghazalmua':'12345'})
        log=APIRequestLog.objects.first()
        self.assertEqual(ast.literal_eval(log.query_params) , {
                                             'api':clst ,
                                             'my_field': clst , 
                                             'ghazalmua':'12345' ,
                                                            
        })
        
