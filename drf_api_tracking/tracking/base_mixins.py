from django.utils.timezone import now
import ipaddress


class BaseLoggingMixin:
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
    
    def finalize_response(self, request, response, *args, **kwargs):
        response= super().finalize_response(request, response, *args, **kwargs)
        self.log.update(
            {'remote_addr':self._get_ip_address(request)} ,
        )
        self.handle_log()
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
            ipaddr=request.META.get('REMOTE_ADDR', '').splite(',')[0]   # dar soorati k tooye header ha 'HTTP_X_FORWARDED_FOR' ro nadashti
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