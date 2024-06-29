from rest_framework.test import APITestCase , APIRequestFactory
from tracking.models import APIRequestLog
from .views import MockLoggingView
from django.test import TestCase, override_settings 
from tracking.models import APIRequestLog
from django.contrib.auth.models import User
import ast
from tracking.mixins import BaseLoggingMixin
from unittest import mock
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
        
        
        
    def test_invalid_cleaned_substitute_fails(self):
        '''
            miaym check mikonim hatman on variable clean_substitue i ke karbar vared karde be
            sorate string bashe va chon in code shart ro ba assert neveshte bodimesh tooye base_mixins,
            bayad assertionerror behesh bedim. nokteye badi inke toye view i ke be invalid_cleaned_substitute 
            vasle ma ye clean_substitude intiger dadim k shart ro naghz kone vasde hamin test esh injri neveshte mishe
        '''
        with self.assertRaises(AssertionError):    
            self.client.get('/invalid_cleaned_substitute/')
        











        '''
            MOCK baraye shabih sazie amaliati hastesh ke nemikhaym vaghean etefagh biofte.
            vaseye delete kardane file ya upload kardane file
        '''
    @mock.patch('tracking.models.APIRequestLog.save')
    def test_log_doesnt_prevent_api_call_if_log_savefails(self , mock_save):
        '''
            ba on decorator i ke mizarim balaye function moshakhas mikonim k bere 
            too app tracking tooye file modeles.py va modele APIRequestLog ro biare
            va method save ro mock kone ke dige etefagh nayofte kolan hadafe in function
            mon ine ke age yemoghe mixin mon kar nakard etelaat eshteabh sabt nakone.
            baraye moshakhas kardane Exceptionha az `side_effect` estefade mikonim.
            vaghti miaym `side_effect` moshakhas mikonim yani vaghti save etefagh
            oftad Exception etefagh biofte ba in payam k `db failure`
            
        '''
        mock_save.side_effect = Exception('db failure')
        response = self.client.get('/with_logging/')
        tedad = APIRequestLog.objects.all().count()
        self.assertEqual(response.status_code , 200)
        self.assertEqual(tedad , 0)
        
        
        