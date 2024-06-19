from django.utils.timezone import now
import ipaddress
from tracking.app_settings import app_settings
import traceback
import logging



logger=logging.getLogger(__name__)         #vase neveshtane log. bad ghabl az inke self.handle_log() ejra beshe y try except mizarim ag exception i etefagh oftad tooye log file betone zakhirash bokone.

class BaseLoggingMixin:
    
    logging_methods='__all__'                  #vaseye entekhabe noe method e http
    
    '''
        method initial ke in zire yeki ag method hay aslie class e APIView
        hast ke ghabl az inke request ersal beshe ejra mishe; ma omadim
        override esh kardm k django ro goool bzanim ghabl az inke kari 
        kkone biad kari k ma mikhaymo anjam bede. kari ham k ma mikhaym 
        bokonim ine ke taktake etelaate model_base mon ro inja tooye
        `self.log` zakhire konim tooye ye dictionary ke badan in `self.log`  
        ro befrestim be model aslimooon.
        
        baaraye zakhire kardane ip karbar az finalize_response() estefade 
        mikonim chonke karbar miad darkhastesho ersal mikone bad ke pasokh
        bargardonede shod az rooye on pasokh ip karbar ro migirim va tooye
        `self.log` save esh mikonim.
        
    '''
    
    def initial(self, request, *args, **kwargs):
        self.log={'requested_at':now(),}
        return super().initial(request, *args, **kwargs)
    
    
    def handle_exception(self, exc):
        """
        in method male khode APIView hastesh k ma overridesh mikonim superesho seda mizanim
        vaa tooye dele in function khata haro migiiirim. gereftanae matne khata ha ham ba
        module Traceback anjam mishe. module traceback khatayi k be shoma namayesh dade mishe
        ro dar ekhtiare shoma gharar mide.
        in module method hay mokhtalefi dare vali ma miaym az method `format.exc` estefade 
        mikonim k khata ro b shekle string b shoma namayesh mide.
        
        ye method hm minevismim be esme should_log() ke age true bargardoond log etelaat karbar, 
        zakhire beshe va ag false bargardoond save nashan. masalan moshakhas konim ag error balaye 
        400 bod biad log ro save kone ya age method i k karbar baahaash miad post bod log ro save
        kone ya harchize digei....
        
        """
        response= super().handle_exception(exc)
        self.log['errors']=traceback.format_exc()
        return response
    
    
    def finalize_response(self, request, response, *args, **kwargs):
        response= super().finalize_response(request, response, *args, **kwargs)
        if self.should_log(request,response):
            user=self._get_user(request)
            self.log.update({
                'remote_addr': self._get_ip_address(request) ,
                'view':self._get_view_name(request),
                'view_method' : self._get_view_method(request),
                'path':self._get_path(request),
                'user': user,
                'host': request.get_host(),     #khode request e django method get_host() ro dare.
                'method': request.method,
                'username_persistent': user.get_username() if user else 'Anonymous',
                'response_ms':self._get_response_ms(),
                'status_code':response.status_code,
            })
            try:
                self.handle_log()
            except Exception:
                logger.exception('Loggin API call raise  exception.')
        return response
    
    
    def _handle_log(self):
        raise NotImplementedError
    
    
    
    def _get_ip_address(self,request):
        '''
            ma baraye gereftane ip address karbar 2ta header dariim
            avalish khode http header hastesh REMOTE_ADDR in ip karbari 
            hastesh k vasl shode be website shoma va ip karbar too moteghayere
            REMOTE_ADDR  zakhire mishe. in momkene k taghir kone maslan vaghti karbar 
            az vpn estefade mikone emkanesh hast k taghir bokone va ip proxy y hamon vpn 
            ro neshoon mide. ye header dg darim b esme HTTP_X_FORWARDED_FOR hastesh vali tooye
            in dg faghat ip address vagheiye karbar namayesh dade mishe hata ag az vpn estefade kone 
            ava address vagheisho neshoon mide bad az on ip haye proxy hayi k beheshon karbar vasle ro
            be tartib bad az ip aslish minevise va nokte inke in ip ha ba comma tooye in az ham dg joda mishan. 
            age karbar az proxy ya vpn estefade nakone, REMOTE_ADDR  va HTTP_X_FORWARDED_FOR  baaham dige barabaar mishan.
        '''
        
        ipaddr=request.META.get('HTTP_X_FORWARDED_FOR',None)   # boro begard ag in httpe boodesh berizesh too ipaddr ag nabodesh ham bejash none bezae
        if ipaddr:                                             # age boodesh oon moghe:        
            ipaddr=ipaddr.split(',')[0]                        # hamontor k ghablan goftfim in headere 'HTTP_X_FORWARDED_FOR' 
                                                               # ham ip khode karbaro aval neshon mide bad ip on proxy hai k bhshon
                                                               # vasle. va hamontor k goftim ba comma joda mishan hala [0] yani indexe
                                                               # sefrom yani item aval k mishe ip khode karbar ro mikhad biare
        else:
            ipaddr=request.META.get('REMOTE_ADDR', '').split(',')[0]   # dar soorati k tooye header ha 'HTTP_X_FORWARDED_FOR' ro nadashti
                                                                        # begard donbale 'REMOTE_ADDR va age onam nadidi y string khali bargardon
                                                                        
        possibles=(ipaddr.lstrip('[')).split(']')[0], ipaddr.split(':')[0]               
        '''
            in posiibles bekhatere ineke bazi vaghtga ip be y shekli khasi be ma bargardoonde mishe.
            masalan__>   [<ipv6 address>]     ya in sheklie__>      [<ipv6 address>]:port   vaseinke 
            ip ro dorost va bedone hichi save esh konim tooye database,az line bala posiibles estefde
            mikonim.
        '''
        
        for addr in possibles:
            try:
                return str(ipaddress.ip_address(addr))         
            except:
                pass   
                                          
    """
        HTTP_X_FORWARDED_FOR ----->  proxy=>   real_ip , 1st_proxy_ip , 2nd_proxy_ip , last_proxy_id
        REMOTE_ADDR ----->   proxy=>   ip proxy
    """               
            
   
    def _get_view_name(self,request):
        method = request.method.lower()    #getting http method
        try:
            attribute=getattr(self,method)     #begard tooye self etelaate marboot be on method khas ro baram biar masalan aln
                                               #vsase in barname ino mide ag ino ejra koni:
                                               # <bound method HomeAPIView.get of <tracking.views.HomeAPIView object at 0x102a99040>>
                                               #ag ino ejea ko ni   print(attribute.__self__)   ino mide:   <tracking.views.HomeAPIView object at 0x1051eb230>       
            return (type (attribute.__self__).__module__ + '.' + type(attribute.__self__).__name__)

        except AttributeError:
            return None
        
        

    def _get_view_method(self,request):
        if hasattr(self,'action'):
            return self.action or None
        return request.method.lower()
    
    
    
    def _get_path(self,request):
        return (request.path[:app_settings.PATH_LENGTH])
        
        
        
    def _get_user(self,request):
        user=request.user
        if user.is_anonymous:
            return None
        else:
            return user    

    def _get_response_ms(self,):
        '''
            baraye gereftane time resonse bayad zamani k request ferestade
            shode ro az time hamin hala kam konim ye adadi bdast miad 
            00:00:00:000123 intorie bayad ham inke intigeresh konim ham inke 
            fghat sanie sho mikhaym ke taze onam bayad chon milisanie mikhaym 
            bayad hamoon sanie ash ro ham dar 1000 zarb konim.
            bazi vaghta momkene b bug bokhore javab ro bhmon manfi bede vase 
            hamin az in estefade mikonim max(response_ms,0)  
            yani age response_ms ye adade mosbat bod ye beyne on adad mosbate 
            va 0 kodom bozorgtare? khob maloome response_ms valiiii age response_ms 
            adade manfibod beyen on va 0 kodom bozorgtare? 0 pas hichvaght hata ag be
            bug ham bokhorim gharar nist adade manfi bhmoon bargardoone
        '''
        
        response_timedelta=now() - self.log['requested_at']
        response_ms= int(response_timedelta.total_seconds()*1000)      
        return max(response_ms,0)  
    
    
    
    def should_log(self,request,response):
        return (
            self.logging_methods=='__all__' or request.method in self.logging_methods
        )
    '''
        vaghti kasi az module base_mixins.py dare estefade mikone khodesh mitone biad in method should_log()
        ro override bokone va vasash har sharti k doost dare ro bezare.
    '''    
    
    
    