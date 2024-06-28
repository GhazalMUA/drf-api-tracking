from rest_framework.views import APIView
from rest_framework.response import Response
from tracking.mixins import LoggingMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
class MockNoLoggingView(APIView):
    def get(self,request):
        return Response ('no logging')
    
    
class MockLoggingView(LoggingMixin, APIView):
    def get(self, request):
        return Response('with logging')


class MockExplicitLoggingView(LoggingMixin,APIView):
    '''
        rooye methodi k khodemon moshkhas kardim mikhyam tamarkoz bokonim ke bebinim doorost kar mikone ya na
    '''
    logging_methods=['POST']
    
    def get(self,request):
        return Response('in method nabayad farakhani beshe va log kone.')
    def post(self,request):
        return Response('in method bayad farakhani beshe va log kone.')
    
 
    
class MockCostumCheckLoggingView(LoggingMixin,APIView):
    '''
        mikhyam bebinim ke method should_log kar mikone ya na 
        daravaghe mikhyam y seri shart bzarim k ye seri log hay be khosoooos zakhire beshan
        hala inja mikhaym moshakhas konim age tooye response az kalameye `log` estefade shode bod bia zakhire
        kon on response ro.
        vaseye in kar method should_log() ro override kardam va in ghazie ro toosh moshakhas kardam
        bad omadam 2ta method sakhtam yekish tooye response esh vazheye log hast tooye yekish nist
        badfan test ro ba hamin methodha misanjim.
    '''    
    
    def should_log(self, request,response):
        return 'log' in response.data

    def get(self,request):
        return Response ('with logging')
    
    def post(self,request):
        return Response ('no recording bardia')
    
    
    
    
    
class MockSessionAuthLoggingView(LoggingMixin,APIView):
    '''
        in class vase ineke cj=heck koim bbinim karbar hatman loggin karde bashe.
        vase in kar in dota ro import mikonim.
        from rest_framework.permissions import IsAuthenticated
        from rest_framework.authentication import SessionAuthentication
        authentication_classes va permission_classes male khode APIView hastan tooye source code peydashon kardam
        
    '''    
    authentication_classes=(SessionAuthentication,)
    permission_classes=(IsAuthenticated,)
    
    def get(self,request):
        return Response('with session auth logging')
    
    
    
class MockSensitiveFieldsLoggingView(LoggingMixin,APIView):
    sensitive_fields={'mY_FiEld'}
    def get(self,request):
        return Response('with logging after sensitive')    
    
    
class MockInvalidCleanedSubstituteLoggingView(LoggingMixin,APIView):
    '''
        moshakhas karde bodim tooye mixin moon k htamn clean_substitute ye string bashe 
        hala inja miaym y integer ro be onvane defaulf entekhab mikonim k khata bede.
    '''    
    CLEANED_SUBSTITUTE=2
